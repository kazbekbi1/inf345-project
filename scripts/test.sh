#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

set +e
output=$(python3 -m unittest discover -s tests -t . 2>&1)
status=$?
set -e

echo "$output"
total=$(echo "$output" | sed -n 's/^Ran \([0-9]*\) test.*/\1/p')
total=${total:-0}

if [ "$status" -eq 0 ]; then
  echo "TESTS: $total/$total"
else
  echo "TESTS: 0/$total"
  exit 1
fi
