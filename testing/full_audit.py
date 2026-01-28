#!/usr/bin/env python3
"""
Comprehensive audit of all Risset rhythm combinations.
Tests seam quality for all ratios at multiple measure counts.
"""

import subprocess
import os
import tempfile
from mido import MidiFile


def analyze_seam(filepath, total_beats):
    """
    Analyze a Risset MIDI file for seam quality.
    Returns dict with Layer 1 start offset and seam gap.
    """
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
                    dur = time_beats - start
                    notes.append((start, msg.note, vel, dur))
                    del active_notes[msg.note]

    notes.sort(key=lambda x: x[0])

    # Separate by pitch
    pitches = sorted(set(n[1] for n in notes))
    if len(pitches) < 2:
        return {"error": "Not enough pitches"}

    pitch_low, pitch_high = pitches[0], pitches[-1]

    # In unfold mode, seam is at total_beats
    # High pitch = Layer 2 (bar 1) -> Layer 1 (bar 2)
    layer_high = [(t, v, d) for t, p, v, d in notes if p == pitch_high]
    layer_low = [(t, v, d) for t, p, v, d in notes if p == pitch_low]

    # Find notes around the seam
    high_before = [n for n in layer_high if n[0] < total_beats]
    high_after = [n for n in layer_high if n[0] >= total_beats]

    if not high_before or not high_after:
        return {"error": "Missing notes around seam"}

    last_before = high_before[-1]
    first_after = high_after[0]

    seam_gap = first_after[0] - last_before[0]
    layer1_start_offset = first_after[0] - total_beats

    # Check velocities at seam (should both be high ~120+)
    vel_before = last_before[1]
    vel_after = first_after[1]

    # Check Layer 2 first note (should be near 0)
    layer2_first = layer_high[0][0] if layer_high else None

    return {
        "seam_gap": seam_gap,
        "layer1_start_offset": layer1_start_offset,
        "vel_before_seam": vel_before,
        "vel_after_seam": vel_after,
        "layer2_first_note": layer2_first,
        "last_note_before": last_before[0],
        "first_note_after": first_after[0],
    }


def run_test(ratio_num, ratio_den, direction, measures, bpm=120):
    """Generate a file and analyze it."""
    with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as f:
        output_file = f.name

    # Find risset.py relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    risset_path = os.path.join(script_dir, "..", "risset.py")

    cmd = [
        "python3", risset_path,
        "--ratio", f"{ratio_num}/{ratio_den}",
        "--direction", direction,
        "--measures", str(measures),
        "--bpm", str(bpm),
        "-o", output_file
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        return {"error": result.stderr}

    total_beats = measures * 4  # Assuming 4/4

    analysis = analyze_seam(output_file, total_beats)

    # Clean up
    os.unlink(output_file)

    return analysis


def evaluate_result(analysis):
    """
    Evaluate if a result passes quality checks.
    Returns (pass/fail, reason)
    """
    if "error" in analysis:
        return "ERROR", analysis["error"]

    l1_offset = analysis["layer1_start_offset"]
    seam_gap = analysis["seam_gap"]
    vel_before = analysis["vel_before_seam"]
    vel_after = analysis["vel_after_seam"]

    issues = []

    # Layer 1 should start very close to 0 (within 0.1 beats)
    if abs(l1_offset) > 0.1:
        issues.append(f"L1 offset {l1_offset:.3f}")

    # Seam gap should be reasonable (0.5 to 2.5 beats)
    if seam_gap < 0.3 or seam_gap > 2.5:
        issues.append(f"Gap {seam_gap:.3f}")

    # Both velocities at seam should be high (>100)
    if vel_before < 100:
        issues.append(f"Low vel before ({vel_before})")
    if vel_after < 100:
        issues.append(f"Low vel after ({vel_after})")

    if issues:
        return "FAIL", ", ".join(issues)

    return "PASS", f"Gap={seam_gap:.3f}, L1={l1_offset:.3f}"


def main():
    """Run comprehensive audit."""

    # All ratios to test
    ratios = [
        (2, 1), (3, 1), (3, 2), (4, 3), (5, 3),
        (5, 4), (6, 5), (7, 4), (7, 5), (8, 5)
    ]

    directions = ["accel", "decel"]
    measure_counts = [4, 8]

    print("=" * 80)
    print("RISSET RHYTHM COMPREHENSIVE AUDIT")
    print("=" * 80)
    print()

    results = []

    for measures in measure_counts:
        print(f"\n{'=' * 80}")
        print(f"TESTING {measures} MEASURES (seam at beat {measures * 4})")
        print("=" * 80)

        for direction in directions:
            print(f"\n--- {direction.upper()} ---")
            print(f"{'Ratio':<10} {'Status':<8} {'Details'}")
            print("-" * 60)

            for ratio_num, ratio_den in ratios:
                # For accel, we use inverted ratio input
                if direction == "accel":
                    input_num, input_den = ratio_den, ratio_num
                else:
                    input_num, input_den = ratio_num, ratio_den

                analysis = run_test(input_num, input_den, direction, measures)
                status, details = evaluate_result(analysis)

                ratio_str = f"{ratio_num}:{ratio_den}"
                status_symbol = "✓" if status == "PASS" else "✗" if status == "FAIL" else "?"

                print(f"{ratio_str:<10} {status_symbol} {status:<6} {details}")

                results.append({
                    "measures": measures,
                    "direction": direction,
                    "ratio": ratio_str,
                    "status": status,
                    "details": details,
                    "analysis": analysis
                })

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    errors = sum(1 for r in results if r["status"] == "ERROR")

    print(f"\nTotal tests: {total}")
    print(f"Passed: {passed} ({100*passed/total:.1f}%)")
    print(f"Failed: {failed} ({100*failed/total:.1f}%)")
    print(f"Errors: {errors} ({100*errors/total:.1f}%)")

    if failed > 0:
        print("\n--- FAILED TESTS ---")
        for r in results:
            if r["status"] == "FAIL":
                print(f"  {r['measures']}m {r['direction']} {r['ratio']}: {r['details']}")

    print("\n" + "=" * 80)
    print(f"OVERALL: {'ALL TESTS PASSED' if failed == 0 and errors == 0 else 'SOME TESTS FAILED'}")
    print("=" * 80)

    return failed == 0 and errors == 0


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
