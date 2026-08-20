#!/usr/bin/env python3
"""Build and audit UTM-tagged URLs.

analytics.md calls inconsistent tagging "the single most common way reporting
breaks" — google vs Google vs GOOGLE become three sources in every report.
Consistency by hand across dozens of links is exactly what fails; this
normalizes on build and catches drift on audit.

  python3 scripts/utm.py build --url https://x.com/pricing \
      --source linkedin --medium cpc --campaign spring-launch --content hero-a
  python3 scripts/utm.py check urls.txt
"""
import argparse
import json
import re
import sys
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

REQUIRED = ("utm_source", "utm_medium", "utm_campaign")
OPTIONAL = ("utm_content", "utm_term")
# analytics.md: all lowercase, hyphens not spaces, consistent forever.
VALID = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def normalize(value):
    v = value.strip().lower()
    v = re.sub(r"[\s_]+", "-", v)
    v = re.sub(r"[^a-z0-9-]", "", v)
    return re.sub(r"-{2,}", "-", v).strip("-")


def build(url, params):
    parts = urlparse(url)
    if not parts.scheme or not parts.netloc:
        raise ValueError(f"not a valid absolute URL: {url}")
    existing = parse_qs(parts.query, keep_blank_values=True)
    changed = {}
    for key, raw in params.items():
        if raw is None:
            continue
        clean = normalize(raw)
        if not clean:
            raise ValueError(f"{key} is empty after normalizing {raw!r}")
        if clean != raw:
            changed[key] = (raw, clean)
        existing[key] = [clean]
    query = urlencode([(k, v[0]) for k, v in existing.items()])
    return urlunparse(parts._replace(query=query)), changed


def audit(urls):
    findings, campaigns, seen = [], {}, {}
    for url in urls:
        q = parse_qs(urlparse(url).query)
        flat = {k: v[0] for k, v in q.items() if k.startswith("utm_")}
        problems = []
        for key in REQUIRED:
            if key not in flat:
                problems.append(f"missing {key}")
        for key, val in flat.items():
            if key not in REQUIRED + OPTIONAL:
                problems.append(f"unknown parameter {key}")
                continue
            if not VALID.match(val):
                why = []
                if val != val.lower():
                    why.append("not lowercase")
                if " " in val or "%20" in val:
                    why.append("contains spaces")
                if "_" in val:
                    why.append("uses underscores, convention is hyphens")
                problems.append(f"{key}={val!r} ({', '.join(why) or 'invalid characters'}) "
                                f"-> {normalize(val)}")
        if "utm_term" in flat and flat.get("utm_medium") not in ("cpc", "ppc", "paid"):
            problems.append("utm_term is for paid search only")
        name = flat.get("utm_campaign")
        if name:
            campaigns.setdefault(normalize(name), set()).add(name)
        key = (flat.get("utm_source"), flat.get("utm_medium"), name)
        if key in seen and all(key):
            problems.append(f"duplicate source/medium/campaign, same as line {seen[key]}")
        elif all(key):
            seen[key] = len(findings) + 1
        findings.append({"url": url, "problems": problems, "ok": not problems})

    drift = {norm: sorted(v) for norm, v in campaigns.items() if len(v) > 1}
    return findings, drift


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="build a normalized tagged URL")
    b.add_argument("--url", required=True)
    b.add_argument("--source", required=True)
    b.add_argument("--medium", required=True)
    b.add_argument("--campaign", required=True)
    b.add_argument("--content")
    b.add_argument("--term")
    b.add_argument("--json", action="store_true")

    c = sub.add_parser("check", help="audit existing tagged URLs")
    c.add_argument("file", nargs="?", help="file of URLs, one per line (default: stdin)")
    c.add_argument("--json", action="store_true")

    args = p.parse_args(argv)

    if args.cmd == "build":
        try:
            url, changed = build(args.url, {
                "utm_source": args.source, "utm_medium": args.medium,
                "utm_campaign": args.campaign, "utm_content": args.content,
                "utm_term": args.term})
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps({"url": url, "normalized": {k: {"from": a, "to": b_}
                                                         for k, (a, b_) in changed.items()}}, indent=2))
            return 0
        print(url)
        for key, (before, after) in changed.items():
            print(f"  normalized {key}: {before!r} -> {after!r}", file=sys.stderr)
        return 0

    raw = open(args.file) if args.file else sys.stdin
    urls = [l.strip() for l in raw if l.strip() and not l.startswith("#")]
    if args.file:
        raw.close()
    if not urls:
        print("error: no URLs supplied", file=sys.stderr)
        return 1

    findings, drift = audit(urls)
    bad = sum(not f["ok"] for f in findings)

    if args.json:
        print(json.dumps({"checked": len(findings), "with_problems": bad,
                          "campaign_drift": drift, "findings": findings}, indent=2))
        return 1 if bad or drift else 0

    for i, f in enumerate(findings, 1):
        if f["ok"]:
            print(f"ok   [{i}] {f['url']}")
        else:
            print(f"FAIL [{i}] {f['url']}")
            for prob in f["problems"]:
                print(f"       - {prob}")
    if drift:
        print("\nCampaign name drift — these collapse to the same campaign but were tagged differently:")
        for norm, variants in drift.items():
            print(f"  {norm}: {', '.join(repr(v) for v in variants)}")
    print(f"\n{len(findings)} checked, {bad} with problems")
    return 1 if bad or drift else 0


if __name__ == "__main__":
    sys.exit(main())
