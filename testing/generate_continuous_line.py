#!/usr/bin/env python3
"""
Generate the "ideal" continuous line for a Risset rhythm.

This represents what the merged Layer2-bar1 + Layer1-bar2 SHOULD look like
when generated from pure algorithmic principles.

For decel with ratio 8/5:
- Bar 1 (Layer 2): 192 → 120 BPM, velocity fading IN (1 → 127)
- Bar 2 (Layer 1): 120 → 75 BPM, velocity fading OUT (127 → 1)

The continuous line spans 2 meta-bars with a smooth tempo transition.
"""

import argparse
from midiutil import MIDIFile
import math


def generate_continuous_line(
    bpm=120.0,
    num_measures=4,  # per meta-bar (so 2x this for full line)
    ratio_num=8,
    ratio_den=5,
    direction="decel",
    pitch=64,  # E3
    output_file="continuous_line.mid"
):
    """
    Generate the ideal continuous line spanning 2 meta-bars.
    """

    # Calculate total duration per meta-bar
    beats_per_measure = 4  # Assuming 4/4
    beats_per_metabar = beats_per_measure * num_measures
    total_beats = beats_per_metabar * 2  # Two meta-bars

    # Calculate ratio
    ratio_value = ratio_num / ratio_den
    if ratio_value < 1:
        ratio_value = 1 / ratio_value

    # Determine tempo curve for the full continuous line
    # For decel: fast → base → slow (over 2 meta-bars)
    # For accel: slow → base → fast (over 2 meta-bars)

    if direction == "decel":
        # Bar 1: fast → base (Layer 2's tempo curve)
        # Bar 2: base → slow (Layer 1's tempo curve)
        tempo_fast = bpm * ratio_value
        tempo_base = bpm
        tempo_slow = bpm / ratio_value

        def get_tempo(t):
            if t < beats_per_metabar:
                # First half: fast → base
                progress = t / beats_per_metabar
                return tempo_fast + (tempo_base - tempo_fast) * progress
            else:
                # Second half: base → slow
                progress = (t - beats_per_metabar) / beats_per_metabar
                return tempo_base + (tempo_slow - tempo_base) * progress

        def get_velocity(t):
            if t < beats_per_metabar:
                # First half: fading IN (1 → 127)
                progress = t / beats_per_metabar
                return max(1, int(1 + 126 * progress))
            else:
                # Second half: fading OUT (127 → 1)
                progress = (t - beats_per_metabar) / beats_per_metabar
                return max(1, int(127 - 126 * progress))

    else:  # accel
        # Bar 1: slow → base (Layer 2's tempo curve)
        # Bar 2: base → fast (Layer 1's tempo curve)
        tempo_slow = bpm / ratio_value
        tempo_base = bpm
        tempo_fast = bpm * ratio_value

        def get_tempo(t):
            if t < beats_per_metabar:
                # First half: slow → base
                progress = t / beats_per_metabar
                return tempo_slow + (tempo_base - tempo_slow) * progress
            else:
                # Second half: base → fast
                progress = (t - beats_per_metabar) / beats_per_metabar
                return tempo_base + (tempo_fast - tempo_base) * progress

        def get_velocity(t):
            if t < beats_per_metabar:
                # First half: fading IN (1 → 127)
                progress = t / beats_per_metabar
                return max(1, int(1 + 126 * progress))
            else:
                # Second half: fading OUT (127 → 1)
                progress = (t - beats_per_metabar) / beats_per_metabar
                return max(1, int(127 - 126 * progress))

    # Create MIDI file
    midi = MIDIFile(1)
    track = 0
    channel = 0
    midi.addTempo(track, 0, bpm)
    midi.addTimeSignature(track, 0, 4, 2, 24, 8)  # 4/4

    # Generate notes using phase accumulation
    time_step = 0.01
    current_time = 0.0
    phase = 0.0
    notes = []

    # First note at time 0
    notes.append((0.0, get_velocity(0.0)))

    while current_time < total_beats:
        current_tempo = get_tempo(current_time)
        phase_increment = (current_tempo / bpm) * time_step

        old_phase = phase
        phase += phase_increment

        if int(phase) > int(old_phase):
            if current_time > 0.001:
                notes.append((current_time, get_velocity(current_time)))
            phase = phase - int(phase)

        current_time += time_step

    # Add notes to MIDI
    for i, (t, velocity) in enumerate(notes):
        if t >= total_beats:
            continue

        # Duration until next note
        if i < len(notes) - 1:
            next_time = notes[i + 1][0]
            duration = (next_time - t) * 0.8
        else:
            duration = min(1.0, total_beats - t - 0.2)

        if duration > 0.01:
            midi.addNote(track, channel, pitch, t, duration, velocity)

    # Write file
    with open(output_file, "wb") as f:
        midi.writeFile(f)

    print(f"Generated: {output_file}")
    print(f"  Total beats: {total_beats} (2 x {beats_per_metabar} beat meta-bars)")
    print(f"  Direction: {direction}")
    print(f"  Ratio: {ratio_num}/{ratio_den} ({ratio_value:.3f})")

    if direction == "decel":
        print(f"  Tempo curve: {tempo_fast:.1f} → {tempo_base:.1f} → {tempo_slow:.1f} BPM")
    else:
        print(f"  Tempo curve: {tempo_slow:.1f} → {tempo_base:.1f} → {tempo_fast:.1f} BPM")

    print(f"  Notes generated: {len(notes)}")

    # Print note times around the seam for debugging
    print(f"\n  Notes around the seam (beat {beats_per_metabar}):")
    for t, v in notes:
        if beats_per_metabar - 2 < t < beats_per_metabar + 2:
            print(f"    t={t:.3f}, vel={v}")

    return notes


def analyze_and_compare(risset_file, continuous_file, beats_per_metabar=16):
    """
    Analyze the Risset output and compare to the ideal continuous line.

    Reconstructs the continuous line from Risset by:
    - Taking Layer 2 (high pitch) notes from bar 1
    - Taking Layer 1 (low pitch) notes from bar 1, shifting by +beats_per_metabar
    - Merging to form the reconstructed continuous line
    """
    try:
        from mido import MidiFile
    except ImportError:
        print("mido not installed, skipping analysis")
        return

    print(f"\n{'='*60}")
    print("COMPARISON: Risset output vs Ideal continuous line")
    print(f"{'='*60}")

    # Parse MIDI file with pitch info
    def parse_midi_with_pitch(filepath):
        mid = MidiFile(filepath)
        notes = []
        current_time = 0
        ticks_per_beat = mid.ticks_per_beat
        active_notes = {}

        for track in mid.tracks:
            current_time = 0
            for msg in track:
                current_time += msg.time
                time_beats = current_time / ticks_per_beat

                if msg.type == 'note_on' and msg.velocity > 0:
                    active_notes[msg.note] = (time_beats, msg.velocity)
                elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                    if msg.note in active_notes:
                        start, vel = active_notes[msg.note]
                        notes.append((start, msg.note, vel, time_beats - start))
                        del active_notes[msg.note]

        notes.sort(key=lambda x: x[0])
        return notes

    risset_notes = parse_midi_with_pitch(risset_file)
    continuous_notes = parse_midi_with_pitch(continuous_file)

    # Separate Risset into layers by pitch
    pitches = sorted(set(n[1] for n in risset_notes))
    if len(pitches) >= 2:
        pitch_low, pitch_high = pitches[0], pitches[-1]
        layer1_notes = [(t, v, d) for t, p, v, d in risset_notes if p == pitch_low]
        layer2_notes = [(t, v, d) for t, p, v, d in risset_notes if p == pitch_high]
    else:
        layer1_notes = layer2_notes = [(t, v, d) for t, p, v, d in risset_notes]

    # Reconstruct continuous line from Risset:
    # - Layer 2 from bar 1 (fading in)
    # - Layer 1 from bar 1, shifted by +beats_per_metabar (fading out in bar 2)
    reconstructed = []
    for t, v, d in layer2_notes:
        reconstructed.append((t, v, d, "L2"))
    for t, v, d in layer1_notes:
        reconstructed.append((t + beats_per_metabar, v, d, "L1"))
    reconstructed.sort(key=lambda x: x[0])

    print(f"\nRisset file: {len(risset_notes)} notes (L1: {len(layer1_notes)}, L2: {len(layer2_notes)})")
    print(f"Continuous file: {len(continuous_notes)} notes")
    print(f"Reconstructed continuous: {len(reconstructed)} notes")

    # Show notes around the seam in RECONSTRUCTED continuous line
    print(f"\nNotes around seam (beat {beats_per_metabar}) in RECONSTRUCTED line:")
    for t, v, d, layer in reconstructed:
        if beats_per_metabar - 2 < t < beats_per_metabar + 2:
            print(f"  t={t:.3f}, vel={v}, dur={d:.3f}, end={t+d:.3f} ({layer})")

    print(f"\nNotes around seam (beat {beats_per_metabar}) in IDEAL continuous line:")
    for t, p, v, d in continuous_notes:
        if beats_per_metabar - 2 < t < beats_per_metabar + 2:
            print(f"  t={t:.3f}, vel={v}, dur={d:.3f}, end={t+d:.3f}")

    # Calculate gaps around seam
    print(f"\nGap analysis around seam:")

    recon_for_gaps = [(t, v, d) for t, v, d, _ in reconstructed]
    cont_for_gaps = [(t, v, d) for t, p, v, d in continuous_notes]

    for name, notes in [("Reconstructed", recon_for_gaps), ("Ideal", cont_for_gaps)]:
        gaps = []
        for i in range(len(notes) - 1):
            if beats_per_metabar - 3 < notes[i][0] < beats_per_metabar + 3:
                gap = notes[i+1][0] - notes[i][0]
                gaps.append((notes[i][0], gap))

        print(f"\n  {name} gaps:")
        for t, gap in gaps:
            marker = " <-- SEAM" if t < beats_per_metabar <= t + gap else ""
            print(f"    at t={t:.3f}: gap={gap:.3f}{marker}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate ideal continuous line for Risset rhythm"
    )

    parser.add_argument("--bpm", type=float, default=120.0)
    parser.add_argument("--measures", type=int, default=4)
    parser.add_argument("--ratio", type=str, default="8/5")
    parser.add_argument("--direction", type=str, default="decel",
                        choices=["accel", "decel"])
    parser.add_argument("--pitch", type=int, default=64)
    parser.add_argument("-o", "--output", type=str, default=None)
    parser.add_argument("--compare", type=str, default=None,
                        help="Risset MIDI file to compare against")

    args = parser.parse_args()

    ratio_parts = args.ratio.split("/")
    ratio_num = int(ratio_parts[0])
    ratio_den = int(ratio_parts[1])

    if args.output is None:
        args.output = f"continuous_{ratio_num}-{ratio_den}_{args.direction}.mid"

    generate_continuous_line(
        bpm=args.bpm,
        num_measures=args.measures,
        ratio_num=ratio_num,
        ratio_den=ratio_den,
        direction=args.direction,
        pitch=args.pitch,
        output_file=args.output
    )

    if args.compare:
        analyze_and_compare(args.compare, args.output, args.measures * 4)
