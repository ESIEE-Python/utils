#!/bin/bash

set -e

# --- Usage function ---
usage() {
  echo "Usage: $0 <glob-pattern> <replacement-file> [--replace]"
  echo
  echo "By default, this script runs in dry-run mode."
  echo "Use --replace to actually overwrite matching files."
  echo
  echo "Examples:"
  echo "  $0 '**/config.json' ./new-config.json       # dry run"
  echo "  $0 '**/config.json' ./new-config.json --replace  # real replacement"
  exit 1
}

# --- Validate arguments ---
if [[ "$#" -lt 2 || "$#" -gt 3 ]]; then
  usage
fi

pattern=$1
replacement=$2
do_replace=false

if [[ "$3" == "--replace" ]]; then
  do_replace=true
elif [[ -n "$3" ]]; then
  echo "Unknown option: $3"
  usage
fi

# --- Check replacement file exists ---
if [ ! -f "$replacement" ]; then
  echo "Error: Replacement file '$replacement' does not exist."
  exit 2
fi

# --- Enable globstar for recursive globs ---
shopt -s globstar nullglob

# --- Find matched files ---
matched_files=($pattern)

if [ ${#matched_files[@]} -eq 0 ]; then
  echo "No files matched pattern '$pattern'"
  exit 0
fi

echo "Matched ${#matched_files[@]} file(s) for pattern '$pattern':"

# --- Process matches ---
for file in "${matched_files[@]}"; do
  if $do_replace; then
    echo "Replacing: $file ← $replacement"
    cp -v "$replacement" "$file"
  else
    echo "[Dry Run] Would replace: $file ← $replacement"
  fi
done

# --- Done message ---
if $do_replace; then
  echo "✅ Replacement complete."
else
  echo "✅ Dry run complete. No files were modified."
fi