"""The offline routing proxy has to keep working and keep clearing its floor.

route_lint.py lives in scripts/ (dev tooling), not superagency/scripts/, so it
gets its own path setup rather than riding along in test_tools.py.
"""
import io
import os
import sys
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import route_lint  # noqa: E402

FLOOR = 0.60


class TestRouteLint(unittest.TestCase):
    def test_help_exits_zero(self):
        with self.assertRaises(SystemExit) as cm:
            with redirect_stdout(io.StringIO()):
                route_lint.main(["--help"])
        self.assertEqual(cm.exception.code, 0)

    def test_current_corpus_clears_the_floor(self):
        """If this fails, a routing row or a new workflow has collided with an
        existing one badly enough to matter — investigate before merging."""
        with redirect_stdout(io.StringIO()):
            rc = route_lint.main([f"--fail-under={FLOOR}"])
        self.assertEqual(rc, 0, f"lexical routing accuracy fell below {FLOOR:.0%}")

    def test_profiles_cover_every_routed_workflow(self):
        weighted = route_lint.profiles()
        self.assertGreaterEqual(len(weighted), 26)
        for fn, vec in weighted.items():
            self.assertTrue(vec, f"{fn} has an empty term profile")


if __name__ == "__main__":
    unittest.main(verbosity=2)
