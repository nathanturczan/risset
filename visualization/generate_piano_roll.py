#!/usr/bin/env python3
"""
Generate piano roll visualizations for Risset rhythm MIDI files.

Creates PNG images showing:
- Two rows (one per pitch)
- Velocity as color intensity
- Measure lines
- Tempo marking (120 BPM)
"""

import os
import sys
from mido import MidiFile
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


def parse_midi_notes(filepath):
    """
    Parse MIDI file and extract notes with timing, pitch, velocity, duration.
    Returns list of (start_beat, pitch, velocity, duration_beats) tuples.
    """
    mid = MidiFile(filepath)
    ticks_per_beat = mid.ticks_per_beat

    notes = []
    active_notes = {}  # pitch -> (start_time, velocity)
    current_tick = 0

    for track in mid.tracks:
        current_tick = 0
        for msg in track:
            current_tick += msg.time
            time_beats = current_tick / ticks_per_beat

            if msg.type == 'note_on' and msg.velocity > 0:
                active_notes[msg.note] = (time_beats, msg.velocity)
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                if msg.note in active_notes:
                    start, vel = active_notes[msg.note]
                    duration = time_beats - start
                    notes.append((start, msg.note, vel, duration))
                    del active_notes[msg.note]

    return notes


def generate_piano_roll(midi_path, output_path, title=None):
    """
    Generate a piano roll PNG for a Risset rhythm MIDI file.
    """
    notes = parse_midi_notes(midi_path)

    if not notes:
        print(f"No notes found in {midi_path}")
        return False

    # Get unique pitches and sort them
    pitches = sorted(set(n[1] for n in notes))
    pitch_to_row = {p: i for i, p in enumerate(pitches)}

    # Determine total duration
    max_time = max(n[0] + n[3] for n in notes)
    total_beats = np.ceil(max_time / 4) * 4  # Round up to nearest 4 beats
    num_measures = int(total_beats / 4)

    # Create figure
    fig_width = max(12, num_measures * 2.5)
    fig_height = 2.5
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    # Color map for velocity (light pink to dark red)
    colors_low = [(1.0, 0.9, 0.9)]   # Very light pink for vel=1
    colors_high = [(0.8, 0.1, 0.2)]  # Dark red for vel=127
    cmap = LinearSegmentedColormap.from_list('velocity',
        [(0, colors_low[0]), (1, colors_high[0])])

    # Plot each note as a rectangle
    row_height = 0.8
    for start, pitch, velocity, duration in notes:
        row = pitch_to_row[pitch]

        # Normalize velocity to 0-1 for color
        vel_norm = (velocity - 1) / 126  # vel ranges 1-127
        color = cmap(vel_norm)

        rect = patches.Rectangle(
            (start, row + 0.1),
            duration,
            row_height,
            linewidth=0.5,
            edgecolor='black',
            facecolor=color
        )
        ax.add_patch(rect)

    # Draw measure lines
    for measure in range(num_measures + 1):
        beat = measure * 4
        ax.axvline(x=beat, color='black', linewidth=1.5, zorder=1)

    # Draw beat lines (lighter)
    for beat in range(int(total_beats) + 1):
        if beat % 4 != 0:  # Skip measure lines
            ax.axvline(x=beat, color='gray', linewidth=0.5, linestyle='--', alpha=0.5, zorder=0)

    # Labels
    pitch_names = {60: 'C3', 64: 'E3'}  # Default pitches
    y_labels = [pitch_names.get(p, f'P{p}') for p in pitches]

    ax.set_yticks([i + 0.5 for i in range(len(pitches))])
    ax.set_yticklabels(y_labels, fontsize=12, fontweight='bold')

    # X-axis: show measure numbers
    ax.set_xticks([m * 4 for m in range(num_measures + 1)])
    ax.set_xticklabels([str(m + 1) for m in range(num_measures + 1)], fontsize=10)
    ax.set_xlabel('Measure', fontsize=11)

    # Set limits
    ax.set_xlim(0, total_beats)
    ax.set_ylim(0, len(pitches))

    # Title with tempo
    if title:
        ax.set_title(f'{title}\n♩ = 120 BPM', fontsize=14, fontweight='bold')
    else:
        ax.set_title('♩ = 120 BPM', fontsize=12)

    # Add colorbar for velocity
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=1, vmax=127))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, aspect=10, pad=0.02)
    cbar.set_label('Velocity', fontsize=10)

    # Tight layout
    plt.tight_layout()

    # Save
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"Generated: {output_path}")
    return True


def format_title(filename):
    """
    Extract info from filename and create a nice title.
    e.g., 'risset_120bpm_2-1_accel_8m.mid' -> 'Risset 2:1 Accelerando'
    """
    base = os.path.splitext(filename)[0]
    parts = base.split('_')

    # Find ratio and direction
    ratio = None
    direction = None

    for part in parts:
        if '-' in part and part[0].isdigit():
            ratio = part.replace('-', ':')
        elif part in ['accel', 'decel']:
            direction = 'Accelerando' if part == 'accel' else 'Decelerando'

    if ratio and direction:
        return f"Risset {ratio} {direction}"
    return base


def main():
    """Generate piano rolls for all MIDI files in examples/."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    examples_dir = os.path.join(script_dir, '..', 'examples')
    output_dir = os.path.join(script_dir, 'piano_rolls')

    os.makedirs(output_dir, exist_ok=True)

    # Find all MIDI files
    midi_files = [f for f in os.listdir(examples_dir) if f.endswith('.mid')]

    if not midi_files:
        print(f"No MIDI files found in {examples_dir}")
        return

    print(f"Found {len(midi_files)} MIDI files")

    for midi_file in sorted(midi_files):
        midi_path = os.path.join(examples_dir, midi_file)
        output_name = os.path.splitext(midi_file)[0] + '.png'
        output_path = os.path.join(output_dir, output_name)

        title = format_title(midi_file)
        generate_piano_roll(midi_path, output_path, title)

    print(f"\nGenerated {len(midi_files)} piano roll images in {output_dir}")


if __name__ == '__main__':
    main()
