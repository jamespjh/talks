#!/bin/bash

# Render all .fen files in sources/chess to SVG files in generated
# Usage: ./render_chess.sh

set -u

echo "Rendering all .fen files to SVG..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/sources/chess"
OUTPUT_DIR="$SCRIPT_DIR/generated"

mkdir -p "$OUTPUT_DIR"

found_any=0
for fenfile in "$SOURCE_DIR"/*.fen; do
    if [[ -f "$fenfile" ]]; then
        found_any=1
        base_name="$(basename "$fenfile" .fen)"
        output_file="$OUTPUT_DIR/${base_name}.svg"

        echo "Processing $(basename "$fenfile")..."

        # Read the first non-empty, non-comment line as FEN content.
        fen_line="$(grep -Ev '^[[:space:]]*(#|$)' "$fenfile" | head -n 1)"

        if [[ -z "$fen_line" ]]; then
            echo "✗ Failed to create $output_file (no FEN found in file)"
            continue
        fi

        talks_chess "$fen_line" > "$output_file"

        if [ $? -eq 0 ]; then
            echo "✓ Successfully created $output_file"
        else
            echo "✗ Failed to create $output_file"
        fi
    fi
done

if [ "$found_any" -eq 0 ]; then
    echo "No .fen files found in $SOURCE_DIR"
fi

echo "Done!"
