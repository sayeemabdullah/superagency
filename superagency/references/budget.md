# Budget & Planning

Covers: channel allocation, forecasting, business cases.

## Allocation approach
Start from the goal, not the budget. Work backwards:
target conversions → conversion rate → traffic needed → cost per visit → spend required.
If the math doesn't reach the goal, say so rather than distributing the shortfall quietly.

## Portfolio split
A common frame — adapt, don't apply blindly:
- ~70% proven channels
- ~20% scaling what's showing promise
- ~10% genuine experiments

Cutting the experimental slice is how teams end up with one channel and no options.

## Fixed vs variable
Separate committed costs (headcount, tools, retainers) from flexible spend (media). Only the second can be reallocated mid-quarter — this matters when someone asks to "move budget."

## Building a business case
Expected return, payback period, assumptions stated explicitly, and what happens if the key assumption is wrong. Give a range, not a single number.

## Ask before planning
Total budget, time horizon, and what current channels actually cost and return. Without the third, any allocation is a guess — label it as one.

## Output
Allocation plans and business cases → file, with an explicit assumptions table at the top. Quick gut-checks → inline.

## Tools
Work backwards with the script rather than in prose — it's a four-step chain and
a slipped decimal is invisible.

```bash
# does the budget on hand actually reach the goal?
python3 scripts/budget.py backsolve --target 3000 --conv-rate 0.02 --cpc 2.40 --budget 100000

python3 scripts/budget.py split --total 40000
python3 scripts/budget.py payback --cac 300 --arpu 50 --margin 0.8
```

When the budget falls short, `backsolve` reports the shortfall and what the
budget actually buys. Report that plainly — do not spread the gap across
channels to make the plan look fundable.

## Red flags
| Thought | Reality |
|---|---|
| "The budget is short, I'll spread the gap across channels." | Run `scripts/budget.py backsolve` and state the shortfall plainly. A quiet gap becomes someone's missed target. |
| "Blended CAC is the number to plan against." | It hides that SEO pays back over months and paid pays back immediately. Separate them. |
| "Media spend is the budget." | Production costs are real. So is the headcount that has to make the thing. |

## Rules
- Never present a forecast as a commitment. Label assumptions.
- Account for lag — SEO and content pay back over months; paid pays back immediately. A blended average hides this.
- Include the cost of production, not just media spend.
