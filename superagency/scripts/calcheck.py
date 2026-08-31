#!/usr/bin/env python3
"""Check a content-calendar table for dependencies that land too late.

campaigns.md calls a dependency finishing after the item it blocks "the most
common way calendars break." Spotting it by eye across twenty rows is exactly
what fails. This parses the table, resolves each `dependency` cell — an ISO
date, a week offset like -3, or another row's asset name — and flags any item
whose dependency lands on or after its own due date, plus dependencies that
resolve to nothing.

  python3 scripts/calcheck.py calendar.md
  python3 scripts/calcheck.py --json calendar.md
  cat calendar.md | python3 scripts/calcheck.py
"""
import argparse
import datetime
import json
import re
import sys

DATE_COLS = ("date", "due", "due date", "when", "week")
ASSET_COLS = ("asset", "item", "deliverable", "task")
DEP_COLS = ("dependency", "depends", "depends on", "blocked by", "prerequisite")


def parse_when(raw):
    """Return ('date', date) or ('offset', int) or None."""
    s = raw.strip()
    m = re.search(r"\d{4}-\d{2}-\d{2}", s)
    if m:
        try:
            return ("date", datetime.date.fromisoformat(m.group(0)))
        except ValueError:
            return None
    m = re.fullmatch(r"(?:week\s*|w\s*|t\s*)?([+-]?\d+)", s, re.I)
    if m:
        return ("offset", int(m.group(1)))
    return None


def split_row(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells


def is_separator(cells):
    return all(re.fullmatch(r":?-{2,}:?", c or "-") for c in cells if c is not None)


def find_col(header, names):
    for i, h in enumerate(header):
        if h.strip().lower() in names:
            return i
    return None


def parse_table(text):
    rows = [split_row(l) for l in text.splitlines() if l.lstrip().startswith("|")]
    rows = [r for r in rows if r and any(c for c in r)]
    if len(rows) < 2:
        raise ValueError("no table found (need a header row and at least one data row)")
    header = rows[0]
    body = [r for r in rows[1:] if not is_separator(r)]

    di = find_col(header, DATE_COLS)
    ai = find_col(header, ASSET_COLS)
    pi = find_col(header, DEP_COLS)
    if di is None:
        raise ValueError(f"no date column — looked for one of {sorted(DATE_COLS)}")
    if pi is None:
        raise ValueError(f"no dependency column — looked for one of {sorted(DEP_COLS)}")

    items = []
    for r in body:
        if max(di, pi, ai or 0) >= len(r):
            continue
        items.append({
            "asset": r[ai].strip() if ai is not None and ai < len(r) else "",
            "when_raw": r[di].strip(),
            "when": parse_when(r[di]),
            "dep_raw": r[pi].strip(),
        })
    return items


NONE_WORDS = {"", "-", "—", "none", "n/a", "na"}


def check(items):
    by_asset = {it["asset"].lower(): it for it in items if it["asset"]}
    findings = []

    for it in items:
        dep = it["dep_raw"]
        problem = None
        if dep.lower() in NONE_WORDS:
            resolved = None
        else:
            target = by_asset.get(dep.lower())
            if not target:
                target = next((o for o in items if o["asset"]
                               and o["asset"].lower() in dep.lower()), None)
            if target:
                resolved = target["when"]
                dep_label = f"{dep!r} (row: {target['asset']})"
            else:
                resolved = parse_when(dep)
                dep_label = f"{dep!r}"

            if resolved is None:
                problem = f"dependency {dep_label} doesn't resolve to a date, an offset, or another row"
            elif it["when"] is None:
                problem = f"row's own due value {it['when_raw']!r} isn't a date or offset, can't compare"
            elif resolved[0] != it["when"][0]:
                problem = (f"dependency is a {resolved[0]} but this row's due is a "
                           f"{it['when'][0]} — not comparable")
            elif resolved[1] > it["when"][1]:
                problem = (f"dependency {dep_label} lands {resolved[1]} — after this "
                           f"item's own due {it['when_raw']!r}")

        if problem:
            findings.append({"asset": it["asset"] or it["when_raw"],
                             "due": it["when_raw"], "dependency": it["dep_raw"],
                             "problem": problem})
    return findings


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("file", nargs="?", help="calendar markdown file (default: stdin)")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    raw = open(args.file) if args.file else sys.stdin
    text = raw.read()
    if args.file:
        raw.close()

    try:
        items = parse_table(text)
        findings = check(items)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({"rows": len(items), "problems": len(findings),
                          "findings": findings}, indent=2))
        return 1 if findings else 0

    if not findings:
        print(f"ok — {len(items)} rows, every dependency lands before the item it blocks")
        return 0

    print(f"{len(findings)} of {len(items)} rows have a dependency problem:\n")
    for f in findings:
        print(f"  {f['asset']}  (due {f['due']})")
        print(f"    - {f['problem']}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
