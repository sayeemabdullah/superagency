#!/usr/bin/env python3
"""Score copy for readability, and check it against the saved brand profile.

content.md says to cut adjectives that survive deletion and lead with the
benefit; brand.md keeps a banned-words list. Both are easy to violate while
sounding fine. This measures what can be measured and matches the banned list
mechanically, so the voice check starts from evidence rather than impression.

  python3 scripts/readability.py draft.md --channel linkedin
  echo "some copy" | python3 scripts/readability.py --channel email-subject
"""
import argparse
import json
import os
import re
import sys

# From content.md's channel norms table. Words unless stated otherwise.
CHANNELS = {
    "linkedin":      (150, 300, "words"),
    "x":             (1, 280, "chars"),
    "instagram":     (100, 200, "words"),
    "email-subject": (1, 60, "chars"),
    "email-body":    (100, 250, "words"),
    "blog":          (800, 1500, "words"),
    "case-study":    (500, 900, "words"),
}

VOWELS = "aeiouy"
PASSIVE = re.compile(r"\b(was|were|is|are|been|being|be)\s+\w+(ed|en)\b", re.I)
WEAK = ("very", "really", "quite", "just", "actually", "basically", "simply",
        "powerful", "innovative", "seamless", "robust", "cutting-edge",
        "world-class", "best-in-class", "revolutionary", "game-changing")


def syllables(word):
    word = re.sub(r"[^a-z]", "", word.lower())
    if not word:
        return 0
    count, prev_vowel = 0, False
    for ch in word:
        v = ch in VOWELS
        if v and not prev_vowel:
            count += 1
        prev_vowel = v
    if word.endswith("e") and count > 1:
        count -= 1
    return max(count, 1)


def sentences(text):
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s for s in parts if s.strip()]


def analyze(text):
    words = re.findall(r"[A-Za-z'-]+", text)
    sents = sentences(text)
    n_w, n_s = len(words), max(len(sents), 1)
    n_syl = sum(syllables(w) for w in words)
    if n_w == 0:
        raise ValueError("no words found")

    wps, spw = n_w / n_s, n_syl / n_w
    flesch = 206.835 - 1.015 * wps - 84.6 * spw
    grade = 0.39 * wps + 11.8 * spw - 15.59

    long_sents = sorted(
        ({"words": len(re.findall(r"[A-Za-z'-]+", s)), "text": s.strip()} for s in sents),
        key=lambda d: -d["words"])[:3]

    lowered = " " + text.lower() + " "
    weak_hits = {w: lowered.count(f" {w} ") + lowered.count(f" {w},") + lowered.count(f" {w}.")
                 for w in WEAK}
    weak_hits = {w: c for w, c in weak_hits.items() if c}

    return {
        "words": n_w, "sentences": n_s, "chars": len(text),
        "avg_words_per_sentence": round(wps, 1),
        "flesch_reading_ease": round(flesch, 1),
        "grade_level": round(grade, 1),
        "passive_hits": [m.group(0) for m in PASSIVE.finditer(text)],
        "adverb_ly_count": len([w for w in words if w.lower().endswith("ly")]),
        "weak_words": weak_hits,
        "longest_sentences": long_sents,
    }


def banned_from_brand(path):
    """Pull the banned-words list out of the user's brand profile, if filled in."""
    if not os.path.exists(path):
        return []
    banned = []
    for line in open(path):
        m = re.match(r"\s*-\s*(?:Banned words/phrases|Never claim|Avoid)\s*:\s*(.+)", line, re.I)
        if m and m.group(1).strip():
            banned += [t.strip() for t in re.split(r"[,;]", m.group(1)) if t.strip()]
    return banned


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("file", nargs="?", help="file to score (default: stdin)")
    p.add_argument("--channel", choices=sorted(CHANNELS), help="check length against content.md norms")
    p.add_argument("--brand", default="references/brand.md",
                   help="brand profile to read banned words from")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    text = open(args.file).read() if args.file else sys.stdin.read()
    try:
        r = analyze(text)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.channel:
        lo, hi, unit = CHANNELS[args.channel]
        actual = r["words"] if unit == "words" else r["chars"]
        r["channel"] = {"name": args.channel, "unit": unit, "min": lo, "max": hi,
                        "actual": actual, "within": lo <= actual <= hi}

    hits = [b for b in banned_from_brand(args.brand) if b.lower() in text.lower()]
    r["banned_words_found"] = hits
    r["brand_profile_checked"] = bool(banned_from_brand(args.brand))

    if args.json:
        print(json.dumps(r, indent=2))
        return 1 if hits or (args.channel and not r["channel"]["within"]) else 0

    print(f"{r['words']} words, {r['sentences']} sentences, {r['chars']} chars")
    print(f"Flesch reading ease {r['flesch_reading_ease']} (higher is easier), "
          f"grade level {r['grade_level']}")
    print(f"Average {r['avg_words_per_sentence']} words/sentence")
    if args.channel:
        c = r["channel"]
        state = "within" if c["within"] else "OUTSIDE"
        print(f"{state} {c['name']} norm: {c['actual']} {c['unit']} (target {c['min']}-{c['max']})")
    if r["weak_words"]:
        print("\nWords that usually survive deletion: "
              + ", ".join(f"{w} x{c}" for w, c in sorted(r["weak_words"].items())))
    if r["passive_hits"]:
        print(f"Passive constructions ({len(r['passive_hits'])}): "
              + ", ".join(repr(h) for h in r["passive_hits"][:5]))
    if r["longest_sentences"] and r["longest_sentences"][0]["words"] > 25:
        s = r["longest_sentences"][0]
        print(f"\nLongest sentence ({s['words']} words): {s['text'][:110]}...")
    if hits:
        print(f"\nBANNED per brand.md: {', '.join(hits)}")
    elif not r["brand_profile_checked"]:
        print("\n(brand.md has no banned list yet — nothing to check against)")
    return 1 if hits or (args.channel and not r["channel"]["within"]) else 0


if __name__ == "__main__":
    sys.exit(main())
