#!/usr/bin/env python3
"""A/B test sample size and significance.

testing.md requires a sample size calculated before launch and forbids
declaring a winner on underpowered data. Both are arithmetic, and arithmetic
done by reasoning is where confident wrong answers come from. Run this instead.

Standard library only — the skill sandbox has no network for installs.

  python3 scripts/ab.py size --baseline 0.032 --mde 0.20 --daily-traffic 900
  python3 scripts/ab.py result --a 40000 1200 --b 40100 1310
"""
import argparse
import json
import math
import sys


def norm_cdf(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def norm_ppf(p):
    """Inverse normal CDF by bisection — exact enough and dependency-free."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be in (0, 1)")
    lo, hi = -40.0, 40.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if norm_cdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def sample_size(baseline, mde, alpha=0.05, power=0.80, two_sided=True):
    """Required n per variant to detect a relative lift of `mde` on `baseline`."""
    if not 0.0 < baseline < 1.0:
        raise ValueError("--baseline must be a rate between 0 and 1")
    if mde <= 0:
        raise ValueError("--mde must be positive")
    p1 = baseline
    p2 = baseline * (1.0 + mde)
    if p2 >= 1.0:
        raise ValueError("baseline * (1 + mde) reaches 100% — check your inputs")
    z_a = norm_ppf(1.0 - alpha / 2.0) if two_sided else norm_ppf(1.0 - alpha)
    z_b = norm_ppf(power)
    pooled = (p1 + p2) / 2.0
    n = ((z_a * math.sqrt(2.0 * pooled * (1.0 - pooled))
          + z_b * math.sqrt(p1 * (1.0 - p1) + p2 * (1.0 - p2))) ** 2) / ((p2 - p1) ** 2)
    return math.ceil(n), p1, p2


def two_proportion_test(n_a, x_a, n_b, x_b, alpha=0.05):
    """Two-proportion z-test. Pooled SE for the p-value, unpooled for the CI."""
    for n, x, label in ((n_a, x_a, "A"), (n_b, x_b, "B")):
        if n <= 0:
            raise ValueError(f"variant {label}: n must be positive")
        if not 0 <= x <= n:
            raise ValueError(f"variant {label}: conversions must be between 0 and n")
    p_a, p_b = x_a / n_a, x_b / n_b
    pooled = (x_a + x_b) / (n_a + n_b)
    se_pooled = math.sqrt(pooled * (1.0 - pooled) * (1.0 / n_a + 1.0 / n_b))
    if se_pooled == 0:
        raise ValueError("no variance in the data — both variants are 0% or 100%")
    z = (p_b - p_a) / se_pooled
    p_value = 2.0 * (1.0 - norm_cdf(abs(z)))
    se_diff = math.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)
    z_crit = norm_ppf(1.0 - alpha / 2.0)
    diff = p_b - p_a
    return {
        "rate_a": p_a,
        "rate_b": p_b,
        "absolute_diff": diff,
        "relative_lift": (diff / p_a) if p_a else None,
        "z": z,
        "p_value": p_value,
        "ci_low": diff - z_crit * se_diff,
        "ci_high": diff + z_crit * se_diff,
        "significant": p_value < alpha,
    }


def cmd_size(args):
    n, p1, p2 = sample_size(args.baseline, args.mde, args.alpha, args.power)
    out = {
        "n_per_variant": n,
        "n_total": n * 2,
        "baseline_rate": p1,
        "target_rate": p2,
        "alpha": args.alpha,
        "power": args.power,
    }
    if args.daily_traffic:
        days = math.ceil((n * 2) / args.daily_traffic)
        out["days_required"] = days
        # testing.md: run full weeks to avoid day-of-week skew
        out["days_rounded_to_full_weeks"] = math.ceil(days / 7) * 7
    if args.json:
        print(json.dumps(out, indent=2))
        return
    print(f"Need {n:,} per variant ({n * 2:,} total)")
    print(f"  to detect {p1:.2%} -> {p2:.2%} ({args.mde:.0%} relative lift)")
    print(f"  at alpha={args.alpha}, power={args.power:.0%}")
    if args.daily_traffic:
        print(f"  at {args.daily_traffic:,}/day: {out['days_required']} days "
              f"-> run {out['days_rounded_to_full_weeks']} (full weeks)")


def cmd_result(args):
    n_a, x_a = args.a
    n_b, x_b = args.b
    r = two_proportion_test(n_a, x_a, n_b, x_b, args.alpha)

    required, _, _ = sample_size(r["rate_a"], args.mde, args.alpha, args.power)
    underpowered = min(n_a, n_b) < required

    if r["significant"]:
        verdict = "significant"
        note = ("Significant is not the same as meaningful — check the interval "
                "is a lift worth shipping.")
    elif underpowered:
        verdict = "inconclusive (underpowered)"
        note = (f"Only {min(n_a, n_b):,} per variant; detecting a {args.mde:.0%} "
                f"lift needs ~{required:,}. Do not call this a loss.")
    else:
        verdict = "inconclusive"
        note = "Adequately powered and no effect found — the change was likely too small."

    r.update({"verdict": verdict, "note": note,
              "required_per_variant": required, "underpowered": underpowered})
    if args.json:
        print(json.dumps(r, indent=2))
        return
    print(f"A: {x_a:,}/{n_a:,} = {r['rate_a']:.3%}")
    print(f"B: {x_b:,}/{n_b:,} = {r['rate_b']:.3%}")
    print(f"Relative lift: {r['relative_lift']:+.2%}" if r["relative_lift"] is not None else "")
    print(f"p-value: {r['p_value']:.4f}   z: {r['z']:.3f}")
    print(f"95% CI on absolute difference: [{r['ci_low']:+.3%}, {r['ci_high']:+.3%}]")
    print(f"\nVerdict: {verdict}")
    print(f"  {note}")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("size", help="required sample size before launching")
    s.add_argument("--baseline", type=float, required=True, help="current rate, e.g. 0.032")
    s.add_argument("--mde", type=float, required=True, help="relative lift to detect, e.g. 0.20")
    s.add_argument("--alpha", type=float, default=0.05)
    s.add_argument("--power", type=float, default=0.80)
    s.add_argument("--daily-traffic", type=int, help="total daily visitors across variants")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_size)

    r = sub.add_parser("result", help="read a finished or running test")
    r.add_argument("--a", nargs=2, type=int, metavar=("N", "CONVERSIONS"), required=True)
    r.add_argument("--b", nargs=2, type=int, metavar=("N", "CONVERSIONS"), required=True)
    r.add_argument("--alpha", type=float, default=0.05)
    r.add_argument("--power", type=float, default=0.80)
    r.add_argument("--mde", type=float, default=0.20,
                   help="lift the test was designed to detect, for the power check")
    r.add_argument("--json", action="store_true")
    r.set_defaults(func=cmd_result)

    args = p.parse_args(argv)
    try:
        args.func(args)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
