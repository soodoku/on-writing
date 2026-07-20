#!/usr/bin/env bash
# Eval runner for the on-writing skill.
#
#   ./run.sh baseline   # plain "edit this" prompts, no skill (run with the skill uninstalled)
#   ./run.sh skill      # prompts that invoke the installed on-writing skill
#   ./run.sh check ARM  # re-run checks on saved outputs without calling claude
#
# Runs from $HOME so the sandbox can read ~/.claude/skills. Outputs land in eval/out/.
set -u
EVAL_DIR="$(cd "$(dirname "$0")" && pwd)"
OUT="$EVAL_DIR/out"
mkdir -p "$OUT"
ARM="${1:?usage: run.sh baseline|skill|check [arm]}"

run_arm() {
  local arm="$1"
  local pids=()
  for f in "$EVAL_DIR"/cases/*.txt; do
    local case_id
    case_id="$(basename "$f" .txt)"
    local prompt
    if [ "$arm" = "baseline" ]; then
      prompt="You are editing text. Edit the following text to improve it. Return only the final text, nothing else.

$(cat "$f")"
    else
      prompt="Use the on-writing skill to edit the following text. Return only the skill's one-line triage statement and the final text, nothing else.

$(cat "$f")"
    fi
    ( cd "$HOME" && claude -p "$prompt" < /dev/null > "$OUT/$case_id.$arm.txt" 2> "$OUT/$case_id.$arm.err" ) &
    pids+=($!)
  done
  wait "${pids[@]}"
}

check_arm() {
  local arm="$1" total=0 bad=0
  for f in "$EVAL_DIR"/cases/*.txt; do
    local case_id
    case_id="$(basename "$f" .txt)"
    [ -s "$OUT/$case_id.$arm.txt" ] || { echo "MISS $case_id [$arm] no output"; bad=$((bad+1)); continue; }
    python3 "$EVAL_DIR/checks.py" "$case_id" "$arm" "$OUT/$case_id.$arm.txt" "$f" || bad=$((bad+1))
    total=$((total+1))
  done
  echo "== $arm: $((total-bad))/$total cases fully passing =="
  [ "$bad" -eq 0 ]
}

case "$ARM" in
  baseline|skill) run_arm "$ARM"; check_arm "$ARM" ;;
  check) check_arm "${2:?arm}" ;;
  *) echo "unknown arm $ARM"; exit 2 ;;
esac
