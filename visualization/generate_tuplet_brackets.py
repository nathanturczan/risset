#!/usr/bin/env python3
"""
Generate tuplet bracket assets with transparent backgrounds.
Creates both upward and downward facing brackets for numbers 1-9.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path


def generate_bracket(number, facing='down', output_path=None):
    """
    Generate a single tuplet bracket image.

    Args:
        number: The tuplet number (1-9)
        facing: 'down' or 'up'
        output_path: Where to save the PNG
    """
    fig, ax = plt.subplots(figsize=(2, 0.8))

    # Transparent background
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)

    # Bracket dimensions
    bracket_width = 1.6
    bracket_height = 0.15
    tick_height = 0.12
    line_width = 2.5

    x_start = 0.2
    x_end = x_start + bracket_width
    x_mid = (x_start + x_end) / 2

    if facing == 'down':
        # Downward facing bracket: ticks go down, number above
        y_line = 0.55
        y_tick_end = y_line - tick_height
        y_text = y_line + 0.15

        # Draw bracket (horizontal line with downward ticks)
        # Left tick
        ax.plot([x_start, x_start], [y_line, y_tick_end], 'k-', linewidth=line_width)
        # Right tick
        ax.plot([x_end, x_end], [y_line, y_tick_end], 'k-', linewidth=line_width)
        # Horizontal line (two segments with gap for number)
        gap = 0.25
        ax.plot([x_start, x_mid - gap], [y_line, y_line], 'k-', linewidth=line_width)
        ax.plot([x_mid + gap, x_end], [y_line, y_line], 'k-', linewidth=line_width)

    else:  # up
        # Upward facing bracket: ticks go up, number below
        y_line = 0.35
        y_tick_end = y_line + tick_height
        y_text = y_line - 0.18

        # Draw bracket (horizontal line with upward ticks)
        # Left tick
        ax.plot([x_start, x_start], [y_line, y_tick_end], 'k-', linewidth=line_width)
        # Right tick
        ax.plot([x_end, x_end], [y_line, y_tick_end], 'k-', linewidth=line_width)
        # Horizontal line (two segments with gap for number)
        gap = 0.25
        ax.plot([x_start, x_mid - gap], [y_line, y_line], 'k-', linewidth=line_width)
        ax.plot([x_mid + gap, x_end], [y_line, y_line], 'k-', linewidth=line_width)

    # Add number
    ax.text(x_mid, y_text, str(number), fontsize=18, fontweight='bold',
            ha='center', va='center', color='black')

    # Remove axes
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 0.8)
    ax.axis('off')

    # Save with transparency
    plt.savefig(output_path, dpi=150, transparent=True, bbox_inches='tight', pad_inches=0.05)
    plt.close()

    print(f"Generated: {output_path}")


def main():
    """Generate all tuplet bracket assets."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'tuplet_brackets')

    os.makedirs(output_dir, exist_ok=True)

    # Generate brackets 1-9 in both directions
    for n in range(1, 10):
        # Downward facing
        down_path = os.path.join(output_dir, f'tuplet_{n}_down.png')
        generate_bracket(n, facing='down', output_path=down_path)

        # Upward facing
        up_path = os.path.join(output_dir, f'tuplet_{n}_up.png')
        generate_bracket(n, facing='up', output_path=up_path)

    print(f"\nGenerated {18} tuplet bracket images in {output_dir}")


if __name__ == '__main__':
    main()
