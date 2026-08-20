# Superagency

A Claude Skill that acts as a full marketing team — 25 workflows covering content, campaigns, SEO, paid ads, email, conversion, PR, competitive research, lifecycle, analytics, and more.

Ask Claude a marketing question in plain language and it routes to the right workflow automatically. No prompt engineering, no re-explaining your context every time.

---

## What it does

| Keyword | Workflow | Covers | Example |
|---|---|---|---|
| `draft` | Content | Blogs, social, email, ads, case studies — with per-channel length norms | *"Write a LinkedIn post announcing our new pricing tier"* |
| `campaign` | Campaign planning | Briefs, content calendars, launch phasing, dependency checks | *"Plan a 6-week launch for our API, budget $15k"* |
| `voice` | Brand check | Flags off-voice lines with before/after fixes and severity levels | *"Does this landing page copy sound like us?"* |
| `brand` | Brand profile | Builds your voice profile from examples you consider on-brand | *"Build our voice profile from these 4 posts"* |
| `seo` | SEO | Keywords, on-page, content gaps, technical — split into quick wins vs strategic | *"Why isn't our pricing page ranking?"* |
| `sequence` | Email flows | Onboarding, nurture, re-engagement, win-back, launch — with branching logic | *"Build a 5-email onboarding flow for free-trial signups"* |
| `ads` | Paid | Google, Meta, LinkedIn, TikTok copy + creative testing strategy | *"Write 5 Google Search headline variants for 'time tracking software'"* |
| `cro` | Conversion | Landing page teardowns, funnel drop-off diagnosis | *"Our demo page converts at 1.2% — tear it down"* |
| `compete` | Competitive | Battlecards, positioning gaps, white-space analysis | *"Build a battlecard against Linear"* |
| `pr` | Press | Releases, media pitches, announcements | *"Draft a press release for our Series A"* |
| `social` | Social | Content pillars, platform cadence, calendars | *"Give us 4 content pillars and a weekly LinkedIn cadence"* |
| `position` | Positioning | Value props, messaging hierarchy, taglines | *"We sound like everyone else — sharpen our value prop"* |
| `persona` | Personas | ICP definition, buyer personas, jobs-to-be-done | *"Define the ICP for a self-serve devtool at $29/mo"* |
| `analytics` | Tracking | UTM conventions, event naming, attribution models | *"Set up a UTM convention our whole team can follow"* |
| `test` | Experiments | A/B test design, sample size, reading results honestly | *"Is a 3% lift on 400 visitors actually significant?"* |
| `video` | Video | YouTube, Reels, TikTok scripts, hooks, titles, thumbnails | *"Script a 45-second Reel on our biggest customer win"* |
| `lifecycle` | Retention | Activation, churn signals, expansion, win-back | *"Users sign up then vanish by day 3 — what do we do?"* |
| `influencer` | Creators | Sourcing, outreach, briefs, disclosure requirements | *"Draft outreach to a 30k-follower dev creator"* |
| `event` | Events | Webinars, conferences, promo timelines, follow-up | *"Build the promo timeline for a webinar in 5 weeks"* |
| `community` | Community | Slack/Discord strategy, engagement loops, health metrics | *"Our Discord is dead — how do we restart it?"* |
| `partner` | Partnerships | Co-marketing, affiliates, lead-sharing agreements | *"Pitch a co-marketing webinar to a complementary SaaS"* |
| `budget` | Planning | Channel allocation, forecasting, business cases | *"Split $40k/quarter across paid, content, and events"* |
| `brief` | Creative briefs | Briefs for designers, agencies, freelancers | *"Write a brief for a designer doing our conference booth"* |
| `crisis` | Issues response | Severity assessment, holding statements, escalation | *"Someone's angry at us on Twitter and it's spreading"* |
| `podcast` | Podcasts | Guest pitching, show format and cadence, show notes, repurposing | *"Pitch me as a guest on marketing ops podcasts"* |
| `pulse` | Weekly report | Wins, misses, anomalies, one recommended action | *"How did we do this week? [paste metrics]"* |
| `trend` | Trend summary | Month/quarter rollup from your saved pulse history | *"What's actually moved over the last quarter?"* |

### How to invoke it

**`/superagency` is the only slash command.** Claude.ai registers one command per skill, taken from the `name` field — the keywords above are routing hints the skill reads once it's running, not commands the menu knows about.

Three things that all work:

```
/superagency seo — audit our pricing page
audit our pricing page for SEO
why isn't our pricing page ranking?
```

The last one is the point: you don't need a keyword at all. "Someone's complaining about us on Twitter" routes to crisis, "how do we stop churn" routes to lifecycle. The keyword is there for when you want to override Claude's guess.

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

For weekly reporting, the `pulse` workflow appends each week's summary to `references/pulse-log.md`, so after a month or so `trend` can tell you what's actually moving rather than just what happened last week.

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

Skills load in three stages: the `description` is always in context, the SKILL.md body loads when the skill triggers, and reference files load only when needed. Putting all 25 workflows in one file would mean loading ~35,000 characters of mostly-irrelevant instructions on every request.

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
3. Add the keyword to the keyword list in `SKILL.md`, and a row to the table in this README.
4. **Add the domain to the `description` field.** This is the step people forget, and skipping it means the workflow never triggers — Claude decides whether to use a skill based only on its description.
5. Repackage and re-upload.

To trim: after a few weeks, delete reference files that never get routed to. Anthropic's own guidance favors focused skills over one that does everything, so treat this many workflows as a ceiling rather than a target — a tighter skill routes more accurately.

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

### Opening a pull request

GitHub calls it a pull request; GitLab calls the same thing a merge request. Either way:

1. **Fork** this repo (button at the top right), then clone your fork:

   ```bash
   git clone https://github.com/YOUR-FORK/superagency.git
   cd superagency
   ```

2. **Branch** — never commit to `main` directly:

   ```bash
   git checkout -b add-podcast-workflow
   ```

3. **Make the change.** For a new workflow that's four edits: the new `references/<name>.md`, a routing row in `SKILL.md`, the keyword list, and the `description` field. Add a row to the keyword table in this README too.

4. **Repackage** so `superagency.skill` matches the source:

   ```bash
   rm -f superagency.skill
   zip -rq superagency.skill superagency/ -x "*.DS_Store" "*__pycache__*"
   ```

5. **Commit and push:**

   ```bash
   git add -A
   git commit -m "Add podcast workflow"
   git push -u origin add-podcast-workflow
   ```

6. **Open the PR** — GitHub prints a link when you push, or use the CLI:

   ```bash
   gh pr create --fill
   ```

   In the description, say which workflow you added and paste one example prompt that should route to it.

Before you open it, check that `unzip -l superagency.skill` lists your new reference file, and that the skill still loads in a fresh Claude conversation.

---

## Further reading

- [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude) — official install docs
- [Creating custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills) — skill authoring guide
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)

---

## License

MIT — do whatever you want with it.
