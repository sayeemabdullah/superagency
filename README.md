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

Download `superagency.skill` from [Releases](../../releases/latest).

The archive isn't committed to the repo — it's a build artifact. CI builds it on every PR and attaches it to each tagged release, so a release download always matches the source it was built from.

Note that `main` can be ahead of the latest release. If you want the very newest source, build it yourself with Option B.

**Option B — build it from a clone**

Only needed if you've made local changes you haven't pushed yet:

```bash
git clone https://github.com/sayeemabdullah/superagency.git
cd superagency
./scripts/build.sh
```

Use the script rather than a bare `zip` — it produces the same bytes CI does, and fails if the archive root isn't `superagency/`, which is what Claude.ai rejects on upload.

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

## Updating an installed skill

Claude.ai has **no in-place update**. Uploading a revised file does not replace the copy already installed — you get a second skill with the same `name`, and two skills answering to `/superagency` route unpredictably. Delete the old one first.

### Get the new file

Download the newest file from [Releases](../../releases/latest). It's already built — CI produced it when the version was tagged.

From a clone, `git pull && ./scripts/build.sh` gives you the same thing from current `main`, which may be ahead of the latest release.

### Replace it in Claude.ai

1. **Customize → Skills** ([claude.ai/customize/skills](https://claude.ai/customize/skills))
2. Click the skill to open it
3. Click **···** next to the toggle → **Delete** → confirm
4. **+** → **Create skill** → **Upload a skill** → pick the new `superagency.skill`
5. Toggle it on
6. **Start a new conversation** — open chats keep the old version for their whole session

Deleting is safe: the skill folder is stateless instruction. Nothing is stored server-side that a re-upload won't restore.

### One thing you will lose

`references/brand.md` and `references/pulse-log.md` are written to *during conversations*, and those edits live in the chat session — not in the copy you uploaded. Re-uploading resets both to blank templates.

So before you delete: open the skill in Claude, ask it to print the current contents of both files, and paste them into your local copies. Otherwise you lose your voice profile and your accumulated pulse history.

The durable fix is to commit your filled-in `brand.md` as a normal PR. CI rebuilds the archive around it, and every build from then on carries your profile — no manual step to remember.

### In Claude Code

No archive, no delete step. If you symlinked it, `git pull` is the whole update:

```bash
ln -s "$PWD/superagency" ~/.claude/skills/superagency   # once
```

If you copied instead of symlinking, re-copy: `rm -rf ~/.claude/skills/superagency && cp -R superagency ~/.claude/skills/`.

### Checking whether you're out of date

Releases are versioned, so compare tags rather than guessing:

```bash
gh release view --repo sayeemabdullah/superagency --json tagName --jq .tagName
```

Or just look at [Releases](../../releases/latest). If that tag is newer than the one you installed, re-download and re-upload.

There's no version string inside the skill itself, so Claude can't tell you which build is loaded. If you're unsure, re-download and re-upload — it costs a minute and is always safe.

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

It also ships six Python tools it actually runs, so the numbers aren't guessed.

Skills load in three stages: the `description` is always in context, the SKILL.md body loads when the skill triggers, and reference files load only when needed. Putting all 25 workflows in one file would mean loading ~35,000 characters of mostly-irrelevant instructions on every request.

So `SKILL.md` is just a routing table. Ask about SEO, it reads `references/seo.md` and nothing else.

Every workflow file follows the same shape: a scope line, the workflow itself, an `Output` section saying what lands inline vs as a file, and a `Rules` section encoding that domain's failure mode — fabricated numbers, unsubstantiated claims, advice that goes stale. Files that commonly work together point at each other with an "Often pairs with" line.

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
5. Run `make check`, open a PR, then tag a release — see [Updating an installed skill](#updating-an-installed-skill), and note that the old copy must be deleted first.

To trim: after a few weeks, delete reference files that never get routed to. Anthropic's own guidance favors focused skills over one that does everything, so treat this many workflows as a ceiling rather than a target — a tighter skill routes more accurately.

---

## It computes instead of guessing

Most marketing skills are prose. This one bundles executable tools, because its own rules demand precision a language model can't reliably produce by reasoning — `testing.md` forbids calling a winner on underpowered data, `paid.md` lists character limits, `analytics.md` calls inconsistent UTMs the top cause of broken reporting.

| Tool | Replaces | Used by |
|---|---|---|
| `ab.py` | Statistics done in your head | `testing.md` |
| `adlint.py` | Counting characters by eye | `paid.md` |
| `utm.py` | Staying consistent by hand | `analytics.md` |
| `budget.py` | A four-step arithmetic chain | `budget.md` |
| `readability.py` | "This reads well, I think" | `content.md`, `brand.md` |
| `pulse.py` | Free-form log entries `trend` can't parse | `reporting.md` |

Standard library only — the skill sandbox has no network, so there's nothing to install. A standing rule in `SKILL.md` tells Claude never to estimate what a tool computes, and to show the command it ran.

```
You:    Is a 3% lift on 400 visitors significant?
Claude: [runs ab.py result --a 400 12 --b 400 13]
        p=0.839. Inconclusive, and underpowered — detecting a 20% lift
        needs ~13,900 per variant. This is not a loss, it's no data.
```

### Worked examples

`references/examples/` holds four reference-quality outputs — a campaign brief, battlecard, landing page teardown, and weekly pulse — loaded only when that workflow runs. Every number in them is invented and each carries a banner saying so, because the skill's central rule is never to present invented figures as evidence.

### Routing evals

A router skill degrades silently: add an overlapping workflow and requests quietly land in the wrong file. `evals/routing.jsonl` holds 53 prompts with the file each should reach, covering all 25 workflows.

```bash
export ANTHROPIC_API_KEY=sk-...
make eval
```

Deliberately not in CI — it costs money and isn't deterministic. Run it after adding a workflow and compare against your last score.

---

## Building and releasing

**You never build, commit, or push `superagency.skill`.** CI owns that file.

Edit `superagency/`, open a PR, and that's the whole job. The archive is gitignored: CI builds and validates it on every PR, and `release.yml` builds and attaches it when you tag a version. If you find yourself running `zip` by hand, use `./scripts/build.sh` instead — a bare `zip` won't reproduce the same bytes.

```bash
make check    # structural validation, same as CI
make test     # unit tests for the bundled tools
make skill    # build the archive locally (gitignored)
```

| When | What runs |
|---|---|
| Every PR and push to `main` | `validate.yml` — validates, runs the tool tests, builds the archive, and uploads it as a 14-day artifact |
| Push a `v*` tag | `release.yml` — validates, builds, and attaches `superagency.skill` to a GitHub Release |

### Cutting a release

A maintainer pushes a tag; CI does everything else:

```bash
git tag v1.1 && git push origin v1.1
```

`release.yml` validates, builds, creates the GitHub Release, and attaches `superagency.skill` to it. No archive is uploaded by hand, and the released asset is byte-identical to the one on `main` — the build is deterministic, so the same source always produces the same file.

### Why the build is deterministic

`scripts/build.sh` normalizes file timestamps and sorts the file list before zipping. Without that, `zip` embeds mtimes and every rebuild produces different bytes — CI would commit a phantom change on every push, and each bot commit would retrigger the build. Normalized, identical content always yields an identical archive, so "has this actually changed?" is a byte comparison.

A consequence worth knowing: if you run `make skill` and your source matches `main`, the rebuild is byte-identical and leaves your tree clean. A diff means your source genuinely changed — and CI will commit that rebuild for you.

`scripts/validate.py` enforces the invariants that break the skill silently: frontmatter is exactly `name` + `description` on one line, every routing row resolves to a real file, every workflow file has `Rules` and `Output`, cross-references resolve, the keyword list matches the README table, every workflow appears in the `description`, and both stateful files ship empty.

It also covers the tooling: every referenced script exists, every shipped script is referenced by something, **every tool's `--help` actually runs** (a stray `%` in an argparse help string is enough to break it, and did), every example carries its illustrative banner, and every routed workflow has an eval case.

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

3. **Make the change.** For a new workflow that's four edits: the new `references/<name>.md`, a routing row in `SKILL.md`, the keyword list, and the `description` field. Add a row to the keyword table in this README too, and at least one case to `evals/routing.jsonl` — the validator fails without it.

4. **Validate** — the same checks CI runs:

   ```bash
   make check
   ```

   **Don't commit `superagency.skill`** — it's gitignored. CI builds and validates it for you; run `make skill` if you want to inspect the archive locally.

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

CI runs `scripts/validate.py` on every PR and fails on a routing row pointing at a missing file, a workflow file without its `Rules`/`Output` sections, keyword drift between `SKILL.md` and the table above, or a workflow missing from the `description` field.

---

## Further reading

- [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude) — official install docs
- [Creating custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills) — skill authoring guide
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)

---

## License

MIT — do whatever you want with it.
