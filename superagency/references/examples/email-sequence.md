# Example — Email Sequence

> **Illustrative only.** Company, product, and copy below are invented for shape. Never reuse the numbers, and treat the copy as a starting point, not finished work.

---

## Free-trial onboarding — Ledgerly (5 emails)

**Goal:** trial account completes its first reconciliation (the activation moment).
**Exit condition:** first reconciliation completed, OR trial expires, OR unsubscribes.
**Trigger:** account created, no reconciliation run within 24h.

### Flow summary
```
Day 0  Welcome + one next step ──► (ran a reconciliation?) ──► exit to "activated" track
Day 1  The 10-minute first close                │ no
Day 3  Case: how one team cut 6 days to 1       │ no
Day 5  "Stuck? reply and we'll set it up with you"
Day 7  Trial-ending nudge + how to extend
```
Branch on the activation event, not on opens. Anyone who activates leaves the
sequence immediately.

---

### Email 1 — Day 0 — Welcome
**Subject A:** Your Ledgerly trial is ready
**Subject B:** Start with one account, not all of them
**Preview:** The fastest first win is a single bank feed.

Body (~90 words): one paragraph on what to do first — connect one bank account
and run a reconciliation on last month. One link: **Connect an account.** No
feature tour.

### Email 2 — Day 1 — First close
**Subject A:** Your first reconciliation in about 10 minutes
**Subject B:** The 10-minute version of month-end
**Preview:** Skip the setup rabbit hole — here's the short path.

Body: the three steps to a first reconciliation, each one line. CTA repeats the
"Connect an account" link.

### Email 3 — Day 3 — Proof
**Subject A:** From a 6-day close to 1
**Subject B:** What changed for one finance team
**Preview:** Same team size. Different first week of the month.

Body: short customer story — the problem, the change, the outcome. Outcome names
a real number only if the customer has agreed to it being used; otherwise keep
it qualitative. CTA: **See how they set it up.**

### Email 4 — Day 5 — Offer help
**Subject A:** Want us to set it up with you?
**Subject B:** 15 minutes, screen shared, done
**Preview:** Reply to this email and we'll book a time.

Body (~60 words): plain-text feel, from a person. One ask: reply to book a
setup call.

### Email 5 — Day 7 — Trial ending
**Subject A:** Your trial ends in 2 days
**Subject B:** Keep your connected accounts
**Preview:** Here's what happens next, and how to keep going.

Body: what they'll lose access to, the link to add a plan, and a line that they
can reply to ask for a short extension.

---

### A/B test
One test: Email 1 subject line (A vs B above). Everything else stays fixed until
that resolves.

### Notes for the drafter
- One CTA per email; where a link repeats it's the *same* CTA, never a second ask.
- Urgency escalates — Email 1 has none, Email 5 has a deadline. Don't open at maximum.
- The exit condition is written down so nobody loops after they've activated.
