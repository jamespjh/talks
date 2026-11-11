#!/bin/bash

# Render the .dot files in sources/graphviz and the charts in sources/charts to SVG in generated/.
# Usage: ./render_diagrams.sh

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/sources/graphviz"
OUTPUT_DIR="$SCRIPT_DIR/generated"
mkdir -p "$OUTPUT_DIR"

status=0
for dotfile in "$SOURCE_DIR"/*.dot; do
    name="$(basename "$dotfile" .dot)"
    if dot -Tsvg -o "$OUTPUT_DIR/$name.svg" "$dotfile"; then
        echo "✓ $name.svg"
    else
        echo "✗ Failed to create $name.svg"; status=1
    fi
done

if python3 "$SCRIPT_DIR/sources/charts/charts.py" "$OUTPUT_DIR"; then
    echo "✓ leaderboard.svg, fully_open.svg"
else
    echo "✗ Failed to draw the charts"; status=1
fi

exit $status
