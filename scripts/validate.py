#!/usr/bin/env python3
"""Structural validation for the Superagency skill.

Checks the invariants that break the skill silently: malformed frontmatter,
routing rows pointing at files that don't exist, workflow files missing their
guardrail sections, and keyword drift between SKILL.md and the README.

Exit 0 = valid, 1 = one or more failures (each printed).
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIR = os.path.join(ROOT, "superagency")
REF_DIR = os.path.join(SKILL_DIR, "references")
SKILL_MD = os.path.join(SKILL_DIR, "SKILL.md")
README = os.path.join(ROOT, "README.md")

# Written to at runtime; they ship as empty templates and have no Rules/Output.
STATEFUL = {"brand.md", "pulse-log.md"}

failures = []


def fail(msg):
    failures.append(msg)


def check_frontmatter(text):
    lines = text.split("\n")
    if lines[0] != "---":
        fail("SKILL.md: does not open with '---'")
        return
    try:
        end = lines.index("---", 1)
    except ValueError:
        fail("SKILL.md: frontmatter is never closed")
        return

    fm = lines[1:end]
    if len(fm) != 2:
        fail(f"SKILL.md: frontmatter must be exactly 2 lines, found {len(fm)}. "
             "A wrapped description silently breaks triggering.")
        return

    keys = [l.split(":", 1)[0] for l in fm]
    if keys != ["name", "description"]:
        fail(f"SKILL.md: frontmatter keys must be [name, description], found {keys}")
    if fm[0] != "name: superagency":
        fail(f"SKILL.md: name must be 'superagency', found {fm[0]!r}")

    desc = fm[1][len("description: "):]
    if len(desc) > 1024:
        fail(f"SKILL.md: description is {len(desc)} chars, over the 1024 limit")
    return desc


def main():
    if not os.path.isdir(REF_DIR):
        fail(f"missing {REF_DIR}")
        return

    skill = open(SKILL_MD).read()
    readme = open(README).read()
    refs = sorted(f for f in os.listdir(REF_DIR) if f.endswith(".md"))

    desc = check_frontmatter(skill)

    # Every routing row must resolve to a real file.
    routed = re.findall(r"^\|.*\| `references/([a-z\-]+\.md)` \|$", skill, re.M)
    for r in routed:
        if r not in refs:
            fail(f"SKILL.md: routing table points at references/{r}, which does not exist")
    if len(routed) != len(set(routed)):
        dupes = {r for r in routed if routed.count(r) > 1}
        fail(f"SKILL.md: duplicate routing rows for {sorted(dupes)}")

    # Every workflow file needs its guardrails and an output contract.
    for r in refs:
        text = open(os.path.join(REF_DIR, r)).read()
        if not text.lstrip().startswith("# "):
            fail(f"{r}: no H1 heading")
        if r in STATEFUL:
            continue
        if r not in routed:
            fail(f"{r}: exists but no routing row points at it, so it can never load")
        if "\n## Rules" not in text:
            fail(f"{r}: missing '## Rules' section")
        if "\n## Output" not in text:
            fail(f"{r}: missing '## Output' section")

    # Cross-references between reference files must resolve.
    for r in refs:
        text = open(os.path.join(REF_DIR, r)).read()
        for target in set(re.findall(r"`([a-z\-]+\.md)`", text)):
            if target not in refs:
                fail(f"{r}: cross-reference to `{target}`, which does not exist")

    # Keyword list must match the README table, in the same order.
    kw_lines = [l for l in skill.split("\n") if l.startswith("`draft`")]
    if not kw_lines:
        fail("SKILL.md: keyword list not found")
    else:
        keywords = re.findall(r"`([a-z]+)`", kw_lines[0])
        table = re.findall(r"^\| `([a-z]+)` \|", readme, re.M)
        if keywords != table:
            only_skill = sorted(set(keywords) - set(table))
            only_readme = sorted(set(table) - set(keywords))
            if only_skill or only_readme:
                fail(f"keyword drift — only in SKILL.md: {only_skill}, "
                     f"only in README: {only_readme}")
            else:
                fail("keyword list and README table have the same keywords in different order")

        # A workflow absent from the description can never trigger. Some
        # keywords are shorthand for a phrase the description spells out.
        aliases = {
            "compete": "competitive",
            "pulse": "performance reporting",
            "trend": "performance reporting",
        }
        if desc:
            low = desc.lower()
            for kw in keywords:
                if aliases.get(kw, kw) not in low:
                    fail(f"keyword '{kw}' has no matching domain in the description "
                         "field, so requests for it may never trigger the skill")

    # The stateful files must ship empty.
    brand = open(os.path.join(REF_DIR, "brand.md")).read()
    if "### Audience\n(Who?" not in brand:
        fail("brand.md: audience placeholder is filled in — it must ship as a blank template")
    pulse = open(os.path.join(REF_DIR, "pulse-log.md")).read()
    if "<!-- No entries yet -->" not in pulse:
        fail("pulse-log.md: must ship with no entries")

    print(f"checked {len(refs)} reference files, {len(routed)} routing rows")


main()

if failures:
    print(f"\n{len(failures)} problem(s):\n", file=sys.stderr)
    for f in failures:
        print(f"  ✗ {f}", file=sys.stderr)
    sys.exit(1)
print("all checks passed")
