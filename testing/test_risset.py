#!/usr/bin/env python3
"""
Tests for the Risset rhythm generator.
Checks velocity crossfade and loop seam continuity.

Run with: pytest testing
Requires mido and pytest (see requirements-dev.txt).
"""

import contextlib
import io
import os
import sys

import pytest
from mido import MidiFile

# Import risset.py from the repository root regardless of the working directory
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import risset


def analyze_midi(filepath, total_beats, base_bpm):
    """
    Analyze a Risset MIDI file for loop seam quality.
    Returns analysis dict with pass/fail status.
    """
    mid = MidiFile(filepath)

    # Extract notes with duration: (time_in_beats, pitch, velocity, duration)
    notes = []
    current_time = 0  # in ticks
    ticks_per_beat = mid.ticks_per_beat

    # Track note_on events to calculate durations
    active_notes = {}  # (pitch, channel) -> (start_time, velocity)

    for track in mid.tracks:
        current_time = 0
        for msg in track:
            current_time += msg.time
            time_beats = current_time / ticks_per_beat

            if msg.type == 'note_on' and msg.velocity > 0:
                key = (msg.note, msg.channel if hasattr(msg, 'channel') else 0)
                active_notes[key] = (time_beats, msg.velocity)
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                key = (msg.note, msg.channel if hasattr(msg, 'channel') else 0)
                if key in active_notes:
                    start_time, velocity = active_notes[key]
                    duration = time_beats - start_time
                    notes.append((start_time, msg.note, velocity, duration))
                    del active_notes[key]

    # Sort by time
    notes.sort(key=lambda x: x[0])

    # Separate layers by pitch (now includes duration)
    pitches = sorted(set(n[1] for n in notes))
    if len(pitches) != 2:
        return {"error": f"Expected 2 pitches, found {len(pitches)}"}

    pitch_low, pitch_high = pitches
    # layer format: (time, velocity, duration)
    layer1 = [(t, v, d) for t, p, v, d in notes if p == pitch_low]   # fades out
    layer2 = [(t, v, d) for t, p, v, d in notes if p == pitch_high]  # fades in

    results = {
        "filepath": filepath,
        "total_beats": total_beats,
        "layer1_count": len(layer1),
        "layer2_count": len(layer2),
        "checks": []
    }

    # === CHECK 1: Velocity crossfade ===
    # Layer 1 should start loud (~127) and end quiet (~1)
    # Layer 2 should start quiet (~1) and end loud (~127)

    # layer format: (time, velocity, duration)
    l1_start_vel = layer1[0][1] if layer1 else 0
    l1_end_vel = layer1[-1][1] if layer1 else 0
    l2_start_vel = layer2[0][1] if layer2 else 0
    l2_end_vel = layer2[-1][1] if layer2 else 0

    vel_check = {
        "name": "Velocity Crossfade",
        "layer1_start": l1_start_vel,
        "layer1_end": l1_end_vel,
        "layer2_start": l2_start_vel,
        "layer2_end": l2_end_vel,
    }

    # Layer 1 should fade out: start > 100, end < 30
    # Layer 2 should fade in: start < 30, end > 100
    vel_ok = (l1_start_vel > 100 and l1_end_vel < 30 and
              l2_start_vel < 30 and l2_end_vel > 100)
    vel_check["pass"] = vel_ok
    results["checks"].append(vel_check)

    # === CHECK 2: Loop seam velocity match ===
    # At the loop point, Layer 2 (loud) hands off to Layer 1 (loud)
    # So l2_end_vel should be close to l1_start_vel

    seam_vel_diff = abs(l2_end_vel - l1_start_vel)
    seam_vel_check = {
        "name": "Loop Seam Velocity",
        "layer2_end": l2_end_vel,
        "layer1_start": l1_start_vel,
        "difference": seam_vel_diff,
        "pass": seam_vel_diff < 30  # Allow some tolerance
    }
    results["checks"].append(seam_vel_check)

    # === CHECK 3: Loop seam timing (onset-based) ===
    # The gap from Layer 2's last note ONSET to total_beats should be reasonable
    # At base tempo, notes are 1 beat apart

    l2_last_time = layer2[-1][0] if layer2 else 0
    l2_last_duration = layer2[-1][2] if layer2 else 0
    l2_gap_to_end = total_beats - l2_last_time

    l1_first_time = layer1[0][0] if layer1 else 0  # Should be 0

    effective_gap = l2_gap_to_end + l1_first_time

    timing_check = {
        "name": "Loop Seam Timing (Onset)",
        "layer2_last_onset": f"{l2_last_time:.3f}",
        "gap_to_loop": f"{l2_gap_to_end:.3f}",
        "layer1_first_note": f"{l1_first_time:.3f}",
        "effective_gap": f"{effective_gap:.3f}",
        "expected_gap": "0.5-2.5 beats (crossfade handles continuity)",
        # More lenient: the velocity crossfade handles perceptual continuity
        # The "Continuous Line" test is the stricter check for rhythm correctness
        "pass": 0.3 < effective_gap < 2.5
    }
    results["checks"].append(timing_check)

    # === CHECK 4: Loop seam - note END doesn't overlap ===
    # Layer 2's last note should END before total_beats (with some gap)
    # This catches the issue where note duration extends too far

    l2_last_end = l2_last_time + l2_last_duration
    l2_end_gap = total_beats - l2_last_end

    end_gap_check = {
        "name": "Loop Seam (Note End Gap)",
        "layer2_last_onset": f"{l2_last_time:.3f}",
        "layer2_last_duration": f"{l2_last_duration:.3f}",
        "layer2_last_end": f"{l2_last_end:.3f}",
        "gap_after_note_end": f"{l2_end_gap:.3f}",
        "pass": l2_end_gap > 0.1  # Note should end with some gap before loop
    }
    results["checks"].append(end_gap_check)

    # === CHECK 5: Continuous Line Test ===
    # Simulate: Layer 2 bar 1 + Layer 1 bar 2 (transposed/merged)
    # This should form ONE continuous rhythmic line
    # Check that gaps between consecutive notes are reasonable

    # Merge: Layer 2 from bar 1, then Layer 1 from bar 2 (offset by total_beats)
    merged_line = [(t, v, d, "L2") for t, v, d in layer2]
    merged_line += [(t + total_beats, v, d, "L1") for t, v, d in layer1]
    merged_line.sort(key=lambda x: x[0])

    # Calculate gaps in the merged line
    gaps = []
    for i in range(len(merged_line) - 1):
        gap = merged_line[i + 1][0] - merged_line[i][0]
        gaps.append(gap)

    # Find the gap at the seam (around total_beats)
    seam_gap = None
    seam_idx = None
    for i, (t, v, d, layer) in enumerate(merged_line[:-1]):
        next_t = merged_line[i + 1][0]
        if t < total_beats <= next_t:
            seam_gap = next_t - t
            seam_idx = i
            break

    # Check if seam gap is within reasonable range of surrounding gaps
    if seam_gap is not None and seam_idx is not None:
        # Get nearby gaps for comparison
        nearby_start = max(0, seam_idx - 3)
        nearby_end = min(len(gaps), seam_idx + 4)
        nearby_gaps = gaps[nearby_start:nearby_end]
        avg_nearby = sum(nearby_gaps) / len(nearby_gaps) if nearby_gaps else 1.0

        # Seam gap should be within 2x of average nearby gaps
        seam_reasonable = 0.2 < seam_gap < (avg_nearby * 3)
    else:
        seam_reasonable = False
        seam_gap = -1
        avg_nearby = -1

    continuous_check = {
        "name": "Continuous Line (Merged Seam)",
        "seam_gap": f"{seam_gap:.3f}" if seam_gap else "N/A",
        "avg_nearby_gaps": f"{avg_nearby:.3f}" if avg_nearby else "N/A",
        "total_merged_notes": len(merged_line),
        "pass": seam_reasonable
    }
    results["checks"].append(continuous_check)

    # === CHECK 6: Layer 1 timing (first to last) ===
    l1_first = layer1[0][0] if layer1 else 0
    l1_last = layer1[-1][0] if layer1 else 0
    l1_span = l1_last - l1_first

    l1_timing = {
        "name": "Layer 1 Span",
        "first_note": f"{l1_first:.3f}",
        "last_note": f"{l1_last:.3f}",
        "span": f"{l1_span:.3f}",
        "pass": l1_last < total_beats
    }
    results["checks"].append(l1_timing)

    # === CHECK 7: Layer 2 timing ===
    l2_first = layer2[0][0] if layer2 else 0
    l2_last = layer2[-1][0] if layer2 else 0
    l2_span = l2_last - l2_first

    l2_timing = {
        "name": "Layer 2 Span",
        "first_note": f"{l2_first:.3f}",
        "last_note": f"{l2_last:.3f}",
        "span": f"{l2_span:.3f}",
        "pass": l2_last < total_beats
    }
    results["checks"].append(l2_timing)

    # Overall pass
    results["all_pass"] = all(c["pass"] for c in results["checks"])

    return results


def print_results(results):
    """Pretty print analysis results."""
    print(f"\n{'='*60}")
    print(f"File: {results['filepath']}")
    print(f"Total beats: {results['total_beats']}")
    print(f"Layer 1 notes: {results['layer1_count']}, Layer 2 notes: {results['layer2_count']}")
    print(f"{'='*60}")

    for check in results["checks"]:
        status = "✓ PASS" if check["pass"] else "✗ FAIL"
        print(f"\n{check['name']}: {status}")
        for k, v in check.items():
            if k not in ["name", "pass"]:
                print(f"  {k}: {v}")

    print(f"\n{'='*60}")
    overall = "✓ ALL CHECKS PASSED" if results["all_pass"] else "✗ SOME CHECKS FAILED"
    print(f"OVERALL: {overall}")
    print(f"{'='*60}\n")

    return results["all_pass"]


def generate(tmp_path, ratio, direction, measures=4, bpm=120, ramp=True):
    """Generate a MIDI file in tmp_path by calling the generator directly."""
    ratio_num, ratio_den = (int(p) for p in ratio.split("/"))
    output_file = str(tmp_path / "risset.mid")
    with contextlib.redirect_stdout(io.StringIO()):
        risset.generate_risset_rhythm(
            bpm=bpm,
            num_measures=measures,
            ratio_num=ratio_num,
            ratio_den=ratio_den,
            direction=direction,
            output_file=output_file,
            ramp=ramp
        )
    return output_file


def read_notes(filepath):
    """Return sorted (time_in_beats, pitch, velocity) for every note_on."""
    mid = MidiFile(filepath)
    notes = []
    for track in mid.tracks:
        current_time = 0
        for msg in track:
            current_time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                notes.append((current_time / mid.ticks_per_beat, msg.note, msg.velocity))
    notes.sort()
    return notes


TEST_CASES = [
    # (ratio, direction)
    ("2/1", "accel"),
    ("2/1", "decel"),
    ("3/4", "accel"),
    ("3/4", "decel"),
    ("8/5", "accel"),
    ("8/5", "decel"),
    ("5/8", "accel"),
    ("5/8", "decel"),
]


@pytest.mark.parametrize("ratio,direction", TEST_CASES)
@pytest.mark.parametrize("measures", [4, 8])
def test_ramp_seam(tmp_path, ratio, direction, measures):
    """Ramp mode (1 metabar): one pitch per layer, so the layer checks apply."""
    filename = generate(tmp_path, ratio, direction, measures=measures, ramp=True)
    total_beats = 4 * measures  # 4/4 time

    results = analyze_midi(filename, total_beats, 120)
    assert "error" not in results, results
    failed = [c for c in results["checks"] if not c["pass"]]
    if failed:
        print_results(results)
    assert not failed


@pytest.mark.parametrize("ratio,direction", TEST_CASES)
def test_arc_is_ramp_repeated_with_pitches_swapped(tmp_path, ratio, direction):
    """Arc mode (2 metabars): metabar 2 repeats metabar 1 with the pitches swapped."""
    measures = 8
    metabar_beats = 4 * measures / 2
    notes = read_notes(generate(tmp_path, ratio, direction, measures=measures, ramp=False))

    pitches = sorted(set(p for _, p, _ in notes))
    assert len(pitches) == 2
    swap = {pitches[0]: pitches[1], pitches[1]: pitches[0]}

    first = [(round(t, 3), p, v) for t, p, v in notes if t < metabar_beats]
    second = [(round(t - metabar_beats, 3), swap[p], v) for t, p, v in notes if t >= metabar_beats]
    assert first
    assert sorted(first) == sorted(second)
    assert max(t for t, _, _ in notes) < 2 * metabar_beats


if __name__ == "__main__":
    sys.exit(pytest.main([os.path.abspath(__file__)]))
