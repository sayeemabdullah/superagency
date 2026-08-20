# BUILD.md — Superagency, from scratch

> Give this entire file to Claude and say: "Build this skill exactly as specified, then package it as a .skill file." Claude will create every file and hand back the packaged result.

This document is the complete specification for the Superagency skill. It exists so anyone who clones this repo can regenerate or fork the skill through Claude Chat, without Claude Code and without reading the source files one by one.

Final layout — the outer directory is the repo, the inner one is the skill folder. Claude.ai requires the skill folder at the root of the uploaded archive, so it must be self-contained and separate from repo files like the README.

```
superagency/
├── README.md
├── BUILD.md
├── LICENSE
├── .gitignore
├── superagency.skill
└── superagency/
    ├── SKILL.md
    └── references/
        ├── content.md
        ├── campaigns.md
        ├── brand.md
        ├── seo.md
        ├── email-sequences.md
        ├── paid.md
        ├── cro.md
        ├── competitive.md
        ├── pr.md
        ├── social.md
        ├── positioning.md
        ├── persona.md
        ├── analytics.md
        ├── testing.md
        ├── video.md
        ├── lifecycle.md
        ├── influencer.md
        ├── events.md
        ├── community.md
        ├── partnership.md
        ├── budget.md
        ├── creative-brief.md
        ├── crisis.md
        ├── reporting.md
        └── pulse-log.md
```

Package it with the skill folder at the archive root:

```bash
zip -r superagency.skill superagency/ -x "*.DS_Store" "*__pycache__*"
```

`unzip -l superagency.skill` should show paths beginning with `superagency/` — not `./superagency/` and not an absolute path. Claude.ai accepts both `.skill` and `.zip`; the `.skill` extension is just a renamed ZIP.

---

## Design principles — preserve these

Three decisions govern the architecture. Do not "improve" them.

### 1. Router architecture, not a monolith

Skills load in three stages:

| Stage | What loads | When |
|---|---|---|
| Metadata | `name` + `description` only | Always, every conversation |
| SKILL.md body | The router file | When the skill triggers |
| Reference files | One `.md` from `references/` | Only when that workflow is needed |

If all 24 workflows lived in SKILL.md, every request would load ~35,000 characters of mostly irrelevant instruction. Instead SKILL.md is a ~70-line routing table that points to one reference file per request.

Keep SKILL.md under 500 lines. New workflows get a new reference file plus a routing table row — never inline content in the router.

### 2. The description field is the entire trigger mechanism

Claude decides whether to use a skill based *only* on the YAML `description`. The body is invisible until after that decision. Claude also tends to under-trigger skills, so the description here is deliberately broad and slightly pushy: it names all 24 domains, then adds natural-language examples of how people actually phrase requests.

Any workflow not named in the description will never fire.

### 3. Guardrails are encoded, not assumed

Marketing work has predictable failure modes: invented statistics, fabricated customer quotes, competitor claims stated as fact, legal exposure from unsubstantiated superlatives, and confidently outdated advice about platforms that change monthly. The skill encodes standing rules against all of these. Each reference file ends with a "Rules" section covering its domain's specific failure mode. Preserve every one.

---

## Two stateful files

Most reference files are read-only instruction. Two are meant to be written to:

- **`brand.md`** ships as a blank template. On first customer-facing use, the skill asks the user for audience, tone adjectives, and things to avoid, then saves the answers. Every later request reads from it.
- **`pulse-log.md`** accumulates weekly metric summaries so `/trend` can compare across weeks and months rather than looking at one week in isolation.

Both ship intentionally empty. Do not populate them with sample data.

---

## Extending it

To add a workflow:

1. Write `references/<name>.md` — scope line, structure or checklist, then a "Rules" section covering that domain's failure mode.
2. Add a row to the routing table in `SKILL.md`.
3. Add the slash command to the command list.
4. **Add the domain to the `description` field.** This is the step people forget, and skipping it means the workflow never triggers.
5. Repackage and re-upload.

To trim: after a few weeks of real use, delete reference files that never get routed to. Anthropic's guidance favors focused skills over one that does everything, so treat 24 workflows as a ceiling rather than a target — a tighter skill routes more accurately.

---

# FILE CONTENTS

Everything below is verbatim. Each block is one file.

---

### File: `.gitignore`

````
.DS_Store
__pycache__/
*.pyc
.env
node_modules/
````

---

### File: `superagency/SKILL.md`

````markdown
---
name: superagency
description: Full-stack marketing agency skill covering content, campaigns, brand voice, SEO, email sequences, paid ads, landing pages and CRO, competitive research, PR, social, positioning, personas, analytics and attribution, A/B testing, video and short-form, lifecycle and retention, influencer marketing, events and webinars, community, partnerships, budget planning, creative briefs, crisis comms, and performance reporting. Use this whenever the user asks for anything marketing-related — writing copy, planning a launch, auditing SEO, building a nurture flow, checking brand voice, researching competitors, drafting a press release, scripting a video, planning spend, or summarizing metrics — even if they never say the word "marketing" (e.g. "write a LinkedIn post," "why isn't our page ranking," "how do we stop churn," "someone's angry at us on Twitter," "how did we do this week").
---

# Superagency

A full marketing team in one skill. Route the request to the right workflow, read only that reference file, then execute.

## Routing table

| User is asking about | Read this |
|---|---|
| Writing posts, blogs, emails, ads, case studies | `references/content.md` |
| Campaign briefs, launches, content calendars | `references/campaigns.md` |
| Brand voice, tone, "does this sound like us" | `references/brand.md` |
| SEO, rankings, keywords, site audits | `references/seo.md` |
| Nurture flows, drip campaigns, onboarding emails | `references/email-sequences.md` |
| Google/Meta/LinkedIn/TikTok ads, paid spend | `references/paid.md` |
| Landing pages, conversion rate, funnel drop-off | `references/cro.md` |
| Competitors, battlecards, white space | `references/competitive.md` |
| Press releases, media pitches, announcements | `references/pr.md` |
| Social cadence, content pillars, platform strategy | `references/social.md` |
| Value props, messaging frameworks, taglines | `references/positioning.md` |
| ICP, buyer personas, jobs-to-be-done | `references/persona.md` |
| UTMs, event tracking, attribution models | `references/analytics.md` |
| A/B tests, experiment design, reading results | `references/testing.md` |
| YouTube, Reels, TikTok scripts, hooks, titles | `references/video.md` |
| Onboarding, activation, churn, expansion | `references/lifecycle.md` |
| Creators, sponsorships, influencer outreach | `references/influencer.md` |
| Webinars, conferences, trade shows | `references/events.md` |
| Slack/Discord/forum community strategy | `references/community.md` |
| Co-marketing, affiliates, referral programs | `references/partnership.md` |
| Channel allocation, forecasting, business cases | `references/budget.md` |
| Briefing designers, agencies, freelancers | `references/creative-brief.md` |
| Backlash, negative press, outages, complaints | `references/crisis.md` |
| Weekly/monthly metrics, wins and misses | `references/reporting.md` |

If a request spans several (e.g. "plan our launch" touches campaigns + content + social + PR), start with the primary one and pull others in only as needed. Never read all of them.

## Slash commands

`/draft` `/campaign` `/voice` `/brand` `/seo` `/sequence` `/ads` `/cro` `/compete` `/pr` `/social` `/position` `/persona` `/analytics` `/test` `/video` `/lifecycle` `/influencer` `/event` `/community` `/partner` `/budget` `/brief` `/crisis` `/pulse` `/trend`

`/pulse` and `/trend` both use `references/reporting.md`.

## Always do this first

1. **Check `references/brand.md`.** If the profile is empty and the request is customer-facing, ask 2-3 quick questions (audience, tone adjectives, things to avoid) and save the answers there. Skip for internal or quick asks.
2. **Search the web when the task depends on current facts** — competitor moves, SEO practice, ad specs, platform algorithms, creator rates, disclosure law. Don't answer from memory on anything that changes.
3. **Ask for inputs that materially change the output** (budget, timeline, audience) rather than inventing them. One question, not five.

## Standing rules across all workflows

- **Never fabricate** statistics, customer quotes, results, testimonials, or attributed statements. If a number would strengthen the work, flag where the user must supply it.
- **Flag claims needing substantiation** — superlatives, comparative claims, health/financial/safety results — and say when something needs legal sign-off rather than drafting around it.
- **Distinguish evidence from hypothesis.** Label anything built without data as something to validate.
- **Offer 2-3 variants** for headlines, subject lines, and taglines. These get chosen, not accepted.
- **Prioritize by impact ÷ effort.** Don't hand over an unranked list of forty items.

## Output conventions

| Type | Format |
|---|---|
| Short copy (captions, subject lines, taglines) | Inline in chat |
| Standalone deliverables (blogs, releases, briefs, audits) | File |
| Reviews and checks (voice, CRO, competitive) | Inline, specific annotated list |
| Weekly pulse | Inline, copy-pasteable into Slack or email |
````

---

### File: `superagency/references/content.md`

````markdown
# Content Drafting

Covers: blog posts, social captions, email copy, landing page copy, ad copy, case studies, newsletters.

## Before writing
- Confirm channel and goal (awareness, clicks, signups, replies). If not stated and it changes the copy, ask.
- Check `brand.md` for tone.
- Know the audience's current belief — good copy changes a mind, it doesn't just describe a product.

## Channel norms
| Channel | Length | Notes |
|---|---|---|
| LinkedIn | 150-300 words | Hook in line 1, before the "see more" cut. Line breaks, not paragraphs. |
| X/Twitter | Under 280 or a thread | First post must stand alone. |
| Instagram caption | 100-200 words | Front-load; CTA at end. |
| Email subject | Under 60 chars | Under 40 is safer on mobile. |
| Email body | 100-250 words | One CTA, repeated at most twice. |
| Blog post | 800-1500 words | Hook first sentence, subheads every 200-300 words, scannable. |
| Landing page hero | 5-12 words headline | Benefit, not feature. |
| Case study | 500-900 words | Problem → approach → result, with a real number in the result. |

## Rules
- Lead with the benefit, not the feature.
- Cut adjectives that survive deletion. "Powerful, innovative solution" says nothing.
- One idea per piece. If there are three, write three pieces.
- Never invent statistics, customer quotes, or results. If a number would strengthen it, flag where the user needs to supply one.
- Offer 2-3 headline/subject variants with a one-line note on what each optimizes for.

## Output
Standalone pieces (blog posts, case studies, newsletters) → file. Single captions or subject lines → inline.
````

---

### File: `superagency/references/campaigns.md`

````markdown
# Campaign Planning

Covers: launches, lead-gen pushes, awareness campaigns, seasonal pushes, multi-week initiatives.

## Campaign brief structure
1. **Objective & primary metric** — one metric, not five. "3,000 signups by Nov 30," not "increase awareness."
2. **Audience** — who, and what they currently believe or do.
3. **Core message** — one sentence describing what changes in the audience's mind.
4. **Channels** — which, and *why those*. Justify each; a channel with no rationale gets cut.
5. **Timeline / calendar** — week-by-week or day-by-day, with dependencies noted (design assets due before social starts, legal review before PR).
6. **Budget** — if given. If not and it's a paid campaign, ask.
7. **Risks & open questions** — what could derail this, what's still unknown.

Keep to one page unless more depth is requested.

## Content calendar format
Table with: date | channel | asset | owner | status | dependency

Flag any item whose dependency lands after its own due date — that's the most common way calendars break.

## Launch-specific
Add a phased structure: pre-launch (tease, waitlist), launch day (announcement across all channels same day), post-launch (proof, testimonials, case studies). Most launches under-invest in post-launch.

## Ask before planning
Timeline, budget, and whether there's a hard date. These three change the plan more than anything else.

## Output
Campaign brief → markdown file (these get shared and saved).
````

---

### File: `superagency/references/brand.md`

````markdown
# Brand Voice

*Template — fill in on first real use, then keep updating.*

## Profile

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
5. If the profile is still empty, say so and offer to build it from 3-5 examples the user considers on-brand, rather than guessing.

## How to build a profile from examples
Ask for 3-5 pieces they think sound right. Look for: sentence length, formality, use of "we" vs "you," humor, jargon tolerance, how they handle claims. Write the profile from patterns, then confirm with the user before saving.
````

---

### File: `superagency/references/seo.md`

````markdown
# SEO

Covers: audits, keyword research, on-page optimization, content gaps, technical checks.

## Search first
SEO changes constantly — algorithm updates, SERP feature shifts, AI overview impact. Web-search for current best practice before giving advice that depends on how search works *today*. Don't answer from memory on ranking factors.

## Audit structure
1. **Keyword opportunities** — terms with real intent match, grouped by funnel stage (informational / commercial / transactional). Note rough difficulty.
2. **On-page** — title tags (under ~60 chars), meta descriptions (~155), H1 uniqueness, heading hierarchy, internal links, image alt text.
3. **Content gaps** — topics competitors rank for that the user doesn't cover. This is usually the biggest win.
4. **Technical** — page speed, mobile usability, crawlability, broken links, duplicate content, sitemap/robots.txt, structured data.
5. **Competitor comparison** — who's ranking for the target terms and why.

## Deliverable
Split recommendations into:
- **Quick wins** — under a day of work, meaningful impact (fix title tags, add internal links, update thin pages)
- **Strategic** — weeks of work (new content clusters, site architecture, backlink campaigns)

Prioritize by impact ÷ effort. Don't hand over an unranked list of 40 items.

## Rules
- Never promise rankings or timelines. SEO outcomes aren't guaranteeable.
- Write for the reader first; keyword-stuffed copy loses on both fronts now.
- If asked to audit a live site, fetch the actual pages rather than assuming what's on them.
````

---

### File: `superagency/references/email-sequences.md`

````markdown
# Email Sequences

Covers: onboarding, nurture, re-engagement, win-back, launch sequences, abandoned cart.

## Sequence design
For each sequence, define:
- **Goal & exit condition** — what action ends the sequence (they convert, they reply, they unsubscribe)
- **Trigger** — what enrolls someone
- **Cadence** — day 0, day 2, day 5... don't default to daily
- **Branching** — what happens on open vs no-open, click vs no-click

## Typical shapes
| Type | Length | Cadence |
|---|---|---|
| Onboarding | 4-6 emails | Day 0, 1, 3, 7, 14 |
| Nurture | 5-8 emails | Weekly |
| Re-engagement | 3 emails | Day 0, 4, 10 — last one is the "should we stop emailing you" |
| Win-back | 3-4 emails | Day 0, 7, 21 |
| Launch | 4-5 emails | Tease, announce, proof, urgency, last call |

## Per-email requirements
Subject line (2-3 variants), preview text, body, one primary CTA. Preview text is wasted by most senders — use it as a second subject line, not a repeat.

## Rules
- One CTA per email. Two links to the same CTA is fine; two different asks is not.
- Escalate urgency across the sequence, don't open at maximum.
- Include the exit condition explicitly so people don't get stuck in loops.
- Suggest one A/B test per sequence, usually the first subject line.

## Output
Full sequence → file, with a flow summary at the top showing the branching.
````

---

### File: `superagency/references/paid.md`

````markdown
# Paid Ads

Covers: Google, Meta, LinkedIn, X, TikTok ad copy and strategy.

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

## Rules
- Never promise specific CPA/ROAS figures.
- Flag any claim in ad copy that would need substantiation (superlatives, comparative claims, health/financial results).
````

---

### File: `superagency/references/cro.md`

````markdown
# Landing Pages & Conversion

Covers: landing page reviews, funnel drop-off, conversion rate improvement.

## Page review checklist
1. **Above the fold** — is the value prop clear in 5 seconds? Headline states the benefit, not the category.
2. **Message match** — does the page deliver what the ad/email/link promised? Mismatch kills conversion faster than anything.
3. **Single conversion goal** — competing CTAs split attention. Nav links on a landing page are usually leaks.
4. **Friction** — form field count (every field costs conversions), required account creation, unclear pricing.
5. **Proof** — testimonials, logos, numbers, guarantees. Placed near the CTA, not buried.
6. **Objection handling** — what stops someone from converting, and is it addressed on the page?
7. **Mobile** — most traffic. Check the CTA is reachable without scrolling past three screens.

## Funnel diagnosis
When conversion is down, isolate *where*: traffic quality, page bounce, form start, form completion, or post-submit. Each has a different fix. Ask for the step-by-step numbers rather than guessing.

## Rules
- Recommend one change at a time if they're testing; simultaneous changes make results unreadable.
- Prioritize by expected impact — headline and offer beat design tweaks nearly every time.
- Don't cite conversion-rate benchmarks as fact without a source; they vary wildly by industry.
````

---

### File: `superagency/references/competitive.md`

````markdown
# Competitive Research

Covers: competitor briefs, battlecards, positioning gaps.

## Always search
Competitor positioning, pricing, and messaging change constantly. Web-search and fetch their actual pages. Never write a competitive brief from memory.

## Brief structure
For each competitor:
- **Positioning** — how they describe themselves in their own words (paraphrased)
- **Target segment** — who they're clearly built for
- **Pricing model** — if public
- **Messaging pillars** — the 2-3 things they repeat
- **Strengths** — honestly stated
- **Weaknesses / gaps** — where they're vulnerable

Then across all of them:
- **White space** — angles nobody has claimed. This is the point of the exercise.
- **Threats** — where they're moving that affects the user

## Battlecard format
For sales use: their pitch → our counter → proof point. Keep each to one line. A battlecard nobody can read in 30 seconds doesn't get used.

## Rules
- Stay factual and fair. Don't write disparaging claims that can't be substantiated — it's a legal risk in comparative marketing.
- Distinguish what's verified from what's inferred.
- If a competitor's claim can't be confirmed, say so rather than repeating it as fact.
````

---

### File: `superagency/references/pr.md`

````markdown
# PR & Press

Covers: press releases, media pitches, announcements, bylines.

## Press release structure
- **Headline** — the news, plainly. Not a tagline.
- **Dateline + lede** — who, what, when, where, why in the first sentence
- **Body** — supporting detail, most newsworthy first (inverted pyramid)
- **Quote** — from a named executive. One good quote beats three bland ones.
- **Boilerplate** — company description
- **Contact**

Keep to 400-600 words.

## Media pitch
Short. Subject line is the whole game. 3-4 sentences: why this matters to *their* readers, the news, the offer (interview, exclusive, data). Never send the release as the pitch.

## Rules
- Is it actually news? Funding, launches, major hires, data, partnerships are. Feature updates usually aren't.
- Never fabricate quotes. Draft a quote for a real named person to approve, and label it clearly as a draft for approval.
- Never attribute invented statements to real people outside the user's own company.
- Flag anything that needs legal or exec sign-off before it goes out.
````

---

### File: `superagency/references/social.md`

````markdown
# Social Strategy

Covers: posting cadence, platform mix, content pillars, community.

## Content pillars
Define 3-4 recurring themes, so posting isn't invented weekly. Typical mix:
- Educational (teach something)
- Proof (customers, results, behind-the-scenes)
- Point of view (opinion, industry take)
- Promotional (the actual ask) — keep this the smallest slice

## Cadence by platform
| Platform | Realistic cadence | Notes |
|---|---|---|
| LinkedIn | 3-5x/week | Best organic reach for B2B right now — verify with a search |
| X | Daily+ | High volume, short shelf life |
| Instagram | 3-4x/week + stories | Visual-first; captions support, don't lead |
| TikTok/Reels | 3-5x/week | Volume and hooks beat production quality |
| YouTube | Weekly or biweekly | High effort, long shelf life |

Don't recommend all platforms. Pick 1-2 where the audience actually is and do those well.

## Calendar output
Table: date | platform | pillar | hook | asset needed | status

## Rules
- Repurpose deliberately — one blog post becomes five social posts, not five original ideas.
- Verify current platform behavior with a search before advising on algorithm or format specifics.
````

---

### File: `superagency/references/positioning.md`

````markdown
# Positioning & Messaging

Covers: value props, messaging frameworks, taglines, category definition.

## Positioning statement
"For [audience] who [need], [product] is a [category] that [key benefit]. Unlike [alternative], we [differentiator]."

Fill this in before writing any copy. Most bad marketing is a positioning problem wearing a copy costume.

## Messaging hierarchy
1. **Core message** — one sentence, the thing you'd want remembered
2. **Pillars** — 3 supporting themes
3. **Proof points** — evidence under each pillar (numbers, customers, features)

Every piece of copy should map to a pillar. If it doesn't, it's noise.

## Value prop rules
- Benefit over feature: what changes for the user
- Specific over broad: "cut invoice processing from 3 days to 20 minutes" beats "boost efficiency"
- Differentiated: if a competitor could put their logo on it, it's not positioning

## Taglines
Offer 5-8 options across different angles (benefit, emotional, category, contrarian), with a one-line note on what each does. Taglines are chosen, not accepted.

## Rules
- Ask what the alternative is — including "do nothing," which is the most common competitor.
- Don't invent customer benefits the product doesn't deliver.
````

---

### File: `superagency/references/persona.md`

````markdown
# Personas & ICP

Covers: ideal customer profile, buyer personas, jobs-to-be-done.

## ICP (company-level, B2B)
- Industry / vertical
- Company size (employees, revenue)
- Geography
- Tech stack or operating model signals
- Trigger events that create the need (funding, new hire, regulation, growth threshold)
- Disqualifiers — who looks like a fit but isn't

## Persona (person-level)
- Role and seniority
- What they're measured on — this drives everything
- Jobs to be done: functional, emotional, social
- Pains and current workarounds
- Where they learn (publications, communities, people they follow)
- Buying role: user, champion, economic buyer, blocker
- Objections they raise

## Rules
- Build from evidence — sales calls, support tickets, interviews, analytics. Ask what the user has before inventing.
- If there's no data, label it explicitly as a hypothesis to validate, not a finding.
- Two or three personas maximum. More than that and nobody uses them.
- Skip demographics that don't change the messaging. Age and hobbies usually don't.
````

---

### File: `superagency/references/analytics.md`

````markdown
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

## Rules
- Distinguish measurable from attributable. Brand, word of mouth, and dark social drive conversions that never show in the data.
- Flag when tracking is set up in a way that will produce misleading numbers.
- Never present modeled or estimated figures as measured ones.
````

---

### File: `superagency/references/testing.md`

````markdown
# A/B Testing

Covers: test design, sample size, reading results.

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

## Rules
- Don't declare a winner on underpowered data. Say the test is inconclusive.
- Never run overlapping tests on the same funnel without accounting for interaction.
````

---

### File: `superagency/references/video.md`

````markdown
# Video & Short-Form

Covers: YouTube, Reels, TikTok, Shorts — scripts, hooks, titles, thumbnails.

## Short-form script structure
- **0-2s hook** — the entire game. State the payoff or create an open loop. No logos, no "hey guys."
- **2-15s setup** — why this matters to them
- **Body** — deliver, fast. Cut every pause.
- **End** — CTA or loop back to the hook

Write scripts as spoken lines plus on-screen text cues, not prose paragraphs.

## Hook patterns
- Contrarian: "Everyone tells you X. That's wrong."
- Result-first: "This took our CPA from $80 to $12."
- Question the viewer is already asking
- Visual surprise in frame one

## YouTube long-form
- Title: under ~60 chars, benefit or curiosity, keyword early
- Thumbnail: one focal point, readable at phone size, doesn't repeat the title text
- First 30 seconds decide retention — state what they'll get, then start
- Chapters for anything over 8 minutes

## Rules
- Search for current format specs and aspect ratios before advising — these change.
- Retention beats production value. A well-hooked phone video outperforms a polished one that opens slowly.
- Don't write scripts that require b-roll or resources the user hasn't said they have.
````

---

### File: `superagency/references/lifecycle.md`

````markdown
# Lifecycle & Retention

Covers: onboarding, activation, churn prevention, expansion, win-back.

## Lifecycle stages
| Stage | Goal | Typical lever |
|---|---|---|
| Activation | Reach first value fast | Onboarding flow, guided setup |
| Adoption | Habit formation | Feature nudges, use-case education |
| Retention | Keep the habit | Value reminders, check-ins |
| Expansion | Grow account | Usage-triggered upsell |
| Win-back | Recover churned | Re-engagement offer |

## Define the activation moment
The specific action correlated with retention (sent first invoice, invited a teammate, hit 3 sessions). Everything in onboarding should drive toward it. If the user doesn't know theirs, that's the first thing to find.

## Churn signals
Declining usage, dropped seats, support escalations, unrenewed integrations, champion leaves. Trigger intervention on signal, not on renewal date.

## Rules
- Segment by behavior, not tenure. A power user at month 1 needs different messaging than a dormant user at month 12.
- Don't message every user the same thing — that's what makes lifecycle email feel like spam.
- Expansion asks should follow evidence of value, never precede it.
````

---

### File: `superagency/references/influencer.md`

````markdown
# Influencer & Creator Marketing

Covers: sourcing, outreach, briefs, measurement.

## Sourcing
Fit over follower count. Evaluate:
- Audience overlap with your ICP — ask for their audience demographics
- Engagement rate, not reach (comments > likes as a quality signal)
- Content quality and brand safety — review their last 20 posts
- Prior sponsorships — how many, and did they feel forced

Micro-creators (10k-100k) usually outperform on cost-per-engagement.

## Outreach
Short, specific, shows you've watched their work. Name the post you liked and why. Lead with what's in it for them and their audience, not your product features. Include: what you're proposing, rough compensation range, timeline.

## Brief
Give them: the message and non-negotiables, and nothing else. Over-scripting is the top cause of flat creator content — their audience can hear it. Specify: required disclosure, banned claims, key message, timeline, deliverables, usage rights.

## Rules
- Disclosure is legally required (FTC in the US, ASA in the UK, and equivalents elsewhere). Search for current rules in the relevant jurisdiction — don't state them from memory.
- Never suggest hiding a paid relationship.
- Agree usage rights up front — whether you can run their content as paid ads changes the price.
- Rate benchmarks vary enormously; search rather than quoting figures from memory.
````

---

### File: `superagency/references/events.md`

````markdown
# Events & Webinars

Covers: webinars, conferences, trade shows, meetups.

## Timeline (webinar)
- **4 weeks out** — topic, speakers, registration page live
- **3 weeks** — first promo push (email, social)
- **2 weeks** — partner/speaker amplification
- **1 week** — reminder + agenda detail
- **Day of** — 1hr reminder, "we're live" post
- **Day after** — recording to all registrants (attendees and no-shows get different emails)
- **Week after** — repurpose into clips, blog post, sequence

Registration-to-attendance runs low for free webinars — plan promo volume for that, and treat no-shows as a real audience segment, not a loss.

## Conference / trade show
- Pre-show: book meetings *before* arriving. Booth traffic alone rarely justifies cost.
- On-site: capture leads with context, not just badge scans. A note on what they asked about doubles follow-up quality.
- Post-show: follow up within 48 hours while memory is fresh, segmented by conversation depth.

## Measurement
Registrations, attendance rate, engaged minutes, pipeline sourced, cost per opportunity. Attendance alone isn't a result.

## Rules
- The follow-up is worth more than the event. Budget effort accordingly.
- Repurpose every event into at least three other assets.
````

---

### File: `superagency/references/community.md`

````markdown
# Community

Covers: Slack/Discord/forum strategy, engagement, advocacy.

## Before starting one
Ask why it should exist. Communities that exist "for marketing" die. Valid reasons: members get value from each other, support deflection, product feedback loop, advocacy.

Also ask who runs it. An unstaffed community is worse than none — an empty channel is negative signal.

## Getting to critical mass
- Seed with 20-50 engaged people before opening broadly
- Post daily in the early weeks; silence is fatal
- Answer every question fast, even badly
- Highlight member contributions publicly — that's what converts lurkers

## Engagement loops
Recurring rituals beat one-off events: weekly threads, member spotlights, office hours, AMAs. Predictability builds habit.

## Health metrics
Active members (not total), member-to-member replies vs staff replies (the key ratio), retention of new joiners past 30 days, questions answered by members.

## Rules
- Set and enforce guidelines early. Moderation debt compounds.
- Don't promote heavily in your own community — it's the fastest way to kill it.
````

---

### File: `superagency/references/partnership.md`

````markdown
# Partnerships & Co-Marketing

Covers: co-marketing, affiliates, integrations, referrals.

## Evaluating a partner
- Audience overlap without direct competition
- Comparable audience size — lopsided partnerships stall
- Credible brand fit
- Willing to actually promote, with a named owner on their side

## Co-marketing formats
Joint webinar, co-authored report, integration announcement, bundled offer, newsletter swap, guest content exchange.

Define up front: who creates what, who promotes when, who owns the leads, and how leads are shared. Lead ownership is where most co-marketing collapses.

## Affiliate / referral programs
- Commission structure and cookie window
- Approved messaging and banned claims
- Payout terms and threshold
- Tracking method
- Disclosure requirements — same legal rules as influencer marketing

## Rules
- Get commitments in writing, including promotion dates.
- Measure per partner, not in aggregate; one partner usually drives most of the result.
- Don't let a partner make claims about your product you haven't approved.
````

---

### File: `superagency/references/budget.md`

````markdown
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

## Rules
- Never present a forecast as a commitment. Label assumptions.
- Account for lag — SEO and content pay back over months; paid pays back immediately. A blended average hides this.
- Include the cost of production, not just media spend.
````

---

### File: `superagency/references/creative-brief.md`

````markdown
# Creative Briefs

Covers: briefs for designers, agencies, freelancers, video teams.

## Brief structure
1. **Project & deliverables** — exact formats, sizes, quantities
2. **Objective** — what this needs to achieve
3. **Audience** — who sees it, in what context
4. **Single message** — one thing. If there are three, the work will be muddy.
5. **Mandatories** — logo, legal, disclaimers, brand rules
6. **Tone & references** — examples of what's right, and what's wrong
7. **Constraints** — budget, timeline, technical limits
8. **Approval process** — who signs off, how many rounds
9. **Deadline** — with milestones, not just a final date

## Rules
- Brief the problem, not the solution. Prescribing execution wastes the creative's value.
- Include what's *not* wanted — it saves a round.
- Name one decision-maker. Committee feedback produces committee work.
- Reference examples do more than adjectives. "Clean and modern" means nothing; a link means something.
````

---

### File: `superagency/references/crisis.md`

````markdown
# Crisis & Issues Response

Covers: negative press, social backlash, outages, product failures.

## First: assess severity
- **Low** — isolated complaint. Respond directly, don't amplify.
- **Medium** — spreading, multiple voices. Prepare a statement, monitor.
- **High** — press coverage, safety/legal/data implications. Involve leadership and legal before responding publicly.

Do not escalate a low-severity issue by responding at high-severity volume.

## Response principles
- Speed matters, but accuracy matters more. "We're looking into this and will update by [time]" is a valid first response.
- Acknowledge, don't deflect. Non-apologies read as worse than silence.
- Say what you know, what you don't, and what you're doing.
- One channel as source of truth; point everything else there.
- Update on the schedule you promised, even if there's nothing new.

## Do not
- Argue with critics publicly
- Delete criticism (unless it violates policy) — it always resurfaces
- Speculate on cause before you know
- Let marketing speak for legal or security matters

## Rules
This skill drafts holding statements and comms plans. Anything touching legal liability, data breaches, safety, or regulatory exposure must go to counsel before publication — say so explicitly rather than drafting around it.
````

---

### File: `superagency/references/reporting.md`

````markdown
# Performance Reporting

Covers: weekly pulse, monthly/quarterly reviews, trend summaries.

## Weekly pulse
1. Get the numbers — pasted, or from a connected source if one's available. Check before asking the user to paste.
2. **Top 3 wins** and **top 3 misses** — specific metrics with numbers, not vague statements.
3. **Anomalies** — sharp jumps or drops flagged separately, even if not top-3.
4. **One recommended action** for next week. One, not five.
5. **Trend** — compare to `pulse-log.md` if prior entries exist. Note direction, not just this week's raw number.
6. Append this week's summary to `pulse-log.md`.
7. Format: ask Slack-style (short, scannable) or email-style (fuller, with greeting) if unclear.

## Monthly / quarterly review
Adds: goal attainment vs target, channel-by-channel breakdown, spend efficiency, and next-period priorities. Narrative over dashboard — say what happened and why, not just what the numbers were.

## Rules
- Don't report metrics without context. "1,200 clicks" means nothing; "1,200 clicks, up 40% on a flat budget" means something.
- Distinguish correlation from cause. If traffic rose the same week as a campaign *and* a press mention, say both.
- Call out metrics that look good but aren't (impressions up, conversions flat).
- Never fabricate numbers the user didn't provide.
````

---

### File: `superagency/references/pulse-log.md`

````markdown
# Weekly Pulse Log

*Each entry: date range, wins, misses, action taken. Append new entries at the bottom.*

<!-- No entries yet -->
````

---

### File: `README.md`

*Substitute the user's GitHub username for YOUR-USERNAME.*

`````markdown
# Superagency

A Claude Skill that acts as a full marketing team — 24 workflows covering content, campaigns, SEO, paid ads, email, conversion, PR, competitive research, lifecycle, analytics, and more.

Ask Claude a marketing question in plain language and it routes to the right workflow automatically. No prompt engineering, no re-explaining your context every time.

---

## What it does

| Command | Workflow | Covers |
|---|---|---|
| `/draft` | Content | Blogs, social, email, ads, case studies — with per-channel length norms |
| `/campaign` | Campaign planning | Briefs, content calendars, launch phasing, dependency checks |
| `/voice` | Brand check | Flags off-voice lines with before/after fixes and severity levels |
| `/brand` | Brand profile | Builds your voice profile from examples you consider on-brand |
| `/seo` | SEO | Keywords, on-page, content gaps, technical — split into quick wins vs strategic |
| `/sequence` | Email flows | Onboarding, nurture, re-engagement, win-back, launch — with branching logic |
| `/ads` | Paid | Google, Meta, LinkedIn, TikTok copy + creative testing strategy |
| `/cro` | Conversion | Landing page teardowns, funnel drop-off diagnosis |
| `/compete` | Competitive | Battlecards, positioning gaps, white-space analysis |
| `/pr` | Press | Releases, media pitches, announcements |
| `/social` | Social | Content pillars, platform cadence, calendars |
| `/position` | Positioning | Value props, messaging hierarchy, taglines |
| `/persona` | Personas | ICP definition, buyer personas, jobs-to-be-done |
| `/analytics` | Tracking | UTM conventions, event naming, attribution models |
| `/test` | Experiments | A/B test design, sample size, reading results honestly |
| `/video` | Video | YouTube, Reels, TikTok scripts, hooks, titles, thumbnails |
| `/lifecycle` | Retention | Activation, churn signals, expansion, win-back |
| `/influencer` | Creators | Sourcing, outreach, briefs, disclosure requirements |
| `/event` | Events | Webinars, conferences, promo timelines, follow-up |
| `/community` | Community | Slack/Discord strategy, engagement loops, health metrics |
| `/partner` | Partnerships | Co-marketing, affiliates, lead-sharing agreements |
| `/budget` | Planning | Channel allocation, forecasting, business cases |
| `/brief` | Creative briefs | Briefs for designers, agencies, freelancers |
| `/crisis` | Issues response | Severity assessment, holding statements, escalation |
| `/pulse` | Weekly report | Wins, misses, anomalies, one recommended action |
| `/trend` | Trend summary | Month/quarter rollup from your saved pulse history |

You don't have to use the slash commands — describing the task works too. "Why isn't our pricing page ranking?" routes to SEO. "Someone's complaining about us on Twitter" routes to crisis.

---

## Install

**Requirements:** any Claude plan (Free, Pro, Max, Team, Enterprise) with **Code execution and file creation** enabled.

### 1. Enable code execution

Go to **Settings → Capabilities** and turn on **Code execution and file creation**.

> If the Skills menu is missing or greyed out, this is almost always why — it's not a plan limitation. On Team and Enterprise plans, an owner may need to enable it at the organization level.

### 2. Get the skill file

**Option A — download the packaged file**

Download `superagency.skill` from this repo (or from [Releases](../../releases)).

**Option B — have Claude build it**

Download `BUILD.md`, paste it into a Claude conversation, and say:

> Build this skill exactly as specified, then package it as a .skill file.

Claude will create all 25 files and hand you the packaged result. This route is useful if you want to edit the spec first — swap in your own channel norms, drop workflows you don't need, add ones you do.

**Option C — clone and zip it yourself**

```bash
git clone https://github.com/YOUR-USERNAME/superagency.git
cd superagency
zip -r superagency.zip superagency/
```

The `superagency/` folder must be at the root of the archive.

### 3. Upload to Claude

1. Go to **Customize → Skills** ([claude.ai/customize/skills](https://claude.ai/customize/skills))
2. Click **+** → **Create skill** → **Upload a skill**
3. Select the `.skill` or `.zip` file
4. Toggle it on

### 4. Start a new conversation

Skills load at session start, so an already-open chat won't pick it up.

Test it with something real:

```
Write a LinkedIn post announcing our new pricing tier.
```

---

## First run

The first time you ask for anything customer-facing, the skill will ask three quick questions:

- Who's the audience?
- Two or three adjectives for how the brand should sound
- Anything to avoid — banned words, competitor names, compliance lines

It saves your answers to `references/brand.md` and uses them from then on. You only do this once.

For weekly reporting, `/pulse` appends each week's summary to `references/pulse-log.md`, so after a month or so `/trend` can tell you what's actually moving rather than just what happened last week.

---

## How it's built

```
superagency/
├── SKILL.md              # ~70-line router: frontmatter, routing table, standing rules
└── references/
    ├── content.md
    ├── campaigns.md
    ├── brand.md          # stateful — stores your voice profile
    ├── ...
    └── pulse-log.md      # stateful — accumulates weekly metrics
```

Skills load in three stages: the `description` is always in context, the SKILL.md body loads when the skill triggers, and reference files load only when needed. Putting all 24 workflows in one file would mean loading ~35,000 characters of mostly-irrelevant instructions on every request.

So `SKILL.md` is just a routing table. Ask about SEO, it reads `references/seo.md` and nothing else.

`BUILD.md` documents the full architecture and design reasoning if you want to fork or extend it.

---

## What it won't do

These constraints are deliberate, not oversights:

- **Won't invent numbers.** No fabricated statistics, customer quotes, testimonials, or results. If a figure would strengthen the copy, it flags where you need to supply a real one.
- **Won't state claims that need substantiation.** Superlatives, comparative claims, and health/financial/safety results get flagged, along with a note when something needs legal review.
- **Won't guess at things that change.** Ad specs, SEO practice, platform algorithms, creator rates, and disclosure law get web-searched rather than answered from memory.
- **Won't dress up hypotheses as findings.** Personas or positioning built without data are labelled as things to validate.
- **Won't promise outcomes.** No guaranteed rankings, CPAs, or conversion rates.

---

## Extending it

To add a workflow:

1. Write `references/<name>.md` — scope line, structure or checklist, then a "Rules" section covering that domain's failure mode.
2. Add a row to the routing table in `SKILL.md`.
3. Add the slash command to the command list.
4. **Add the domain to the `description` field.** This is the step people forget, and skipping it means the workflow never triggers — Claude decides whether to use a skill based only on its description.
5. Repackage and re-upload.

To trim: after a few weeks, delete reference files that never get routed to. Anthropic's own guidance favors focused skills over one that does everything, so treat 24 workflows as a ceiling rather than a target — a tighter skill routes more accurately.

---

## Security note

Only install skills from sources you trust, including this one. Before enabling any third-party skill, read the files — this repo is plain markdown with no scripts, no dependencies, and no external network calls, and you can verify that in about two minutes. Apply the same scrutiny to skills that aren't.

---

## Contributing

Issues and PRs welcome, particularly:

- Workflows that are missing
- Reference files that give bad advice in your domain
- Description tweaks that improve triggering accuracy

If you're adding a workflow, follow the extension steps above and include an example prompt that should route to it.

---

## Further reading

- [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude) — official install docs
- [Creating custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills) — skill authoring guide
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)

---

## License

MIT — do whatever you want with it.
`````

---

### File: `LICENSE`

````
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
````
