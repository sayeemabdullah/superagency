# Marketing Operations

Covers: martech stack, lead lifecycle and routing, MQL/SQL definitions, data hygiene, consent and preference management.

Often pairs with: `analytics.md` (ops runs the plumbing measurement reads from), `lifecycle.md` (ops encodes the stage transitions), `email-sequences.md` (ops owns the triggers).

## Lead lifecycle
Define the stages and the *entry criteria for each* before automating anything: anonymous → known → engaged → MQL → SQL → opportunity. A stage with a fuzzy definition produces the same marketing-vs-sales argument every quarter.

## Routing
Speed-to-lead beats routing sophistication. Route on the few fields that actually change ownership — territory, segment, named account — and alert a human. A fifty-branch rule tree nobody can debug fails silently.

## MQL / SQL definitions
Written, agreed with sales, reviewed on a schedule. The definition is a contract: what marketing commits to hand over, what sales commits to work. Score on fit *and* behaviour, not behaviour alone.

## Data hygiene
Normalise on entry — country, job title, company — rather than cleaning up later. Add dedupe rules, a bounce/unsubscribe suppression process, and a quarterly decay review. Bad data shows up as declining match rates and misrouted leads, not as an error.

## Stack
Every tool needs an owner and a reason it isn't a feature of something you already pay for. Integrations are where the stack breaks; map the data flow between systems before adding one.

## Consent
Marketing consent, preference centre, and suppression are legal infrastructure, not settings. Regional rules differ — get the requirements confirmed rather than assuming they carry across.

## Output
Lifecycle models, routing specs, MQL/SQL definitions, stack maps → file (the team operates from these). Quick "is this automation sane" checks → inline.

## Red flags
| Thought | Reality |
|---|---|
| "I'll set the MQL threshold at a score that seems reasonable." | The threshold is a contract with sales, not a number you pick. It gets agreed and reviewed, or it gets ignored. |
| "Build the routing to handle every edge case." | A rule tree nobody can debug fails silently. Route on the few fields that change ownership and alert a human. |
| "The data can be cleaned up later." | Cleanup-later never happens. Normalise on entry; decay surfaces as misrouted leads, not a warning. |
| "Consent can follow the same rules everywhere." | Consent and suppression are legal infrastructure and regional rules differ. Get the requirements confirmed. |

## Rules
- Define stage entry criteria and MQL/SQL in writing, agreed with sales, before automating the transitions.
- Prefer the simplest routing and scoring that works; complexity in ops fails quietly.
- Treat consent, preference, and suppression as legal requirements — flag for review rather than assuming rules carry across regions.
