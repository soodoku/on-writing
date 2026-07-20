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
