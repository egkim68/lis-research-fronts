#!/usr/bin/env bash
# Reproduce every number, table, and figure in the manuscript.
# Usage: bash run_all.sh <folder with the ten yearly Scopus CSVs> <empty work folder> [2026 partial CSV]
# Example: bash run_all.sh data/scopus_raw work data/scopus_2026_partial/scopus_SJR_LIS_2026_partial_exported_2026-10-24.csv
set -euo pipefail
SRC=$(cd "$1" && pwd); WORK=$2; EXTRA=${3:-}; ROOT=$(cd "$(dirname "$0")" && pwd); CODE=$ROOT/code; ORDER=$ROOT/eid_order.csv
[[ -n "$EXTRA" ]] && EXTRA=$(cd "$(dirname "$EXTRA")" && pwd)/$(basename "$EXTRA")
mkdir -p "$WORK"; cd "$WORK"; export PYTHONPATH="$CODE"
for s in "00_merge_exports.py:$SRC $ORDER" 01_prep.py 02_lexical.py 03_flags.py 04_production.py 05_embed_graph.py "06_leiden.py:1.5 3 6 12 20" \
         07_fronts.py 08_topics.py 09_test_2025.py 10_validate_tiers.py 11_thresholds.py 12_figure_data.py 13_figures.py; do
  f=${s%%:*}; a=""; [[ "$s" == *:* ]] && a=${s#*:}
  echo "== $f $a"; python3 -W ignore "$CODE/$f" $a
done
if [[ -n "$EXTRA" ]]; then echo "== 14_early_2026.py"; python3 -W ignore "$CODE/14_early_2026.py" "$EXTRA"; fi
echo "Done. Outputs are in $WORK; manuscript figures are in $WORK/figs/."
