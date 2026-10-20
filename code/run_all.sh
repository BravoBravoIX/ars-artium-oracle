#!/usr/bin/env bash
# Rerun the whole study from the fetched sources.
# Usage: code/run_all.sh SOURCE_DIR [WORK_DIR]    (SOURCE_DIR filled by scripts/fetch_sources.sh;
#        WORK_DIR, default work/, holds the Latin reference text; git ignores it)
# Needs uv, which supplies Python 3.13 (set PYTHON to use another Python 3.11 or later). The
# code uses the standard library only. CPU only, under a minute.
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$(cd "$1" && pwd)"
WORK="${2:-$HERE/work}"
mkdir -p "$WORK"
WORK="$(cd "$WORK" && pwd)"
PY="${PYTHON:-uv run --no-project --python 3.13 python}"
cd "$HERE"
$PY code/build_corpus.py "$SRC" "$WORK"
# Test 1 (operations 1-2 against the worked numbers; descriptive)
$PY code/reproduce.py > /dev/null
# Tests 2-4 (letter count, Latin-likeness with controls, sensitivity; pre-registered)
WORK_DIR="$WORK" nice -n 19 $PY code/tests.py > /dev/null
# Tests 6-11 (stages 3-7 against the example sheets; pre-registered) and the exploratory look at D
nice -n 19 $PY code/stage_tests.py > /dev/null
$PY code/explore_d.py > /dev/null
# Agreement of the two transcription passes
$PY code/passes.py > /dev/null
$PY code/run_records.py "$SRC" "$WORK"
echo "done: results/*.json"
