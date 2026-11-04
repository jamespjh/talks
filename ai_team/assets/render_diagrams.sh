#!/bin/bash

# Render all .dot files in sources/graphviz to SVG in generated/,
# plus, for diagrams with role= tags, one copy per highlighted piece (<name>_<role>.svg).
# Usage: ./render_diagrams.sh

set -uo pipefail
echo "Rendering all .dot files to SVG..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/sources/graphviz"
OUTPUT_DIR="$SCRIPT_DIR/generated"
mkdir -p "$OUTPUT_DIR"

# Diagrams with logos reference sized copies by relative path; logos.py then inlines them
cd "$OUTPUT_DIR"
python3 "$SCRIPT_DIR/sources/logos.py" prepare logos-sized
with_logos() { if grep -q "<image" "$1"; then python3 "$SCRIPT_DIR/sources/logos.py" inline "$1"; fi; }

status=0
for dotfile in "$SOURCE_DIR"/*.dot; do
    name="$(basename "$dotfile" .dot)"
    if dot -Tsvg -o "$OUTPUT_DIR/$name.svg" "$dotfile" && with_logos "$OUTPUT_DIR/$name.svg"; then
        echo "✓ $name.svg"
    else
        echo "✗ Failed to create $name.svg"; status=1
    fi
done

# Any diagram whose nodes carry role="..." also gets one copy per role with that piece lit up
for dotfile in $(grep -l 'role="' "$SOURCE_DIR"/*.dot); do
    name="$(basename "$dotfile" .dot)"
    for role in $(grep -o 'role="[a-z]*"' "$dotfile" | sort -u | sed -E 's/role="([a-z]*)"/\1/'); do
        if gvpr -c -a "$role" -f "$SCRIPT_DIR/sources/highlight.g" "$dotfile" \
            | dot -Tsvg -o "$OUTPUT_DIR/${name}_$role.svg" && with_logos "$OUTPUT_DIR/${name}_$role.svg"; then
            echo "✓ ${name}_$role.svg"
        else
            echo "✗ Failed to create ${name}_$role.svg"; status=1
        fi
    done
done

echo "Done!"
exit $status
