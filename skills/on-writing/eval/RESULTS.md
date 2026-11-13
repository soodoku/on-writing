# Eval results - 2026-07-19

Seven fixed cases, each run headlessly two ways: a **baseline** arm ("edit the following text to improve it", no skill) and a **skill** arm (invoke the installed on-writing skill). Outputs are scored by the mechanical checks in `checks.py`; the triage line is stripped before content checks. Model: Claude Code defaults on the date above.

## Score

| Case | Baseline | Skill |
|---|---|---|
| buried-lede-abstract | FAIL (kept em dashes) | PASS (finding moved to line 1, Mode A, no dashes, tells gone) |
| human-vignette | FAIL (16 changed words) | PASS (returned verbatim, Mode B) |
| luskin-passage | FAIL (29 changed words) | PASS (2 small edits, opener and em dash kept, Mode B) |
| marketing-slop | FAIL (kept em dashes) | PASS (all slop vocabulary and formulas gone) |
| medium-email | FAIL (kept em dash) | PASS (only the counted tells fixed, anchors intact) |
| meta-jargon | PASS | PASS (meta-nouns 9 → 2 vs baseline's 9 → 5) |
| passive-docs | FAIL (kept bold-header list, passive fragments) | PASS (prose, actors as subjects, Mode A) |
| **Total** | **1/7** | **7/7** |

The baseline's characteristic failures are the ones the skill exists to fix: it polishes human drafts it should leave alone (16 and 29 changed words on the two human-written cases) and it does not treat em dashes or bold-header lists as defects.

## Iterations (RED → GREEN → REFACTOR)

1. **RED.** Baseline run before the skill existed: 1/7.
2. First skill draft: behaviorally correct on all cases, but the harness scored the triage preamble as content; checks were fixed to score only the delivered text.
3. **REFACTOR 1.** Mode B cut Luskin's "Tell us what you think!" as a "stray opener." Added: an edit needs a nameable defect; direct address, exclamations, and opinionated openers are voice, not clutter. The opener survived the re-run.
4. **REFACTOR 2.** One run paraphrased the triage ("hands-off edit") instead of naming the mode; the process step now pins the shape (`Triage:` prefix, mode by name).
5. **REFACTOR 3.** A fresh run under-triaged the docs case (kept the bold-header list) because Step 0's countable tells omitted formatting tells; subjectless passive fragments and bold-header label echoes were added to the count. Re-run passed.
6. **GREEN.** Final: skill 7/7, baseline 1/7. Six outputs come from the last full skill-arm run; passive-docs was re-run after iteration 5.

## Reproduce

```bash
./run.sh baseline   # with the skill uninstalled
./run.sh skill      # with skill installed in ~/.claude/skills/on-writing
./run.sh check skill
```

Caveats: single run per case per arm (behavior varies across runs; iteration 5 exists because of exactly that), checks are mechanical proxies, and `out/` is untracked.


---

# Eval results - 2026-07-29 (after the argument-craft revision)

The revision added Luskin's remaining rules (O6-O8, S5, W6-W7), a numbers/tables/figures
pass distilled from Cochrane and the *QJPS* guidelines, Shafer's opening-as-filter rule,
and `references/argument-craft.md`. SKILL.md grew from 73 to ~100 lines.

## What the re-run found

Two regressions, both predicted by the shape of the change, and both traced rather than
waved off as variance.

**1. Pass 3 lost salience (`passive-docs`).** The first re-run emitted a bold-header list,
the exact tell the pass bans. Three repeat runs: 1 fail, 2 pass. Adding ~25 lines of inline
Mode A rules diluted a sweep that was already only a prose paragraph pointing at a reference
file. **Fix:** an explicit output check in the process step, listing the hard bans (no
em/en dashes, no bold-header lists, no sentence-initial "However,") to verify before
delivering. Four runs after the fix: 4/4 clean.

**2. Mode B got more aggressive (`luskin-passage`).** A human expert draft that previously
took 2 edits took 6. More rules inline reads as more license to edit. **Fix:** Pass 1 and
Pass 2 are labeled Mode A passes, and Mode B now states that a rule below justifies an edit
only if you can also name what the line does wrong for the reader. Four runs after the fix:
3/4 pass, typical 3-4 edits and 12-14 changed words.

**Honest accounting:** the mitigation is partial. Typical Mode B edits on this case went from
2 to 3-4, and one run in four still exceeds the threshold. The revision buys Mode A capability
at some cost in Mode B restraint. Worth watching if more inline rules are ever added.

## An unresolved conflict the eval surfaced

`medium-email` fails `no_dashes` because the author's own correctly-used em dash survives.
That is now *deliberate*: the 3-4 band says author punctuation stays unless it was one of the
counted tells, and a single correct dash is voice rather than a tell - only clusters count.
Before the revision the skill was silent on this, and behavior flipped run to run depending
on whether a run happened to count the dash (verified: 3 runs, 2 kept it, 1 removed it).

The skill is now self-consistent; the check is not. Either the case's `no_dashes` check should
be dropped, or the rule should count single dashes in the middle band. That is a judgment call
about what the case is for, so it is flagged rather than silently changed.
