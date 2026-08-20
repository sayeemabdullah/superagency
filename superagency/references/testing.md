# A/B Testing

Covers: test design, sample size, reading results.

Often pairs with: `cro.md` — it supplies what to test, this file supplies how.

## Designing a test
1. **Hypothesis** — "Changing X to Y will increase Z because [reason]." No reason = no learning, regardless of outcome.
2. **One variable** — headline OR button OR image. Multivariate needs traffic most teams don't have.
3. **Primary metric** — decided before launch. Picking it after is how you fool yourself.
4. **Sample size and duration** — calculate before starting. Run full weeks to avoid day-of-week skew.
5. **Stop condition** — pre-committed. Peeking and stopping at significance inflates false positives.

## Reading results
- Significance is not the same as meaningful. A 0.3% lift can be significant and worthless.
- Report the confidence interval, not just the point estimate.
- A "losing" test that teaches you something is a win. A flat test usually means the change was too small.
- Novelty effects fade — be cautious about big early lifts.

## What to test, in order of impact
Offer > headline/value prop > page structure > form length > CTA copy > design details. Most teams test the last one first.

## Output
Test plans → inline (hypothesis, variable, metric, duration, stop condition — five lines). A full experiment log or program doc → file.

## Rules
- Don't declare a winner on underpowered data. Say the test is inconclusive.
- Never run overlapping tests on the same funnel without accounting for interaction.
