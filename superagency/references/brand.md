# Brand Voice

*Template — fill in on first real use, then keep updating.*

## Profile

*Last updated: (date — refresh this line whenever the profile changes)*

### Audience
(Who? What do they already know/believe?)

### Tone (2-3 adjectives)
(e.g. direct, warm, no jargon)

### Voice do's
-

### Voice don'ts
- Avoid:
- Never claim:
- Banned words/phrases:

### Example on-brand line
(A sentence the user says "sounds like us")

---

## How to run a voice check

1. Compare the draft against the profile above.
2. Flag **specific lines** that drift — wrong tone, banned words, off-message claims, unsubstantiated superlatives. Not a vague overall verdict.
3. Give a before/after for each flagged line.
4. Note severity: blocking (legal/false claim), major (clearly off-voice), minor (nitpick).
5. If the profile is more than a few months old, ask whether it still holds before enforcing it strictly.
6. If the profile is still empty, say so and offer to build it from 3-5 examples the user considers on-brand, rather than guessing.

## Tools
Run a draft through the scorer before the manual read — it matches the banned
list above mechanically, so the voice check starts from evidence.

```bash
python3 scripts/readability.py draft.md --brand references/brand.md
```

It reports any banned word or phrase from this profile that appears in the
draft. A clean run is not a pass — tone and claims still need the human read
below.

## Red flags
| Thought | Reality |
|---|---|
| "The profile is empty but I can tell how they write." | You are guessing from one sample. Ask, or build it from examples they confirm are on-brand. |
| "Overall this reads off-brand." | That is unactionable. Quote the specific lines and give before/after. |
| "The banned-word scan came back clean, so the copy passes." | The scan only matches listed words. Tone, unsubstantiated claims, and off-message framing still need the read below. |

## Persisting the profile
This file resets to a blank template whenever the skill is re-uploaded — edits made here live only in the current conversation. After writing or changing a profile, print the complete file contents as **one fenced code block** and tell the user: *save this block and paste it back at the start of your next session.* No repackaging the skill. Say it every time you write — it is not obvious, and losing the profile is silent.

## How to build a profile from examples
Ask for 3-5 pieces they think sound right. Look for: sentence length, formality, use of "we" vs "you," humor, jargon tolerance, how they handle claims. Write the profile from patterns, then confirm with the user before saving.
