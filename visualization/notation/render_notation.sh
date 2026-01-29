#!/bin/bash
#
# Render all LilyPond files in notation/ to PNG
#
# Requires LilyPond: brew install lilypond
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NOTATION_DIR="$SCRIPT_DIR/notation"

if ! command -v lilypond &> /dev/null; then
    echo "Error: LilyPond not found. Install with: brew install lilypond"
    exit 1
fi

cd "$NOTATION_DIR" || exit 1

count=0
for ly_file in *.ly; do
    if [ -f "$ly_file" ]; then
        echo "Rendering: $ly_file"
        lilypond --png -dpreview "$ly_file" 2>/dev/null

        # Rename preview.png to just .png for cleaner naming
        base="${ly_file%.ly}"
        if [ -f "${base}.preview.png" ]; then
            mv "${base}.preview.png" "${base}.png"
        fi

        # Clean up intermediate files
        rm -f "${base}.preview.eps" "${base}.pdf" 2>/dev/null

        ((count++))
    fi
done

# Clean up the non-preview PNG if it exists (larger, uncropped version)
for f in *.png; do
    # Keep only files that don't have .preview in the original
    true
done

echo ""
echo "Rendered $count PNG files in notation/"
