#!/usr/bin/env python3
"""Structural validation for the Superagency skill.

Checks the invariants that break the skill silently: malformed frontmatter,
routing rows pointing at files that don't exist, workflow files missing their
guardrail sections, and keyword drift between SKILL.md and the README.

Exit 0 = valid, 1 = one or more failures (each printed).
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIR = os.path.join(ROOT, "superagency")
REF_DIR = os.path.join(SKILL_DIR, "references")
SKILL_MD = os.path.join(SKILL_DIR, "SKILL.md")
README = os.path.join(ROOT, "README.md")

# Written to at runtime; they ship as empty templates and have no Rules/Output.
STATEFUL = {"brand.md", "pulse-log.md"}

SCRIPT_DIR = os.path.join(SKILL_DIR, "scripts")
EXAMPLE_DIR = os.path.join(REF_DIR, "examples")
EVAL_CASES = os.path.join(ROOT, "evals", "routing.jsonl")
SKILL_MD_MAX_LINES = 500
# Examples exist to show shape. Realistic-looking numbers in them are exactly
# what the skill forbids reusing, so each must carry the warning.
EXAMPLE_BANNER = "**Illustrative only.**"

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
    refs = sorted(f for f in os.listdir(REF_DIR)
                  if f.endswith(".md") and os.path.isfile(os.path.join(REF_DIR, f)))

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
    examples = sorted(os.listdir(EXAMPLE_DIR)) if os.path.isdir(EXAMPLE_DIR) else []
    for r in refs:
        text = open(os.path.join(REF_DIR, r)).read()
        for target in set(re.findall(r"`([a-z\-]+\.md)`", text)):
            if target not in refs and target not in examples:
                fail(f"{r}: cross-reference to `{target}`, which does not exist")
        for target in set(re.findall(r"`references/examples/([a-z\-]+\.md)`", text)):
            if target not in examples:
                fail(f"{r}: points at missing example references/examples/{target}")

    # Bundled tools must exist and actually start. A literal % in an argparse
    # help string is enough to break --help, and once did.
    if not os.path.isdir(SCRIPT_DIR):
        fail("superagency/scripts/ is missing — the bundled tools do not ship")
    else:
        scripts = sorted(f for f in os.listdir(SCRIPT_DIR) if f.endswith(".py"))
        referenced = set()
        for r in refs:
            text = open(os.path.join(REF_DIR, r)).read()
            referenced |= set(re.findall(r"scripts/([a-z_]+\.py)", text))
        referenced |= set(re.findall(r"`([a-z_]+\.py)`", open(SKILL_MD).read()))

        for name in sorted(referenced):
            if name not in scripts:
                fail(f"a reference file invokes scripts/{name}, which does not exist")
        for name in scripts:
            if name not in referenced:
                fail(f"{name} ships but no reference file or SKILL.md mentions it, "
                     "so nothing will ever run it")
            proc = subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, name), "--help"],
                                  capture_output=True, text=True)
            if proc.returncode != 0:
                fail(f"scripts/{name} --help exits {proc.returncode}: "
                     f"{proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else 'no output'}")

    # Examples must be labelled so their invented numbers are never reused.
    for name in examples:
        text = open(os.path.join(EXAMPLE_DIR, name)).read()
        if EXAMPLE_BANNER not in text:
            fail(f"examples/{name}: missing the '{EXAMPLE_BANNER}' banner — "
                 "unlabelled sample numbers invite exactly the fabrication the skill forbids")
        if not text.lstrip().startswith("# "):
            fail(f"examples/{name}: no H1 heading")

    # Eval coverage: every routed workflow needs at least one case.
    if os.path.exists(EVAL_CASES):
        expected = set()
        for i, line in enumerate(open(EVAL_CASES), 1):
            if not line.strip():
                continue
            try:
                case = json.loads(line)
            except json.JSONDecodeError:
                fail(f"evals/routing.jsonl line {i}: not valid JSON")
                continue
            if case.get("expect") not in refs:
                fail(f"evals/routing.jsonl line {i}: expects {case.get('expect')!r}, "
                     "which is not a reference file")
            expected.add(case.get("expect"))
        for r in routed:
            if r not in expected:
                fail(f"{r} is routed to but has no eval case, so its routing is untested")

    if len(skill.split("\n")) > SKILL_MD_MAX_LINES:
        fail(f"SKILL.md is {len(skill.split(chr(10)))} lines, over the "
             f"{SKILL_MD_MAX_LINES}-line router ceiling")

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

    print(f"checked {len(refs)} reference files, {len(routed)} routing rows, "
          f"{len(examples)} examples, "
          f"{len([f for f in os.listdir(SCRIPT_DIR) if f.endswith(chr(46) + chr(112) + chr(121))]) if os.path.isdir(SCRIPT_DIR) else 0} tools")


main()

if failures:
    print(f"\n{len(failures)} problem(s):\n", file=sys.stderr)
    for f in failures:
        print(f"  ✗ {f}", file=sys.stderr)
    sys.exit(1)
print("all checks passed")
