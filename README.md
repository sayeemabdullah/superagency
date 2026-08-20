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

**Option B — clone and zip it yourself**

```bash
git clone https://github.com/sayeemabdullah/superagency.git
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
