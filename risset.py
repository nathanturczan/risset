#!/usr/bin/env python3
"""
Risset rhythm generator.
Two layers with opposing tempo curves and crossfading velocities.
"""

import argparse
from midiutil import MIDIFile
import math


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
    output_file="risset.mid"
):
    """
    Generate a Risset rhythm MIDI file with two layers.
    """
    
    # Calculate total duration in beats
    beats_per_measure = time_sig_num * (4.0 / time_sig_den)
    total_beats = beats_per_measure * num_measures
    
    # Calculate ratio
    ratio_value = ratio_num / ratio_den
    
    # Create MIDI file
    midi = MIDIFile(1)
    track = 0
    channel = 0
    midi.addTempo(track, 0, bpm)
    midi.addTimeSignature(track, 0, time_sig_num, int(math.log2(time_sig_den)), 24, 8)
    
    # Determine start and end tempos for each layer based on direction
    if direction == "accel":
        layer1_start = bpm
        layer1_end = bpm * ratio_value
        layer2_start = bpm / ratio_value
        layer2_end = bpm
    else:  # decel
        layer1_start = bpm
        layer1_end = bpm / ratio_value
        layer2_start = bpm * ratio_value
        layer2_end = bpm
    
    # Generate layers using phase accumulation
    generate_layer_phase(
        midi, track, channel,
        total_beats=total_beats,
        base_bpm=bpm,
        start_bpm=layer1_start,
        end_bpm=layer1_end,
        pitch=note_pitch_low,
        fade_out=True
    )
    
    generate_layer_phase(
        midi, track, channel,
        total_beats=total_beats,
        base_bpm=bpm,
        start_bpm=layer2_start,
        end_bpm=layer2_end,
        pitch=note_pitch_high,
        fade_out=False
    )
    
    # Write file
    with open(output_file, "wb") as f:
        midi.writeFile(f)
    
    duration_seconds = (total_beats / bpm) * 60.0
    
    print(f"Generated: {output_file}")
    print(f"  Time signature: {time_sig_num}/{time_sig_den}")
    print(f"  Base tempo: {bpm} BPM")
    print(f"  Duration: {num_measures} measures ({total_beats} beats, {duration_seconds:.2f} sec)")
    print(f"  Ratio: {ratio_num}/{ratio_den} ({ratio_value:.3f})")
    print(f"  Direction: {direction}")
    print(f"  Layer 1: {layer1_start:.1f} → {layer1_end:.1f} BPM (fades out)")
    print(f"  Layer 2: {layer2_start:.1f} → {layer2_end:.1f} BPM (fades in)")


def generate_layer_phase(midi, track, channel, total_beats, base_bpm, start_bpm, end_bpm, pitch, fade_out):
    """
    Generate layer using phase accumulation.
    Phase accumulates based on the current tempo ratio.
    Velocity range: 1-127 (never 0)
    """
    
    time_step = 0.01  # Small time step in beats
    current_time = 0.0
    phase = 0.0
    
    notes = []
    
    # Place first note at time 0
    velocity = 127 if fade_out else 1
    notes.append((0.0, velocity))
    
    while current_time < total_beats:
        # Progress through transition
        progress = current_time / total_beats
        
        # Linear tempo interpolation
        current_tempo = start_bpm + (end_bpm - start_bpm) * progress
        
        # Phase increment: how much phase we accumulate per beat at base_bpm
        phase_increment = (current_tempo / base_bpm) * time_step
        
        # Check if we crossed a phase boundary
        old_phase = phase
        phase += phase_increment
        
        if int(phase) > int(old_phase):
            # Place a note
            # Velocity range: 1-127 (never 0)
            if fade_out:
                velocity = int(127 - 126 * progress)  # 127 → 1
            else:
                velocity = int(1 + 126 * progress)     # 1 → 127
            
            notes.append((current_time, velocity))
            # Reset phase
            phase = phase - int(phase)
        
        current_time += time_step
    
    # Add notes to MIDI with bounds checking
    for i, (note_time, velocity) in enumerate(notes):
        # Skip notes beyond the boundary
        if note_time >= total_beats:
            continue
        
        # Duration until next note or end
        if i < len(notes) - 1:
            next_time = notes[i+1][0]
            duration = min((next_time - note_time) * 0.8, total_beats - note_time)
        else:
            # Last note: calculate proper duration
            duration = min(1.0, total_beats - note_time)
        
        # Ensure duration is valid (positive and non-zero)
        if duration > 0.01:
            midi.addNote(track, channel, pitch, note_time, duration, velocity)


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
    parser.add_argument("-o", "--output", type=str, default="risset.mid",
                        help="Output file (default: risset.mid)")
    
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
        output_file=args.output
    )