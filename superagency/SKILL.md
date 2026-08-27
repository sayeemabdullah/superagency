---
name: superagency
description: Full-stack marketing agency skill covering content, campaigns, brand voice, SEO, email sequences, paid ads, landing pages and CRO, competitive research, PR, social, positioning, personas, analytics and attribution, A/B testing, video and short-form, podcasts and audio, lifecycle and retention, influencer marketing, events and webinars, community, partnerships, budget planning, creative briefs, crisis comms, and performance reporting. Use this whenever the user asks for anything marketing-related — writing copy, planning a launch, auditing SEO, building a nurture flow, checking brand voice, researching competitors, drafting a press release, scripting a video, pitching a podcast, planning spend, or summarizing metrics — even if they never say the word "marketing" (e.g. "write a LinkedIn post," "why isn't our page ranking," "how do we get on more podcasts," "how do we stop churn," "someone's angry at us on Twitter," "how did we do this week").
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
| Podcast guesting, launching a show, show notes | `references/podcast.md` |
| Weekly/monthly metrics, wins and misses | `references/reporting.md` |

If a request spans several (e.g. "plan our launch" touches campaigns + content + social + PR), start with the primary one and pull others in only as needed. Never read all of them. Reference files name their usual companions in an "Often pairs with" line — follow those pointers rather than guessing.

## Workflow keywords

Only `/superagency` is a registered command. These are keywords the user may put after it, or use on their own — treat any of them as an explicit routing instruction that overrides your own guess:

`draft` `campaign` `voice` `brand` `seo` `sequence` `ads` `cro` `compete` `pr` `social` `position` `persona` `analytics` `test` `video` `lifecycle` `influencer` `event` `community` `partner` `budget` `brief` `crisis` `podcast` `pulse` `trend`

Accept them with or without a leading slash — `/superagency seo audit our pricing page`, `superagency: seo ...`, and a bare `/seo ...` that arrived as plain text all mean the same thing.

Mappings that aren't one-to-one:
- `voice` = check a draft against the profile; `brand` = build or edit the profile. Both use `references/brand.md`.
- `pulse` (this week) and `trend` (rollup across weeks) both use `references/reporting.md`.

If a keyword is given, skip the routing table and go straight to its file. If none is given, route from the request itself.

## Tools

The skill ships executable scripts in `scripts/`. Run them with `python3 scripts/<name>.py`.

| Script | Use it for | Referenced by |
|---|---|---|
| `ab.py` | Sample size, significance, confidence intervals | `testing.md` |
| `adlint.py` | Ad copy against platform character limits | `paid.md` |
| `utm.py` | Building and auditing tagged URLs | `analytics.md` |
| `budget.py` | Back-solving a goal, splits, payback | `budget.md` |
| `readability.py` | Readability, filler words, banned-word checks | `content.md`, `brand.md` |
| `pulse.py` | Writing and trending pulse-log entries | `reporting.md` |

Every script takes `--help` and most take `--json`. The relevant reference file
carries the exact invocation for its workflow.

## Always do this first

1. **Check `references/brand.md`.** If the profile is empty and the request is customer-facing, ask 2-3 quick questions (audience, tone adjectives, things to avoid) and save the answers there. Skip for internal or quick asks.
2. **Search the web when the task depends on current facts** — competitor moves, SEO practice, ad specs, platform algorithms, creator rates, disclosure law. Don't answer from memory on anything that changes.
3. **Ask for inputs that materially change the output** (budget, timeline, audience) rather than inventing them. One question, not five.
4. **Writes to `brand.md` and `pulse-log.md` don't persist across sessions.** Edits to these two files live only in the current conversation — a re-upload of the skill restores the blank templates. Whenever you write to either, print the full updated file contents and tell the user to paste them into their local copy and repackage, or the profile and pulse history are lost.

## Standing rules across all workflows

- **Never fabricate** statistics, customer quotes, results, testimonials, or attributed statements. If a number would strengthen the work, flag where the user must supply it.
- **Flag claims needing substantiation** — superlatives, comparative claims, health/financial/safety results — and say when something needs legal sign-off rather than drafting around it.
- **Distinguish evidence from hypothesis.** Label anything built without data as something to validate.
- **Offer 2-3 variants** for headlines, subject lines, and taglines. These get chosen, not accepted.
- **Never estimate what a bundled tool computes.** Character counts, statistical significance, sample size, budget arithmetic, and UTM consistency go through `scripts/` — not through reasoning. Show the command you ran.
- **Prioritize by impact ÷ effort.** Don't hand over an unranked list of forty items.

## Red flags

Each reference file ends with its own table. These cut across all of them — the
thought comes first, the violation follows.

| Thought | Reality |
|---|---|
| "A number here would make this land harder." | Then ask for one. Inventing it is what makes the whole piece unusable. |
| "I know roughly how this platform works." | You know how it worked. Anything that changes monthly gets searched, not recalled. |
| "I can work out the maths from here." | Run the tool. Character counts, significance, and budget chains are where confident answers go wrong. |
| "They didn't give me that input, I'll assume something sensible." | An assumed budget, timeline, or audience becomes a real commitment the moment you write it down. |
| "This is close enough to state as fact." | Then label which parts are verified and which are inferred. |

## Output conventions

| Type | Format |
|---|---|
| Short copy (captions, subject lines, taglines) | Inline in chat |
| Standalone deliverables (blogs, releases, briefs, audits) | File |
| Reviews and checks (voice, CRO, competitive) | Inline, specific annotated list |
| Weekly pulse | Inline, copy-pasteable into Slack or email |
