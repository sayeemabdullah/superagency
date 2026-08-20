#!/usr/bin/env python3
"""Append weekly pulse entries and read the trend across them.

reporting.md requires every pulse-log.md entry to use one fixed structure,
because `trend` compares across weeks and drifting formats make that
impossible. Writing entries through this script is what actually enforces it.

  python3 scripts/pulse.py append --week 2026-08-10 2026-08-16 \
      --win "signups 412 (+18% wow)" --miss "demo requests 22 (-9% wow)" \
      --next-action "test the pricing page hero"
  python3 scripts/pulse.py trend
"""
import argparse
import json
import re
import sys

DEFAULT_LOG = "references/pulse-log.md"
HEADER = re.compile(r"^## Week of (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2})\s*$", re.M)
# "signups 412 (+18% wow)" -> metric, value, delta
METRIC = re.compile(r"^(?P<name>.+?)\s+(?P<value>-?[\d,.]+%?)\s*(?:\((?P<delta>[+-][\d.]+%?)[^)]*\))?$")


def render(week_from, week_to, wins, misses, anomalies, last_action, next_action):
    lines = [f"## Week of {week_from} to {week_to}"]
    lines.append("- **Wins:** " + ("; ".join(wins) if wins else "none recorded"))
    lines.append("- **Misses:** " + ("; ".join(misses) if misses else "none recorded"))
    lines.append("- **Anomalies:** " + (anomalies or "none"))
    lines.append("- **Last week's action:** " + (last_action or "not recorded"))
    lines.append("- **Next action:** " + (next_action or "not recorded"))
    return "\n".join(lines)


def parse(text):
    entries = []
    matches = list(HEADER.finditer(text))
    for i, m in enumerate(matches):
        body = text[m.end():matches[i + 1].start() if i + 1 < len(matches) else len(text)]
        fields = {}
        for line in body.splitlines():
            fm = re.match(r"\s*-\s*\*\*(.+?):?\*\*\s*(.*)", line)
            if fm:
                fields[fm.group(1).strip().lower().rstrip(":")] = fm.group(2).strip()
        entries.append({"from": m.group(1), "to": m.group(2), "fields": fields})
    return entries


def metrics_in(blob):
    found = {}
    for chunk in re.split(r";", blob):
        chunk = chunk.strip()
        if not chunk or chunk.lower().startswith("none"):
            continue
        mm = METRIC.match(chunk)
        if mm:
            raw = mm.group("value").replace(",", "").rstrip("%")
            try:
                found[mm.group("name").strip().lower()] = {
                    "value": float(raw), "delta": mm.group("delta")}
            except ValueError:
                continue
    return found


def cmd_append(args):
    entry = render(args.week[0], args.week[1], args.win, args.miss,
                   args.anomalies, args.last_action, args.next_action)
    try:
        current = open(args.file).read()
    except FileNotFoundError:
        print(f"error: {args.file} not found — run from the skill root", file=sys.stderr)
        return 1
    if f"## Week of {args.week[0]} to {args.week[1]}" in current:
        print(f"error: an entry for {args.week[0]} already exists", file=sys.stderr)
        return 1
    with open(args.file, "a") as fh:
        fh.write("\n" + entry + "\n")
    print(entry)
    print(f"\nAppended to {args.file}.")
    print("This write does not survive the session — print the file and have the "
          "user save it locally, or the history is lost.")
    return 0


def cmd_trend(args):
    try:
        entries = parse(open(args.file).read())
    except FileNotFoundError:
        print(f"error: {args.file} not found", file=sys.stderr)
        return 1
    if not entries:
        print("No entries yet. Nothing to trend against — report this week on its own.")
        return 0

    series = {}
    for e in entries:
        for bucket in ("wins", "misses"):
            for name, data in metrics_in(e["fields"].get(bucket, "")).items():
                series.setdefault(name, []).append({"week": e["from"], "value": data["value"]})

    trends = {}
    for name, points in series.items():
        if len(points) < 2:
            continue
        first, last = points[0]["value"], points[-1]["value"]
        trends[name] = {
            "points": len(points), "first": first, "last": last,
            "change_pct": round(((last - first) / first * 100), 1) if first else None,
            "direction": "up" if last > first else "down" if last < first else "flat",
        }

    out = {"entries": len(entries),
           "range": [entries[0]["from"], entries[-1]["to"]],
           "trends": trends}
    if args.json:
        print(json.dumps(out, indent=2))
        return 0

    print(f"{len(entries)} entries, {entries[0]['from']} to {entries[-1]['to']}")
    if not trends:
        print("\nOnly one data point per metric — need at least two weeks to show direction.")
        return 0
    print("\nMetrics tracked across weeks:")
    for name, t in sorted(trends.items()):
        chg = f"{t['change_pct']:+.1f}%" if t["change_pct"] is not None else "n/a"
        print(f"  {name:28} {t['first']:>10,.0f} -> {t['last']:>10,.0f}  {chg:>8}  ({t['points']} wks)")
    print("\nDirection over the whole range, not week-on-week. "
          "State what changed and why, not just the number.")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--file", default=DEFAULT_LOG)
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("append", help="append an entry in the required format")
    a.add_argument("--week", nargs=2, metavar=("FROM", "TO"), required=True)
    a.add_argument("--win", action="append", default=[], help='repeatable, e.g. "signups 412 (+18%% wow)"')
    a.add_argument("--miss", action="append", default=[])
    a.add_argument("--anomalies")
    a.add_argument("--last-action")
    a.add_argument("--next-action")
    a.set_defaults(func=cmd_append)

    t = sub.add_parser("trend", help="compare metrics across entries")
    t.add_argument("--json", action="store_true")
    t.set_defaults(func=cmd_trend)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
