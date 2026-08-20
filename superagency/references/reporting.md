# Performance Reporting

Covers: weekly pulse, monthly/quarterly reviews, trend summaries.

## Weekly pulse
1. Get the numbers — pasted, or from a connected source if one's available. Check before asking the user to paste.
2. **Top 3 wins** and **top 3 misses** — specific metrics with numbers, not vague statements.
3. **Anomalies** — sharp jumps or drops flagged separately, even if not top-3.
4. **One recommended action** for next week. One, not five.
5. **Trend** — compare to `pulse-log.md` if prior entries exist. Note direction, not just this week's raw number.
6. Append this week's summary to `pulse-log.md` using the entry template at the top of that file — identical structure every week is what makes `trend` comparisons possible. Then print the appended entry so the user can save it to their local copy — the write does not survive the session.
7. Format: ask Slack-style (short, scannable) or email-style (fuller, with greeting) if unclear.

## Monthly / quarterly review
Adds: goal attainment vs target, channel-by-channel breakdown, spend efficiency, and next-period priorities. Narrative over dashboard — say what happened and why, not just what the numbers were.

## Output
Pulse → inline, copy-pasteable into Slack or email. Monthly/quarterly reviews → file.

For shape, see `references/examples/weekly-pulse.md` — note the anomaly called out separately, the metric that looks good but isn't, and the single action.

## Tools
Write entries through the script so every week has the identical structure that
`trend` depends on.

```bash
python3 scripts/pulse.py append --week 2026-08-10 2026-08-16 \
  --win "signups 412 (+18%% wow)" --miss "demo requests 22 (-9%% wow)" \
  --next-action "test the pricing page hero"

python3 scripts/pulse.py trend
```

`trend` parses every entry and reports direction across the whole range. If it
finds only one data point for a metric, say so rather than implying a trend.

## Rules
- Don't report metrics without context. "1,200 clicks" means nothing; "1,200 clicks, up 40% on a flat budget" means something.
- Distinguish correlation from cause. If traffic rose the same week as a campaign *and* a press mention, say both.
- Call out metrics that look good but aren't (impressions up, conversions flat).
- Never fabricate numbers the user didn't provide.
