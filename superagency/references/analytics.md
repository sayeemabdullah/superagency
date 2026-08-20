# Analytics & Tracking

Covers: UTM conventions, event tracking, attribution, dashboards.

## UTM convention
`utm_source` = where (google, linkedin, newsletter)
`utm_medium` = type (cpc, email, social, referral)
`utm_campaign` = campaign name
`utm_content` = variant, for A/B
`utm_term` = keyword, paid search only

Rules: all lowercase, hyphens not spaces, consistent forever. Inconsistent casing is the single most common way reporting breaks.

## Event tracking
Define events before building: name, trigger, properties. Use a consistent naming scheme (`object_action`: `signup_completed`, `demo_requested`). Don't track everything — track what maps to a decision.

## Attribution models
| Model | Credits | Best for |
|---|---|---|
| Last touch | Final click | Simple, biases to bottom-funnel |
| First touch | Initial click | Demand-gen evaluation |
| Linear | Split evenly | Long cycles |
| Time decay | Recent weighted | Short cycles |
| Data-driven | Modeled | Needs volume |

Say which model the numbers use. Two people arguing about channel performance are usually using different models.

## Dashboards
One decision per view. A dashboard nobody acts on is decoration. Separate the weekly glance (5-7 numbers, trended) from the deep-dive (drillable). Lead with the metric the team is paid on, not the one that looks best.

## Output
UTM conventions, tracking plans, dashboard specs → file (these become team reference docs). Quick checks and model explanations → inline.

## Tools
Build tagged URLs through the script so casing and separators can't drift, and
audit existing ones in bulk.

```bash
python3 scripts/utm.py build --url https://example.com/pricing \
  --source linkedin --medium cpc --campaign spring-launch --content hero-a

python3 scripts/utm.py check urls.txt
```

`check` catches the failure this file warns about: campaign names that differ
only by case or separator become separate rows in every report. It reports those
as drift, grouped by what they normalize to.

## Rules
- Distinguish measurable from attributable. Brand, word of mouth, and dark social drive conversions that never show in the data.
- Flag when tracking is set up in a way that will produce misleading numbers.
- Never present modeled or estimated figures as measured ones.
