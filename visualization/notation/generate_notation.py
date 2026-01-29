#!/usr/bin/env python3
"""
Generate LilyPond notation files for all example Risset rhythms.
"""

import subprocess
import os

# Ratios to generate
RATIOS = [
    (2, 1), (3, 1), (3, 2), (4, 3), (5, 3),
    (5, 4), (6, 5), (7, 4), (7, 5), (8, 5)
]

DIRECTIONS = ["accel", "decel"]
MEASURES = 4  # Single metabar for cleaner notation
BPM = 120

def main():
    # Create notation directory
    notation_dir = os.path.join(os.path.dirname(__file__), "notation")
    os.makedirs(notation_dir, exist_ok=True)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    risset_path = os.path.join(script_dir, "risset.py")

    generated = []

    for direction in DIRECTIONS:
        for ratio_num, ratio_den in RATIOS:
            # For accel, we need to invert the ratio input
            if direction == "accel":
                input_num, input_den = ratio_den, ratio_num
            else:
                input_num, input_den = ratio_num, ratio_den

            filename = f"risset_{ratio_num}-{ratio_den}_{direction}"
            output_path = os.path.join(notation_dir, f"{filename}.mid")

            cmd = [
                "python3", risset_path,
                "--ratio", f"{input_num}/{input_den}",
                "--direction", direction,
                "--measures", str(MEASURES),
                "--bpm", str(BPM),
                "--ramp",  # Single metabar for cleaner notation
                "--lilypond",
                "-o", output_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                generated.append(f"{filename}.ly")
                print(f"Generated: {filename}.ly")
            else:
                print(f"Error generating {filename}: {result.stderr}")

    print(f"\nGenerated {len(generated)} LilyPond files in notation/")
    print("\nTo render all to PNG, run:")
    print("  ./render_notation.sh")


if __name__ == "__main__":
    main()
