"""Known-answer tests for the bundled skill tools.

The point of shipping these tools is that arithmetic beats reasoning. That
only holds if the arithmetic is right, so the numbers below are checked
against independently known values rather than against the implementation.
"""
import io
import os
import sys
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "superagency", "scripts"))

import ab, adlint, budget, pulse, readability, utm  # noqa: E402


class TestNormal(unittest.TestCase):
    def test_cdf_known_points(self):
        self.assertAlmostEqual(ab.norm_cdf(0), 0.5, places=6)
        self.assertAlmostEqual(ab.norm_cdf(1.96), 0.975, places=4)
        self.assertAlmostEqual(ab.norm_cdf(-1.96), 0.025, places=4)

    def test_ppf_inverts_cdf(self):
        self.assertAlmostEqual(ab.norm_ppf(0.975), 1.959964, places=4)
        self.assertAlmostEqual(ab.norm_ppf(0.80), 0.841621, places=4)
        for p in (0.01, 0.25, 0.5, 0.9, 0.99):
            self.assertAlmostEqual(ab.norm_cdf(ab.norm_ppf(p)), p, places=6)


class TestSampleSize(unittest.TestCase):
    def test_matches_textbook_formula(self):
        """Derive the expected value here rather than hardcoding our own output,
        so this catches a wrong implementation instead of enshrining one."""
        import math
        p1, p2 = 0.05, 0.06
        za, zb = ab.norm_ppf(0.975), ab.norm_ppf(0.80)
        textbook = (za + zb) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / (p2 - p1) ** 2
        n, _, _ = ab.sample_size(0.05, 0.20)
        self.assertLess(abs(n / textbook - 1), 0.05, f"{n} vs textbook {textbook:.0f}")

    def test_within_lehrs_rule_of_thumb(self):
        """Lehr's rule: n ~= 16 * p(1-p) / delta^2 for 80% power, alpha .05."""
        lehr = 16 * (0.055 * 0.945) / (0.01 ** 2)
        n, _, _ = ab.sample_size(0.05, 0.20)
        self.assertLess(abs(n / lehr - 1), 0.10, f"{n} vs Lehr {lehr:.0f}")

    def test_smaller_effect_needs_more_traffic(self):
        big, _, _ = ab.sample_size(0.05, 0.20)
        small, _, _ = ab.sample_size(0.05, 0.05)
        self.assertGreater(small, big * 5)

    def test_more_power_needs_more_traffic(self):
        p80, _, _ = ab.sample_size(0.05, 0.20, power=0.80)
        p95, _, _ = ab.sample_size(0.05, 0.20, power=0.95)
        self.assertGreater(p95, p80)

    def test_rejects_impossible_inputs(self):
        for bad in ((0, 0.2), (1.5, 0.2), (0.05, 0)):
            with self.assertRaises(ValueError):
                ab.sample_size(*bad)


class TestSignificance(unittest.TestCase):
    def test_identical_variants_are_not_significant(self):
        r = ab.two_proportion_test(10000, 500, 10000, 500)
        self.assertAlmostEqual(r["p_value"], 1.0, places=6)
        self.assertFalse(r["significant"])

    def test_large_clear_difference_is_significant(self):
        r = ab.two_proportion_test(10000, 500, 10000, 700)
        self.assertLess(r["p_value"], 0.001)
        self.assertTrue(r["significant"])

    def test_tiny_sample_is_not_significant(self):
        r = ab.two_proportion_test(400, 12, 400, 13)
        self.assertFalse(r["significant"])

    def test_ci_brackets_the_observed_difference(self):
        r = ab.two_proportion_test(5000, 250, 5000, 300)
        self.assertLess(r["ci_low"], r["absolute_diff"])
        self.assertGreater(r["ci_high"], r["absolute_diff"])

    def test_relative_lift(self):
        r = ab.two_proportion_test(1000, 100, 1000, 120)
        self.assertAlmostEqual(r["relative_lift"], 0.20, places=6)

    def test_rejects_bad_counts(self):
        with self.assertRaises(ValueError):
            ab.two_proportion_test(100, 200, 100, 10)


class TestAdLint(unittest.TestCase):
    def test_google_headline_boundary(self):
        exactly_30 = "x" * 30
        res, errors, _ = adlint.lint("google", {"headline": [exactly_30, "x" * 31]})
        self.assertEqual(errors, 1)
        statuses = [r["status"] for r in res if r.get("index")]
        self.assertEqual(statuses, ["pass", "fail"])

    def test_soft_limit_warns_not_fails(self):
        _, errors, warnings = adlint.lint("meta", {"primary": ["x" * 200]})
        self.assertEqual(errors, 0)
        self.assertGreaterEqual(warnings, 1)

    def test_too_many_headlines_fails(self):
        _, errors, _ = adlint.lint("google", {"headline": ["ok"] * 16})
        self.assertGreaterEqual(errors, 1)

    def test_every_platform_has_a_field(self):
        for name, spec in adlint.PLATFORMS.items():
            self.assertTrue(spec, f"{name} has no fields")
            for field, rule in spec.items():
                self.assertIn(rule["kind"], ("hard", "soft"))
                self.assertGreater(rule["limit"], 0)


class TestUTM(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(utm.normalize("Spring Launch 2026"), "spring-launch-2026")
        self.assertEqual(utm.normalize("Email_Blast"), "email-blast")
        self.assertEqual(utm.normalize("  GOOGLE  "), "google")
        self.assertEqual(utm.normalize("a--b"), "a-b")

    def test_build_lowercases_and_preserves_existing_query(self):
        url, changed = utm.build("https://x.com/p?ref=abc", {
            "utm_source": "LinkedIn", "utm_medium": "CPC", "utm_campaign": "Q3 Push"})
        self.assertIn("ref=abc", url)
        self.assertIn("utm_source=linkedin", url)
        self.assertIn("utm_campaign=q3-push", url)
        self.assertIn("utm_source", changed)

    def test_build_rejects_relative_url(self):
        with self.assertRaises(ValueError):
            utm.build("/pricing", {"utm_source": "x"})

    def test_audit_flags_case_and_underscores(self):
        findings, _ = utm.audit(
            ["https://x.com/p?utm_source=Google&utm_medium=cpc&utm_campaign=Spring_Launch"])
        self.assertFalse(findings[0]["ok"])

    def test_audit_detects_campaign_drift(self):
        _, drift = utm.audit([
            "https://x.com/p?utm_source=a&utm_medium=cpc&utm_campaign=spring-launch",
            "https://x.com/p?utm_source=b&utm_medium=cpc&utm_campaign=Spring_Launch"])
        self.assertIn("spring-launch", drift)

    def test_clean_url_passes(self):
        findings, drift = utm.audit(
            ["https://x.com/p?utm_source=google&utm_medium=cpc&utm_campaign=spring-launch"])
        self.assertTrue(findings[0]["ok"])
        self.assertFalse(drift)


class TestBudget(unittest.TestCase):
    def test_backsolve_arithmetic(self):
        r = budget.backsolve(3000, 0.02, 2.40)
        self.assertEqual(r["visits_required"], 150000)
        self.assertAlmostEqual(r["spend_required"], 360000.0, places=2)
        self.assertAlmostEqual(r["cost_per_conversion"], 120.0, places=2)

    def test_shortfall_is_reported_not_hidden(self):
        r = budget.backsolve(3000, 0.02, 2.40, budget=100000)
        self.assertFalse(r["reaches_goal"])
        self.assertAlmostEqual(r["shortfall"], 260000.0, places=2)
        self.assertEqual(r["conversions_affordable"], 833)

    def test_sufficient_budget(self):
        r = budget.backsolve(100, 0.02, 2.40, budget=100000)
        self.assertTrue(r["reaches_goal"])

    def test_split_sums_to_total(self):
        r = budget.split(40000, (0.7, 0.2, 0.1))
        self.assertAlmostEqual(sum(r["allocation"].values()), 40000, places=2)

    def test_split_rejects_bad_weights(self):
        with self.assertRaises(ValueError):
            budget.split(1000, (0.5, 0.2, 0.1))

    def test_payback(self):
        r = budget.payback(300, 50, 0.8)
        self.assertAlmostEqual(r["payback_months"], 7.5, places=1)


class TestReadability(unittest.TestCase):
    def test_syllables(self):
        for word, expected in (("cat", 1), ("running", 2), ("beautiful", 3), ("the", 1)):
            self.assertEqual(readability.syllables(word), expected, word)

    def test_simple_text_scores_easier_than_complex(self):
        simple = readability.analyze("The cat sat. The dog ran. We go now.")
        complex_ = readability.analyze(
            "Notwithstanding the aforementioned considerations, the organization "
            "subsequently implemented a comprehensive optimization initiative.")
        self.assertGreater(simple["flesch_reading_ease"], complex_["flesch_reading_ease"])

    def test_flags_weak_words(self):
        r = readability.analyze("This is a very powerful and innovative solution.")
        self.assertIn("very", r["weak_words"])
        self.assertIn("powerful", r["weak_words"])

    def test_detects_passive(self):
        r = readability.analyze("The report was written by the team.")
        self.assertTrue(r["passive_hits"])

    def test_counts_words_and_sentences(self):
        r = readability.analyze("One two three. Four five!")
        self.assertEqual(r["words"], 5)
        self.assertEqual(r["sentences"], 2)

    def test_empty_input_raises(self):
        with self.assertRaises(ValueError):
            readability.analyze("   ")


class TestPulse(unittest.TestCase):
    def test_render_then_parse_round_trip(self):
        entry = pulse.render("2026-08-03", "2026-08-09",
                             ["signups 350 (+5% wow)"], ["demos 24"], None, None, "ship it")
        parsed = pulse.parse(entry)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["from"], "2026-08-03")
        self.assertIn("wins", parsed[0]["fields"])

    def test_metric_extraction(self):
        m = pulse.metrics_in("signups 412 (+18% wow); trial starts 96")
        self.assertEqual(m["signups"]["value"], 412.0)
        self.assertEqual(m["trial starts"]["value"], 96.0)

    def test_metric_handles_commas(self):
        m = pulse.metrics_in("pageviews 1,250")
        self.assertEqual(m["pageviews"]["value"], 1250.0)

    def test_none_recorded_is_not_a_metric(self):
        self.assertEqual(pulse.metrics_in("none recorded"), {})

    def test_two_weeks_parse_in_order(self):
        text = (pulse.render("2026-08-03", "2026-08-09", ["signups 350"], [], None, None, None)
                + "\n\n"
                + pulse.render("2026-08-10", "2026-08-16", ["signups 412"], [], None, None, None))
        entries = pulse.parse(text)
        self.assertEqual([e["from"] for e in entries], ["2026-08-03", "2026-08-10"])


class TestCLIsAreWired(unittest.TestCase):
    """Every tool must expose --help without blowing up; a literal % in an
    argparse help string is enough to break it, and did once."""

    def test_help_exits_zero(self):
        for mod in (ab, adlint, budget, pulse, readability, utm):
            with self.subTest(mod=mod.__name__):
                with self.assertRaises(SystemExit) as cm:
                    with redirect_stdout(io.StringIO()):
                        mod.main(["--help"])
                self.assertEqual(cm.exception.code, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
