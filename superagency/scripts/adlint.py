#!/usr/bin/env python3
"""Check ad copy against platform character limits.

paid.md lists these limits; counting characters is exactly the kind of
mechanical work a language model gets wrong while sounding certain. Run the
copy through here before handing it over.

Limits marked "hard" are enforced by the platform and reject on submit.
Limits marked "soft" are truncation or visibility thresholds — exceeding them
is a judgement call, not an error.

  python3 scripts/adlint.py google --headline "Cut invoicing to 20 minutes" \
      --description "Stop chasing paperwork. Try it free for 14 days."
"""
import argparse
import json
import sys

# paid.md says specs change and must be re-verified. This date says when these
# were last checked; if it is stale, search before trusting the numbers.
SPECS_VERIFIED = "2026-08"

PLATFORMS = {
    "google": {
        "headline":    {"limit": 30,  "kind": "hard", "max_count": 15, "min_count": 3},
        "description": {"limit": 90,  "kind": "hard", "max_count": 4,  "min_count": 2},
        "path":        {"limit": 15,  "kind": "hard", "max_count": 2},
    },
    "meta": {
        "primary":     {"limit": 125, "kind": "soft", "note": "visible before 'See more'"},
        "headline":    {"limit": 40,  "kind": "hard"},
        "description": {"limit": 30,  "kind": "hard"},
    },
    "linkedin": {
        "primary":     {"limit": 150, "kind": "soft", "note": "truncates after this"},
        "headline":    {"limit": 70,  "kind": "hard"},
    },
    "x": {
        "primary":     {"limit": 280, "kind": "hard"},
    },
    "tiktok": {
        "primary":     {"limit": 100, "kind": "hard", "note": "ad text; the hook matters more"},
    },
}

FIELDS = ("headline", "description", "primary", "path")


def lint(platform, fields):
    spec = PLATFORMS[platform]
    results, errors, warnings = [], 0, 0

    for name, values in fields.items():
        if not values:
            continue
        if name not in spec:
            warnings += 1
            results.append({"field": name, "status": "unsupported",
                            "message": f"{platform} has no '{name}' field"})
            continue
        rule = spec[name]
        for i, text in enumerate(values, 1):
            n = len(text)
            over = n - rule["limit"]
            if over > 0:
                status = "fail" if rule["kind"] == "hard" else "warn"
                errors += status == "fail"
                warnings += status == "warn"
                msg = f"{n} chars, {over} over the {rule['limit']} limit"
            else:
                status = "pass"
                msg = f"{n}/{rule['limit']}"
            entry = {"field": name, "index": i, "chars": n, "limit": rule["limit"],
                     "kind": rule["kind"], "status": status, "message": msg, "text": text}
            if "note" in rule:
                entry["note"] = rule["note"]
            results.append(entry)

        count = len(values)
        if "max_count" in rule and count > rule["max_count"]:
            errors += 1
            results.append({"field": name, "status": "fail",
                            "message": f"{count} supplied, {platform} accepts at most {rule['max_count']}"})
        if "min_count" in rule and count < rule["min_count"]:
            warnings += 1
            results.append({"field": name, "status": "warn",
                            "message": f"only {count} supplied; {rule['min_count']}+ recommended so the system can rotate"})

    return results, errors, warnings


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("platform", choices=sorted(PLATFORMS))
    for f in FIELDS:
        p.add_argument(f"--{f}", action="append", default=[],
                       help=f"repeatable; one flag per {f}")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    fields = {f: getattr(args, f) for f in FIELDS}
    if not any(fields.values()):
        print("error: supply at least one field, e.g. --headline \"...\"", file=sys.stderr)
        return 1

    results, errors, warnings = lint(args.platform, fields)

    if args.json:
        print(json.dumps({"platform": args.platform, "specs_verified": SPECS_VERIFIED,
                          "errors": errors, "warnings": warnings, "results": results}, indent=2))
        return 1 if errors else 0

    mark = {"pass": "ok  ", "warn": "warn", "fail": "FAIL", "unsupported": "warn"}
    for r in results:
        idx = f"[{r['index']}]" if "index" in r else "   "
        print(f"{mark[r['status']]} {r['field']}{idx} {r['message']}")
        if r.get("note"):
            print(f"       ({r['note']})")
    print(f"\n{errors} error(s), {warnings} warning(s) — specs verified {SPECS_VERIFIED}")
    if errors or warnings:
        print("Specs change often. Re-check the platform's current limits before shipping.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
