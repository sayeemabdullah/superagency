# Superagency

A Claude Skill that acts as a full marketing team — 28 workflows covering content, campaigns, SEO, paid ads, email, conversion, PR, competitive research, lifecycle, analytics, pricing, sales enablement, marketing ops, and more.

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
| `pricing` | Pricing & packaging | Tier design, price changes, discounting, objection diagnosis | *"Should we add a cheaper tier?"* |
| `sales` | Sales enablement | One-pagers, objection docs, demo scripts, pitch decks | *"Write a one-pager the sales team can leave behind"* |
| `ops` | Marketing ops | Lead lifecycle, routing, MQL/SQL definitions, data hygiene | *"Define our MQL criteria with sales"* |

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

Download [`superagency.skill`](../../raw/main/superagency.skill) from this repo, or grab a pinned version from [Releases](../../releases/latest).

You never build it yourself. CI rebuilds the archive from `superagency/` on every PR and commits it, so the copy on `main` always matches the source.

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

Download it from [Releases](../../releases/latest), or `git pull` if you have a clone.

Either way it's already built. Nothing to package, nothing to run — CI rebuilt the archive when the change merged, and attached it to the release when the version was tagged.

### Replace it in Claude.ai

1. **Customize → Skills** ([claude.ai/customize/skills](https://claude.ai/customize/skills))
2. Click the skill to open it
3. Click **···** next to the toggle → **Delete** → confirm
4. **+** → **Create skill** → **Upload a skill** → pick the new `superagency.skill`
5. Toggle it on
6. **Start a new conversation** — open chats keep the old version for their whole session

Deleting is safe: the skill folder is stateless instruction. Nothing is stored server-side that a re-upload won't restore.

### Keeping your brand profile and pulse history

`references/brand.md` and `references/pulse-log.md` are written to *during conversations*, and those edits live in the chat session — not in the copy you uploaded. Re-uploading, or just starting a new chat, resets both to blank templates.

The skill handles this: whenever it writes to either file it prints the whole file as one fenced code block and tells you to save it. Keep that block somewhere, and paste it back at the start of your next session — the skill picks up from it. No rebuilding the archive.

The durable fix, if you'd rather bake the profile in, is to commit your filled-in `brand.md` as a normal PR. CI rebuilds the archive around it, and every build from then on carries your profile — no paste step to remember.

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

## Getting started, step by step

The whole path, from a fresh install to a working weekly rhythm.

### 1. Install and open a new chat

Follow [Install](#install) above — enable code execution, upload `superagency.skill`, toggle it on. Skills load at the **start** of a conversation, so open a fresh chat before testing.

### 2. Just ask — no command needed

Type a marketing task in plain language:

> Write a LinkedIn post announcing our new pricing tier.

The skill reads its router, picks one workflow (`content`, here), loads only that file, and answers. You never choose the workflow yourself: *"someone's complaining about us on Twitter"* lands on `crisis`, *"how do we stop churn"* on `lifecycle`, *"should we add a cheaper tier"* on `pricing`.

If it routes wrong, put the keyword in front to override the guess — `sequence — win-back flow for churned accounts`. The full list is in [What it does](#what-it-does).

### 3. Set your brand voice once

The first time you ask for anything customer-facing, the skill asks three questions:

- Who's the audience?
- Two or three adjectives for how the brand should sound
- Anything to avoid — banned words, competitor names, compliance lines

Answer them and it writes a profile into `brand.md`. Every draft after that is checked against it, and the `voice` keyword runs a dedicated *"does this sound like us?"* review with line-by-line fixes.

**Then save the profile.** The skill prints the whole of `brand.md` as one fenced code block — copy that block into a note somewhere. Step 6 explains why.

### 4. Produce a real deliverable

Ask for something with substance:

> Plan a 6-week launch for our API. Budget $15k, hard date April 1.

You get a one-page campaign brief as a file. Where a number would help but you didn't supply one, it flags the gap instead of inventing it; where the plan rests on a claim that needs substantiation or legal sign-off, it says so.

Tools run automatically when the task needs arithmetic — a budget backsolve, a significance test, an ad-copy character check, a calendar-dependency scan — and Claude shows the command it ran rather than eyeballing the answer.

### 5. Run the weekly pulse

Once a week, paste your numbers:

> How did we do this week? Signups 412 (+18%), demos 22 (-9%), trials-to-paid 31%.

You get wins, misses, anomalies, and **one** recommended action, formatted to drop into Slack or email. It also appends the week to `pulse-log.md` and prints the **whole file** back as a block — save that the same way you saved the brand profile. After a few weeks, `trend` reads the accumulated history and tells you what's actually moving, not just what happened last week.

### 6. Restore state at the start of each session

`brand.md` and `pulse-log.md` live only inside the conversation that wrote them. A new chat — or a re-upload — starts from the blank templates.

So when you start a session that needs either one, paste the saved block back in:

> Here's my brand profile: [paste the fenced block]

The skill picks up from it. If you'd rather not do this each time, commit your filled-in `brand.md` as a PR (see [Extending it](#extending-it)) — CI bakes it into every future build and there's nothing to paste.

### 7. Update when a new version ships

Claude.ai has no in-place update: you delete the old skill and upload the new one — full steps in [Updating an installed skill](#updating-an-installed-skill). Your saved blocks from steps 3 and 5 carry your state across the swap.

---

## How it's built

```
superagency/
├── SKILL.md              # ~125-line router: frontmatter, routing table, standing rules
└── references/
    ├── content.md
    ├── campaigns.md
    ├── brand.md          # stateful — stores your voice profile
    ├── ...
    └── pulse-log.md      # stateful — accumulates weekly metrics
```

It also ships seven Python tools it actually runs, so the numbers aren't guessed.

Skills load in three stages: the `description` is always in context, the SKILL.md body loads when the skill triggers, and reference files load only when needed. Putting all 28 workflows in one file would mean loading ~40,000 characters of mostly-irrelevant instructions on every request.

So `SKILL.md` is just a routing table. Ask about SEO, it reads `references/seo.md` and nothing else.

Every workflow file follows the same shape: a scope line, the workflow itself, an `Output` section saying what lands inline vs as a file, a `Red flags` table, and a `Rules` section encoding that domain's failure mode — fabricated numbers, unsubstantiated claims, advice that goes stale. Files that commonly work together point at each other with an "Often pairs with" line.

### Where the skill stops

"Marketing" is unbounded, so the scope is drawn on purpose:

- **Advice and drafts, not execution.** It writes the press release, plans the campaign, designs the sequence. It does not run your ad accounts, send from your ESP, administer your CRM, or configure your martech stack.
- **No production of built or visual assets.** It briefs a designer; it doesn't design. It scripts a video; it doesn't cut one. It specs a landing page; it doesn't build it.
- **No legal, financial, or accounting judgement.** It flags what needs sign-off and stops there.
- **28 workflows is a ceiling, not a target.** Anthropic's own guidance favours focused skills, and a tighter router is a more accurate one. A new workflow earns its place only if it doesn't lexically collide with an existing one — `scripts/route_lint.py` measures that on every PR, and `make route` prints the most-similar pairs so you can see a collision coming.

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

1. Write `references/<name>.md` — scope line, structure or checklist, an `Output` section, a `Red flags` table (≥2 rows, each a quoted thought), and a `Rules` section covering that domain's failure mode.
2. Add a row to the routing table in `SKILL.md`.
3. Add the keyword to the keyword list in `SKILL.md`, and a row to the table in this README — same order in both.
4. **Add the domain to the `description` field.** This is the step people forget, and skipping it means the workflow never triggers — Claude decides whether to use a skill based only on its description.
5. Add at least one case to `evals/routing.jsonl` — the validator fails without it.
6. Run `make check && make route && make test`. If `make route` drops sharply, your routing row or `Covers:` line collides with an existing workflow — reword until it doesn't. Then open a PR, and tag a release once merged — see [Updating an installed skill](#updating-an-installed-skill), noting the old copy must be deleted first.

To trim: after a few weeks, delete reference files that never get routed to. Anthropic's own guidance favors focused skills over one that does everything, so treat 28 workflows as a ceiling rather than a target — a tighter skill routes more accurately.

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
| `calcheck.py` | Eyeballing a calendar for late dependencies | `campaigns.md` |

Standard library only — the skill sandbox has no network, so there's nothing to install. A standing rule in `SKILL.md` tells Claude never to estimate what a tool computes, and to show the command it ran.

```
You:    Is a 3% lift on 400 visitors significant?
Claude: [runs ab.py result --a 400 12 --b 400 13]
        p=0.839. Inconclusive, and underpowered — detecting a 20% lift
        needs ~13,900 per variant. This is not a loss, it's no data.
```

### Worked examples

`references/examples/` holds eight reference-quality outputs — a campaign brief, battlecard, landing page teardown, weekly pulse, positioning framework, buyer persona, press release, and email sequence — loaded only when that workflow runs. Every number in them is invented and each carries a banner saying so, because the skill's central rule is never to present invented figures as evidence.

### Routing checks

A router skill degrades silently: add an overlapping workflow and requests quietly land in the wrong file. `evals/routing.jsonl` holds 90 prompts with the file each should reach, covering all 28 workflows — including deliberately oblique and boundary-case phrasings for the pairs that get confused.

Two things run against it:

```bash
make route     # deterministic, in CI — a lexical proxy for routing accuracy
make eval      # the real thing: asks a model. needs ANTHROPIC_API_KEY, costs money
```

`route_lint.py` builds a bag-of-words profile per workflow and routes each prompt by term overlap. The absolute score (~71%) doesn't mean much — a lexical router is dumb — but the **delta** does: a new workflow that collides with an existing one drops it, in CI, before the ambiguity ships. It also prints the most-similar workflow profiles directly. `make eval` is the honest measure; it's out of CI because it costs money and isn't deterministic, so run it after adding a workflow and compare against your last score.

---

## Red flags: naming the excuse, not the rule

Every workflow file carries a table of the thoughts that immediately precede that domain's failure:

| Thought | Reality |
|---|---|
| "p = 0.06 is basically significant." | It is not. Run `scripts/ab.py result` and report the interval, not a verdict you rounded toward. |
| "The budget is short, I'll spread the gap across channels." | Run `scripts/budget.py backsolve` and state the shortfall plainly. A quiet gap becomes someone's missed target. |
| "I'll write the quote in the CEO's voice." | Label it a draft for a named person to approve. Never present an invented quote as said. |

A rule tells you what to do. A red flag catches you talking yourself out of it — which is where the violation actually happens. `SKILL.md` carries a router-level table for the rationalizations that cut across every workflow, and the validator refuses a workflow file without one.

---

## Building and releasing

**You never build, commit, or push `superagency.skill`.** CI owns that file.

Edit `superagency/`, open a PR, and that's the whole job. CI rebuilds the archive, commits it to your branch, and it reaches `main` with your merge. Releases are built and published by CI too. If you find yourself running `zip`, something has gone wrong — `make hooks` installs a guard that stops the archive being staged by hand.

```bash
make hooks    # once — installs a pre-commit guard against hand-built archives
make check    # structural validation, same as CI
make route    # deterministic routing proxy, same as CI
make test     # unit tests for the bundled tools
make skill    # rebuild locally to inspect; do not commit the result
```

| When | What runs |
|---|---|
| Every PR | `validate.yml` — validates structure, runs the routing proxy, runs the tool tests, rebuilds, and commits the archive to the PR branch if it's stale |
| Push to `main` | Same workflow in verify-only mode; fails if `main`'s archive drifts from source |
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

Since a rule that stops firing looks identical to one that works, it also requires a `Red flags` table in every workflow file, with at least two rows whose left column is a quoted thought.

It also covers the tooling: every referenced script exists, every shipped script is referenced by something, **every tool's `--help` actually runs** (a stray `%` in an argparse help string is enough to break it, and did), every example carries its illustrative banner, and every routed workflow has an eval case.

Alongside it, `scripts/route_lint.py` runs in CI as a deterministic proxy for routing accuracy — a lexical router over the eval prompts, failed under 60%. It won't catch a subtle wording problem, but it catches a new workflow whose routing row collides with an existing one, which is the failure that otherwise ships silently.

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

3. **Make the change.** For a new workflow, follow the six steps in [Extending it](#extending-it): the new `references/<name>.md`, a routing row and keyword in `SKILL.md`, the `description` field, a row in this README's keyword table, and a case in `evals/routing.jsonl`.

4. **Validate** — the same checks CI runs:

   ```bash
   make check && make route && make test
   ```

   **Leave `superagency.skill` alone** — don't build it, don't stage it, don't push it. CI rebuilds it and commits it to your branch for you. Run `make hooks` once and git will stop you staging it by accident.

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
