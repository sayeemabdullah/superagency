#!/usr/bin/env python3
"""Measure routing accuracy: does each prompt reach the right reference file?

A router skill degrades silently. Add a workflow whose description overlaps an
existing one and nothing errors — requests just start landing in the wrong file
and the answers get quietly worse. This turns that into a number.

Not part of CI's blocking path: it costs money and is non-deterministic.

  export ANTHROPIC_API_KEY=sk-...
  python3 scripts/eval_routing.py
  python3 scripts/eval_routing.py --limit 10 --model claude-sonnet-5
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_MD = os.path.join(ROOT, "superagency", "SKILL.md")
CASES = os.path.join(ROOT, "evals", "routing.jsonl")
API = "https://api.anthropic.com/v1/messages"

INSTRUCTION = """You are routing a request using the skill below.

Read the routing table and reply with the single reference filename you would
open — for example `seo.md`. Nothing else: no path, no backticks, no
explanation. If several could apply, give the primary one only.

---

{skill}
"""


def ask(prompt, skill, model, api_key):
    body = json.dumps({
        "model": model,
        "max_tokens": 20,
        "system": INSTRUCTION.format(skill=skill),
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(API, data=body, headers={
        "content-type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.load(resp)
    text = "".join(b.get("text", "") for b in data.get("content", []))
    m = re.search(r"([a-z-]+\.md)", text.strip())
    return m.group(1) if m else text.strip()[:40]


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--model", default="claude-sonnet-5")
    p.add_argument("--limit", type=int, help="run only the first N cases")
    p.add_argument("--workers", type=int, default=6)
    p.add_argument("--json", action="store_true")
    p.add_argument("--fail-under", type=float, default=0.0,
                   help="exit non-zero if accuracy falls below this (0-1)")
    args = p.parse_args(argv)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("error: ANTHROPIC_API_KEY is not set.\n"
              "This eval calls the API and costs money, which is why it is not "
              "part of the PR check.", file=sys.stderr)
        return 2

    skill = open(SKILL_MD).read()
    cases = [json.loads(l) for l in open(CASES) if l.strip()]
    if args.limit:
        cases = cases[:args.limit]

    def run(case):
        try:
            got = ask(case["prompt"], skill, args.model, api_key)
            return {**case, "got": got, "ok": got == case["expect"]}
        except urllib.error.HTTPError as e:
            return {**case, "got": f"HTTP {e.code}", "ok": False, "error": e.read().decode()[:200]}
        except Exception as e:  # noqa: BLE001 - report, don't crash the sweep
            return {**case, "got": type(e).__name__, "ok": False, "error": str(e)[:200]}

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(run, cases))

    hits = sum(r["ok"] for r in results)
    accuracy = hits / len(results) if results else 0.0
    confusion = Counter((r["expect"], r["got"]) for r in results if not r["ok"])

    if args.json:
        print(json.dumps({"model": args.model, "cases": len(results), "correct": hits,
                          "accuracy": round(accuracy, 4),
                          "confusions": [{"expected": e, "got": g, "count": c}
                                         for (e, g), c in confusion.most_common()],
                          "results": results}, indent=2))
    else:
        print(f"{hits}/{len(results)} correct — {accuracy:.1%} ({args.model})\n")
        for r in results:
            if not r["ok"]:
                print(f"  MISS  {r['expect']:22} got {r['got']:22} {r['prompt'][:56]}")
                if r.get("error"):
                    print(f"        {r['error']}")
        if confusion:
            print("\nMost confused pairs:")
            for (exp, got), n in confusion.most_common(5):
                print(f"  {exp} -> {got}  x{n}")
        print("\nRecord this number. A drop after adding a workflow means the new "
              "description is competing with an existing one.")

    if args.fail_under and accuracy < args.fail_under:
        print(f"\naccuracy {accuracy:.1%} below threshold {args.fail_under:.1%}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
