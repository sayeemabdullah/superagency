#!/usr/bin/env python3
"""A deterministic, offline proxy for routing accuracy.

`eval_routing.py` asks a real model where each prompt should route. It is the
honest measure, but it costs money and is non-deterministic, so it can't gate a
PR. This script is the cheap tripwire that can: it builds a bag-of-words profile
for every workflow from its routing-table row, heading, and "Covers:" line, then
routes each eval prompt by weighted term overlap and reports how often that
lands on the expected file.

The absolute number means little — a lexical router is dumb. The *delta* is the
point. Add a workflow whose routing row collides with an existing one and this
score drops, in CI, before the ambiguity ships. The confusability report flags
the same risk directly, without needing a prompt to trip over it.

  python3 scripts/route_lint.py
  python3 scripts/route_lint.py --json
  python3 scripts/route_lint.py --fail-under 0.75
"""
import argparse
import collections
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_MD = os.path.join(ROOT, "superagency", "SKILL.md")
REF_DIR = os.path.join(ROOT, "superagency", "references")
CASES = os.path.join(ROOT, "evals", "routing.jsonl")

STOP = set("""
a an the this that these those and or but if then else for to of in on at by with
from into over under out up down off as is are was were be been being do does did
you your we our they their it its i me my he she his her them us who whom which what
whats how why when where should would could can will do dont don t not no yes any
some more most our need want get give me our using use used make made new one two
three our about actually even just our our our our our our
""".split())

TOKEN = re.compile(r"[a-z0-9]+")


def norm(tok):
    tok = tok.lower()
    if len(tok) > 4 and tok.endswith("s") and not tok.endswith("ss"):
        tok = tok[:-1]
    return tok


def tokens(text):
    return [norm(t) for t in TOKEN.findall(text.lower())
            if t not in STOP and len(t) >= 3 and norm(t) not in STOP]


def profiles():
    """term -> weight, per reference filename, from SKILL.md + the file itself."""
    skill = open(SKILL_MD).read()
    rows = re.findall(r"^\| (.+?) \| `references/([a-z\-]+\.md)` \|$", skill, re.M)
    row_text = {fn: desc for desc, fn in rows}

    raw = {}
    for fn in sorted(os.listdir(REF_DIR)):
        if not fn.endswith(".md") or fn in ("brand.md", "pulse-log.md"):
            continue
        if fn not in row_text:
            continue
        text = open(os.path.join(REF_DIR, fn)).read()
        bag = collections.Counter()
        # Routing row carries the most intent — weight it heavily; then the
        # headings, then the body at low weight so oblique prompts still land.
        bag.update(tokens(row_text[fn]) * 6)
        for line in text.splitlines():
            if line.startswith(("# ", "Covers:", "## ", "Often pairs with:")):
                bag.update(tokens(line) * 2)
            else:
                bag.update(tokens(line))
        raw[fn] = bag

    df = collections.Counter()
    for bag in raw.values():
        df.update(bag.keys())
    n = len(raw)
    idf = {t: math.log(1 + n / c) for t, c in df.items()}

    weighted = {}
    for fn, bag in raw.items():
        weighted[fn] = {t: cnt * idf[t] for t, cnt in bag.items()}
    return weighted


def route(prompt, weighted):
    toks = set(tokens(prompt))
    best, score = None, 0.0
    for fn, vec in weighted.items():
        s = sum(vec.get(t, 0.0) for t in toks)
        if s > score:
            best, score = fn, s
    return best


def confusable_pairs(weighted, top=8):
    names = sorted(weighted)
    sims = []
    for i, a in enumerate(names):
        va = weighted[a]
        na = math.sqrt(sum(v * v for v in va.values())) or 1.0
        for b in names[i + 1:]:
            vb = weighted[b]
            nb = math.sqrt(sum(v * v for v in vb.values())) or 1.0
            dot = sum(va[t] * vb.get(t, 0.0) for t in va)
            sims.append((dot / (na * nb), a, b))
    sims.sort(reverse=True)
    return sims[:top]


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--json", action="store_true")
    p.add_argument("--fail-under", type=float, default=0.0,
                   help="exit non-zero if accuracy falls below this (0-1)")
    args = p.parse_args(argv)

    weighted = profiles()
    cases = [json.loads(l) for l in open(CASES) if l.strip()]
    results = [{**c, "got": route(c["prompt"], weighted)} for c in cases]
    for r in results:
        r["ok"] = r["got"] == r["expect"]
    hits = sum(r["ok"] for r in results)
    acc = hits / len(results) if results else 0.0
    confusion = collections.Counter((r["expect"], r["got"]) for r in results if not r["ok"])
    pairs = confusable_pairs(weighted)

    if args.json:
        print(json.dumps({
            "cases": len(results), "correct": hits, "accuracy": round(acc, 4),
            "misses": [{"prompt": r["prompt"], "expect": r["expect"], "got": r["got"]}
                       for r in results if not r["ok"]],
            "confusion": [{"expected": e, "got": g, "count": c}
                          for (e, g), c in confusion.most_common()],
            "most_similar_profiles": [{"a": a, "b": b, "cosine": round(s, 3)}
                                      for s, a, b in pairs],
        }, indent=2))
    else:
        print(f"lexical routing: {hits}/{len(results)} = {acc:.1%} "
              "(offline proxy — watch the delta, not the value)\n")
        for r in results:
            if not r["ok"]:
                print(f"  MISS  {r['expect']:22} got {str(r['got']):22} {r['prompt'][:52]}")
        print("\nmost similar workflow profiles (a collision risk if a new one joins here):")
        for s, a, b in pairs:
            print(f"  {s:.3f}  {a}  ~  {b}")

    if args.fail_under and acc < args.fail_under:
        print(f"\naccuracy {acc:.1%} is below the {args.fail_under:.0%} floor", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
