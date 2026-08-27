# Paid Ads

Covers: Google, Meta, LinkedIn, X, TikTok ad copy and strategy.

Often pairs with: `cro.md` — the landing page is half the campaign.

## Search first
Ad format specs, character limits, and targeting options change often. Verify current specs before writing to them.

## Copy structure by platform
- **Google Search** — headlines (30 chars each) + descriptions (90 chars). Write more variants than needed; the system rotates. Include the keyword in at least one headline.
- **Meta** — primary text (first ~125 chars visible), headline, description. Hook in the first line. Creative matters more than copy here.
- **LinkedIn** — intro text (~150 chars before truncation), headline (~70). Professional framing, but avoid corporate mush.
- **TikTok/Reels** — script, not copy. Hook in first 2 seconds.

## Strategy checklist
- Objective matches the funnel stage (don't run conversion campaigns to cold traffic with no warm-up)
- Audience definition — and what you're *excluding* (existing customers, recent converters)
- Budget split across campaigns, with a testing allocation (~20%)
- Success metric: CPA or ROAS, defined before launch
- Landing page matches the ad promise — biggest single source of wasted spend

## Creative testing
Test one variable at a time. Suggest 3-5 variants on the hook or headline first; that moves numbers more than button color.

## Output
Ad copy variants → inline, grouped by platform with character counts shown. Campaign strategy and structure → file.

## Tools
Character counts are mechanical and easy to get wrong by eye. Lint every set of
ad copy before handing it over.

```bash
python3 scripts/adlint.py google \
  --headline "Cut invoicing to 20 minutes" --headline "Stop chasing paperwork" \
  --description "Try it free for 14 days. No card needed."
```

Platforms: `google`, `meta`, `linkedin`, `x`, `tiktok`. Hard limits are rejected
on submit; soft limits are truncation thresholds and are a judgement call. The
script prints when its specs were last verified — if that's stale, search.

## Red flags
| Thought | Reality |
|---|---|
| "That headline looks about thirty characters." | Run `scripts/adlint.py`. Counting characters by eye is exactly the thing you get wrong while feeling certain. |
| "I remember the current ad specs." | Specs change quarterly. Verify before writing copy that has to fit them. |
| "They asked what CPA to expect, I'll give a range." | You have no data for their account. A quoted range becomes a target you invented. |

## Rules
- Never promise specific CPA/ROAS figures.
- Flag any claim in ad copy that would need substantiation (superlatives, comparative claims, health/financial results).
