#!/usr/bin/env python3
"""
Risset rhythm generator.
Two layers with opposing tempo curves and crossfading velocities.
"""

import argparse
from midiutil import MIDIFile
import math


def generate_layer_times_forward(total_beats, base_bpm, start_tempo, end_tempo):
    """
    Generate note times for a layer, starting with a note at t=0.
    Used for Layer 1 (fades out) - needs to be loud at the START.
    """
    time_step = 0.01
    current_time = 0.0
    phase = 0.0
    times = [0.0]  # Always start with a note at t=0

    def get_tempo(t):
        progress = t / total_beats
        return start_tempo + (end_tempo - start_tempo) * progress

    while current_time < total_beats:
        current_tempo = get_tempo(current_time)
        phase_increment = (current_tempo / base_bpm) * time_step

        old_phase = phase
        phase += phase_increment

        if int(phase) > int(old_phase):
            if current_time > 0.001:  # Don't duplicate the t=0 note
                times.append(current_time)
            phase = phase - int(phase)

        current_time += time_step

    return times


def generate_layer_times_backward(total_beats, base_bpm, start_tempo, end_tempo):
    """
    Generate note times for a layer, ending with a note near total_beats.
    Used for Layer 2 (fades in) - needs to be loud at the END.

    Generates backwards from total_beats to ensure the last note
    lands close to the seam point.
    """
    time_step = 0.01
    current_time = total_beats
    phase = 0.0
    min_end_gap = 0.05  # Small gap before total_beats
    times = [total_beats - min_end_gap]  # Last note just before seam

    def get_tempo(t):
        progress = t / total_beats
        return start_tempo + (end_tempo - start_tempo) * progress

    while current_time > 0:
        current_tempo = get_tempo(current_time)
        phase_increment = (current_tempo / base_bpm) * time_step

        old_phase = phase
        phase += phase_increment

        if int(phase) > int(old_phase):
            if current_time < total_beats - 0.1:  # Don't duplicate the end note
                times.append(current_time)
            phase = phase - int(phase)

        current_time -= time_step

    times.reverse()
    return times


def generate_continuous_line_times(total_beats, base_bpm, ratio_value, direction):
    """
    Generate the continuous line spanning 2 metabars.
    This is the "ground truth" that gets split into two layers.

    For decel: tempo goes fast → base → slow
    For accel: tempo goes slow → base → fast

    IMPORTANT: Ensures a note at exactly t=total_beats (the split point)
    for seamless layer separation.

    Returns list of times over 2*total_beats.
    """
    double_beats = total_beats * 2
    time_step = 0.01
    current_time = 0.0
    phase = 0.0
    times = [0.0]

    if direction == "decel":
        tempo_start = base_bpm * ratio_value  # fast
        tempo_mid = base_bpm                   # base
        tempo_end = base_bpm / ratio_value     # slow
    else:  # accel
        tempo_start = base_bpm / ratio_value   # slow
        tempo_mid = base_bpm                   # base
        tempo_end = base_bpm * ratio_value     # fast

    def get_tempo(t):
        if t < total_beats:
            # First half: start → mid
            progress = t / total_beats
            return tempo_start + (tempo_mid - tempo_start) * progress
        else:
            # Second half: mid → end
            progress = (t - total_beats) / total_beats
            return tempo_mid + (tempo_end - tempo_mid) * progress

    while current_time < double_beats:
        current_tempo = get_tempo(current_time)
        phase_increment = (current_tempo / base_bpm) * time_step

        old_phase = phase
        phase += phase_increment

        if int(phase) > int(old_phase):
            if current_time > 0.001:
                times.append(current_time)
            phase = phase - int(phase)

        current_time += time_step

    # Note: We intentionally do NOT force a note at total_beats.
    # The phase accumulation naturally determines note positions, and
    # the velocity crossfade handles perceptual continuity at the seam.
    # Forcing a note would create rhythmic double-hits.

    return times


def split_continuous_to_layers(continuous_times, total_beats):
    """
    Split the continuous line into two layers for the Risset rhythm.

    Layer 2 = first half of continuous (fading in) - times in [0, total_beats)
    Layer 1 = second half of continuous, shifted back (fading out) - times >= total_beats

    The note at exactly t=total_beats goes to Layer 1 (becomes t=0 in Layer 1).
    This ensures seamless phase continuity at the loop seam.
    """
    # Use small epsilon for floating point comparison
    epsilon = 0.001
    split_point = total_beats - epsilon

    layer2_times = [t for t in continuous_times if t < split_point]
    layer1_times = [t - total_beats for t in continuous_times if t >= split_point]

    # Handle float precision - ensure no negative times
    layer1_times = [max(0, t) for t in layer1_times]

    return layer1_times, layer2_times


def generate_risset_rhythm(
    time_sig_num=4,
    time_sig_den=4,
    bpm=120.0,
    num_measures=4,
    ratio_num=2,
    ratio_den=1,
    direction="accel",
    note_pitch_low=60,
    note_pitch_high=64,
    output_file="risset.mid",
    ramp=False
):
    """
    Generate a Risset rhythm MIDI file with two layers.

    Arc mode (default): 2 metabars, each voice completes a full fade arc.
      - More musical, complete statement
      - Each pitch: quiet → loud → quiet (or vice versa)

    Ramp mode (--ramp): 1 metabar, a building block for composition.
      - One pitch fading out, one fading in
      - Use for transitions, stacking, layering
    """

    # Calculate duration in beats
    beats_per_measure = time_sig_num * (4.0 / time_sig_den)
    total_output_beats = beats_per_measure * num_measures

    # Arc mode: 2 metabars, so each metabar is half the output
    # Ramp mode: 1 metabar, so metabar equals full output
    if ramp:
        metabar_beats = total_output_beats
    else:
        metabar_beats = total_output_beats / 2

    # Calculate ratio - normalize to >= 1 so multiply = faster, divide = slower
    ratio_value = ratio_num / ratio_den
    if ratio_value < 1:
        ratio_value = 1 / ratio_value

    # Create MIDI file
    midi = MIDIFile(1)
    track = 0
    channel = 0
    midi.addTempo(track, 0, bpm)
    midi.addTimeSignature(track, 0, time_sig_num, int(math.log2(time_sig_den)), 24, 8)

    # Generate layer times using independent layer approach for both directions
    # Layer 1: forward from t=0 (guaranteed loud note at start)
    # Layer 2: backward from metabar_beats (guaranteed loud note at end)
    # This ensures consistent, predictable behavior regardless of ratio or measure count

    if direction == "accel":
        # Accel: Layer 1 speeds up (base → fast), Layer 2 speeds up (slow → base)
        layer1_start_tempo = bpm
        layer1_end_tempo = bpm * ratio_value
        layer2_start_tempo = bpm / ratio_value
        layer2_end_tempo = bpm
    else:
        # Decel: Layer 1 slows down (base → slow), Layer 2 slows down (fast → base)
        layer1_start_tempo = bpm
        layer1_end_tempo = bpm / ratio_value
        layer2_start_tempo = bpm * ratio_value
        layer2_end_tempo = bpm

    layer1_times = generate_layer_times_forward(metabar_beats, bpm, layer1_start_tempo, layer1_end_tempo)
    layer2_times = generate_layer_times_backward(metabar_beats, bpm, layer2_start_tempo, layer2_end_tempo)

    # Determine display tempos for output
    if direction == "accel":
        layer1_start, layer1_end = bpm, bpm * ratio_value
        layer2_start, layer2_end = bpm / ratio_value, bpm
    else:
        layer1_start, layer1_end = bpm, bpm / ratio_value
        layer2_start, layer2_end = bpm * ratio_value, bpm

    # Both directions: Layer 1 fades out (127→1), Layer 2 fades in (1→127)
    # This creates the crossfade illusion regardless of tempo direction

    # Minimum gap to leave at end for seamless looping (at base tempo)
    min_end_gap = 0.2  # Leave at least 0.2 beats before loop point

    # Helper to add a layer's notes
    def add_layer_notes(times, pitch, fade_out, time_offset=0):
        """Add notes for a layer. fade_out=True means 127→1, False means 1→~120.

        Velocity is calculated by note INDEX (not time position) to ensure:
        - First note of fade_out = 127, last note = 1
        - First note of fade_in = 1, last note = slightly less than 127

        The fade_in layer doesn't reach 127 because the 127 belongs to the
        first note of the fade_out layer at the seam. Two 1s at the opposite
        seam is acceptable (imperceptible).

        Notes are filtered by duration FIRST, then velocities calculated on
        the remaining notes.
        """
        # First pass: calculate durations and filter out invalid notes
        valid_notes = []
        for i, t in enumerate(times):
            if i < len(times) - 1:
                next_time = times[i + 1]
                duration = min((next_time - t) * 0.8, metabar_beats - t - min_end_gap)
            else:
                duration = min(1.0, metabar_beats - t - min_end_gap)

            if duration > 0.01:
                valid_notes.append((t, duration))

        # Second pass: calculate velocities and add notes
        n_notes = len(valid_notes)
        for i, (t, duration) in enumerate(valid_notes):
            if fade_out:
                # Fade out: 127 → 1 (first note = 127, last note = 1)
                if n_notes > 1:
                    progress = i / (n_notes - 1)  # 0.0 to 1.0
                else:
                    progress = 0.0  # Single note gets 127
                velocity = round(127 - 126 * progress)  # 127 → 1
            else:
                # Fade in: 1 → (not quite 127)
                # The 127 belongs to the first note of the fade_out layer at the seam.
                # Two 1s in a row at the opposite seam is fine (imperceptible).
                if n_notes > 1:
                    progress = i / n_notes  # 0.0 to (n_notes-1)/n_notes, never reaches 1.0
                else:
                    progress = 0.0  # Single note gets 1
                velocity = round(1 + 126 * progress)    # 1 → ~118-125

            # Clamp to valid MIDI range
            velocity = max(1, min(127, velocity))

            midi.addNote(track, channel, pitch, t + time_offset, duration, velocity)

    # Meta-bar 1: Layer 1 on low pitch (fades out), Layer 2 on high pitch (fades in)
    add_layer_notes(layer1_times, note_pitch_low, fade_out=True, time_offset=0)
    add_layer_notes(layer2_times, note_pitch_high, fade_out=False, time_offset=0)

    # Meta-bar 2 (arc mode only): pitches swapped to reveal continuous lines
    if not ramp:
        add_layer_notes(layer1_times, note_pitch_high, fade_out=True, time_offset=metabar_beats)
        add_layer_notes(layer2_times, note_pitch_low, fade_out=False, time_offset=metabar_beats)

    # Write file
    with open(output_file, "wb") as f:
        midi.writeFile(f)

    duration_seconds = (total_output_beats / bpm) * 60.0
    mode_str = "ramp" if ramp else "arc"

    print(f"Generated: {output_file}")
    print(f"  Mode: {mode_str}")
    print(f"  Time signature: {time_sig_num}/{time_sig_den}")
    print(f"  Base tempo: {bpm} BPM")
    print(f"  Duration: {num_measures} measures ({total_output_beats} beats, {duration_seconds:.2f} sec)")
    print(f"  Ratio: {ratio_num}/{ratio_den} ({ratio_value:.3f})")
    print(f"  Direction: {direction}")
    print(f"  Layer 1: {layer1_start:.1f} → {layer1_end:.1f} BPM (fades out)")
    print(f"  Layer 2: {layer2_start:.1f} → {layer2_end:.1f} BPM (fades in)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Risset rhythm MIDI"
    )
    
    parser.add_argument("--time-sig", type=str, default="4/4",
                        help="Time signature (default: 4/4)")
    parser.add_argument("--bpm", type=float, default=120.0,
                        help="Base tempo (default: 120)")
    parser.add_argument("--measures", type=int, default=4,
                        help="Number of measures (default: 4)")
    parser.add_argument("--ratio", type=str, default="2/1",
                        help="Speed ratio (default: 2/1)")
    parser.add_argument("--direction", type=str, required=True,
                        choices=["accel", "decel"],
                        help="Direction: accel or decel (REQUIRED)")
    parser.add_argument("--pitch-low", type=int, default=60,
                        help="MIDI note for slower layer (default: 60)")
    parser.add_argument("--pitch-high", type=int, default=64,
                        help="MIDI note for faster layer (default: 64)")
    parser.add_argument("-o", "--output", type=str, default=None,
                        help="Output file (default: auto-generated from parameters)")
    parser.add_argument("--ramp", action="store_true",
                        help="Ramp mode: output 1 metabar (default is arc: 2 metabars)")

    args = parser.parse_args()

    # Parse time signature
    time_parts = args.time_sig.split("/")
    if len(time_parts) != 2:
        print("Error: time signature must be num/den (e.g., 4/4)")
        exit(1)

    time_sig_num = int(time_parts[0])
    time_sig_den = int(time_parts[1])

    # Parse ratio
    ratio_parts = args.ratio.split("/")
    if len(ratio_parts) != 2:
        print("Error: ratio must be num/den (e.g., 2/1)")
        exit(1)

    ratio_num = int(ratio_parts[0])
    ratio_den = int(ratio_parts[1])

    # Validate ratio direction and auto-flip if contradictory
    # For accel: ratio should be < 1 (num < den) - "speeding up from num to den"
    # For decel: ratio should be > 1 (num > den) - "slowing down from num to den"
    ratio_value = ratio_num / ratio_den

    if args.direction == "accel" and ratio_value > 1:
        print(f"Warning: {ratio_num}/{ratio_den} with 'accel' is contradictory.")
        print(f"  '{ratio_num}/{ratio_den}' suggests {ratio_num} slowing to {ratio_den}, not accelerating.")
        print(f"  Auto-flipping to {ratio_den}/{ratio_num} for acceleration ({ratio_den} → {ratio_num}).")
        ratio_num, ratio_den = ratio_den, ratio_num
    elif args.direction == "decel" and ratio_value < 1:
        print(f"Warning: {ratio_num}/{ratio_den} with 'decel' is contradictory.")
        print(f"  '{ratio_num}/{ratio_den}' suggests {ratio_num} speeding to {ratio_den}, not decelerating.")
        print(f"  Auto-flipping to {ratio_den}/{ratio_num} for deceleration ({ratio_den} → {ratio_num}).")
        ratio_num, ratio_den = ratio_den, ratio_num

    # Generate default filename with metadata if not specified
    if args.output is None:
        bpm_str = f"{int(args.bpm)}bpm" if args.bpm == int(args.bpm) else f"{args.bpm}bpm"
        mode_str = "_ramp" if args.ramp else ""
        output_file = f"risset_{bpm_str}_{ratio_num}-{ratio_den}_{args.direction}_{args.measures}m{mode_str}.mid"
    else:
        output_file = args.output

    generate_risset_rhythm(
        time_sig_num=time_sig_num,
        time_sig_den=time_sig_den,
        bpm=args.bpm,
        num_measures=args.measures,
        ratio_num=ratio_num,
        ratio_den=ratio_den,
        direction=args.direction,
        note_pitch_low=args.pitch_low,
        note_pitch_high=args.pitch_high,
        output_file=output_file,
        ramp=args.ramp
    )