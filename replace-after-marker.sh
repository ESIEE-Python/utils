#!/bin/bash
# Usage: ./replace_after_marker.sh "MARKER" file1 [file2 ...] replacement_file

if [ $# -lt 3 ]; then
    echo "Usage: $0 MARKER file1 [file2 ...] replacement_file"
    exit 1
fi

marker="$1"
replacement="${@: -1}" # last argument is the replacement file
shift # remove marker
set -- "$@" # reset positional parameters
files=("${@:1:$#-1}") # all args except last are files

for f in "${files[@]}"; do
    if [[ ! -f "$f" ]]; then
        echo "File not found: $f"
        continue
    fi

    awk -v marker="$marker" -v repl="$replacement" '
        $0 ~ marker {
            print # keep the marker line
            while ((getline line < repl) > 0) print line
            exit
        }
        { print }
    ' "$f" > "$f.tmp" && mv "$f.tmp" "$f"

    echo "Updated: $f"
done