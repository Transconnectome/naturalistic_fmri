#!/usr/bin/env bash
# Upload top 100 naturalistic fMRI PDFs to NotebookLM
set -u

NOTEBOOK_ID="d9265824-3383-4fd4-8d17-03512a338ee5"
NLM="/home/juke/superclaude-env/bin/nlm"
TOP_LIST="/home/juke/naturalistic_fmri_pdfs/top100_paths.json"
LOG="/home/juke/naturalistic_fmri_pdfs/upload.log"
FAIL_LOG="/home/juke/naturalistic_fmri_pdfs/upload_fail.log"

: > "$LOG"
: > "$FAIL_LOG"

# Extract paths from JSON
mapfile -t PATHS < <(python3 -c "import json; [print(p) for p in json.load(open('$TOP_LIST'))]")

echo "Uploading ${#PATHS[@]} PDFs to notebook $NOTEBOOK_ID"
echo "Started at: $(date)"

upload_one() {
  local idx="$1"
  local path="$2"
  local basename=$(basename "$path")
  local result
  if result=$("$NLM" source add "$NOTEBOOK_ID" --file "$path" 2>&1); then
    echo "[$idx] OK: $basename" | tee -a "$LOG"
  else
    echo "[$idx] FAIL: $basename :: $result" | tee -a "$FAIL_LOG"
  fi
}

export -f upload_one
export NLM NOTEBOOK_ID LOG FAIL_LOG

# Upload with limited concurrency (4 parallel) using xargs
# But we need indexing, so let's do simpler sequential approach with progress
for i in "${!PATHS[@]}"; do
  idx=$((i + 1))
  path="${PATHS[$i]}"
  upload_one "$idx" "$path" &
  # Limit concurrency to 4
  if (( idx % 4 == 0 )); then
    wait
  fi
done
wait  # wait for final batch

echo ""
echo "Done at: $(date)"
echo "Summary:"
echo "  Successful: $(wc -l < "$LOG")"
echo "  Failed: $(wc -l < "$FAIL_LOG")"
