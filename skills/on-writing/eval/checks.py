#!/usr/bin/env python3
"""Mechanical checks for on-writing eval outputs.

Usage: checks.py CASE ARM OUTPUT_FILE CASE_FILE
Prints one line per check: PASS/FAIL <case> <check>. Exit 1 if any FAIL.

The skill arm must pass every check. The baseline arm is run through the same
checks to document the delta; its failures are expected and are the point.
"""
import re
import sys
from difflib import SequenceMatcher


TRIAGE_LINE = re.compile(r"^\s*(\*\*)?(using\b|triage\b|register\b)", re.I)


def strip_triage(out):
    """Drop the triage/preamble lines; checks score only the delivered text.

    The skill emits a first line beginning "Triage:"; as a fallback, a leading
    line that names a mode is also treated as triage."""
    lines = [l for l in out.splitlines() if not TRIAGE_LINE.match(l)]
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and re.search(r"\bMode [AB]\b", lines[0]):
        lines.pop(0)
    return "\n".join(lines).strip()


def words(text):
    return re.findall(r"[A-Za-z0-9']+", text.lower())


def word_changes(original, output):
    """(edit_count, changed_words) between original and output at word level.

    An "edit" is one contiguous run of changed words; changed_words bounds
    the total volume across edits.
    """
    a, b = words(original), words(output)
    sm = SequenceMatcher(None, a, b, autojunk=False)
    edits = changed = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "equal":
            edits += 1
            changed += max(i2 - i1, j2 - j1)
    return edits, changed


def no_dashes(out, _):
    return not re.search(r"[—–]", out), "no em/en dashes"


def has_mode(mode):
    def check(out, _):
        return bool(re.search(rf"mode\s*{mode}\b", out, re.I)), f"triage declares Mode {mode}"
    return check


def first_lines_contain(token):
    def check(out, _):
        lines = [l for l in out.splitlines() if l.strip()]
        head = " ".join(lines[:3])
        return token.lower() in head.lower(), f"finding '{token}' in opening lines"
    return check


def absent(*terms):
    def check(out, _):
        found = [t for t in terms if re.search(rf"\b{re.escape(t)}\b", out, re.I)]
        return not found, f"absent: {', '.join(terms)}" + (f" (found {found})" if found else "")
    return check


def substantially_preserved(max_edits, max_words):
    """Mode B has no change quota, but the text must remain the author's:
    a bounded number of distinct edits, each small, none rewriting the voice."""
    def check(out, case):
        edits, changed = word_changes(case, out)
        ok = edits <= max_edits and changed <= max_words
        return ok, f"<= {max_edits} edits and <= {max_words} changed words (got {edits} edits, {changed} words)"
    return check


def contains(*phrases):
    def check(out, _):
        missing = [p for p in phrases if p.lower() not in out.lower()]
        return not missing, "keeps: " + "; ".join(p[:40] for p in phrases) + (f" (missing {len(missing)})" if missing else "")
    return check


def keeps_em_dash(out, _):
    return "—" in out, "author's em dash preserved"


def no_bold_header_list(out, _):
    return not re.search(r"^\s*[-*]\s+\*\*[^*]+:\*\*", out, re.M), "no bold-header list items"


def fewer_meta_nouns(out, case):
    nouns = ["approach", "framework", "perspective", "process", "level", "dynamics", "factors", "tendencies"]
    def count(text):
        return sum(len(re.findall(rf"\b{n}\b", text, re.I)) for n in nouns)
    before, after = count(case), count(out)
    return after <= before - 2, f"meta-nouns dropped by >=2 ({before} -> {after})"


CHECKS = {
    "buried-lede-abstract": {
        "both": [first_lines_contain("8 percentage points"), no_dashes,
                 absent("delves", "landscape", "underscores", "pivotal", "striking"),
                 absent("future looks bright")],
        "skill": [has_mode("A")],
    },
    "human-vignette": {
        "both": [substantially_preserved(5, 20), contains("thermos the size of a fire extinguisher")],
        "skill": [has_mode("B")],
    },
    "marketing-slop": {
        "both": [no_dashes,
                 absent("delve", "tapestry", "testament", "vibrant", "nestled", "boasts"),
                 absent("innovation, collaboration, and excellence"),
                 absent("seasoned analyst or a complete beginner"),
                 absent("exciting journey")],
        "skill": [],
    },
    "passive-docs": {
        "both": [no_bold_header_list, absent("No configuration file needed"),
                 lambda out, _: (bool(re.search(r"\byou\b|\bthe (tool|system|package manager|app)\b", out, re.I)),
                                 "actors as subjects")],
        "skill": [],
    },
    "medium-email": {
        "both": [contains("I checked the quotas by state and the skews are small",
                          "I'll send topline numbers by Friday"),
                 absent("delve", "Additionally", "I hope this helps"), no_dashes],
        "skill": [],
    },
    "meta-jargon": {
        "both": [fewer_meta_nouns, absent("In terms of")],
        "skill": [],
    },
    "luskin-passage": {
        "both": [substantially_preserved(5, 20), keeps_em_dash,
                 contains("Tell us what you think", "an amalgam uniquely your own")],
        "skill": [has_mode("B")],
    },
}


def main():
    case, arm, out_file, case_file = sys.argv[1:5]
    raw = open(out_file).read()
    body = strip_triage(raw)
    original = open(case_file).read()
    spec = CHECKS[case]
    failed = 0
    for fn in spec.get("both", []):
        ok, label = fn(body, original)
        print(f"{'PASS' if ok else 'FAIL'} {case} [{arm}] {label}")
        failed += 0 if ok else 1
    if arm == "skill":
        for fn in spec.get("skill", []):
            ok, label = fn(raw, original)
            print(f"{'PASS' if ok else 'FAIL'} {case} [{arm}] {label}")
            failed += 0 if ok else 1
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
