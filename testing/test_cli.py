#!/usr/bin/env python3
"""
Tests for the risset.py command line.

Run with: pytest testing
"""

import os
import subprocess
import sys

import pytest

RISSET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "risset.py")


def run_cli(tmp_path, *args):
    """Run risset.py with the working directory set to tmp_path."""
    return subprocess.run(
        [sys.executable, RISSET] + list(args),
        capture_output=True, text=True, cwd=str(tmp_path)
    )


# Convention: accel is written smaller number first (num < den),
# decel larger number first (num > den).
@pytest.mark.parametrize("ratio,direction,expected", [
    ("1/2", "accel", "risset_120bpm_1-2_accel_8m.mid"),
    ("2/3", "accel", "risset_120bpm_2-3_accel_8m.mid"),
    ("2/1", "decel", "risset_120bpm_2-1_decel_8m.mid"),
    ("5/3", "decel", "risset_120bpm_5-3_decel_8m.mid"),
])
def test_ratio_in_conventional_order_gives_no_warning(tmp_path, ratio, direction, expected):
    result = run_cli(tmp_path, "--ratio", ratio, "--direction", direction, "--measures", "8")
    assert result.returncode == 0, result.stderr
    assert "Warning" not in result.stdout
    assert os.listdir(str(tmp_path)) == [expected]


@pytest.mark.parametrize("ratio,direction,expected", [
    ("2/1", "accel", "risset_120bpm_1-2_accel_8m.mid"),
    ("3:2", "accel", "risset_120bpm_2-3_accel_8m.mid"),
    ("1/2", "decel", "risset_120bpm_2-1_decel_8m.mid"),
    ("3/5", "decel", "risset_120bpm_5-3_decel_8m.mid"),
])
def test_reversed_ratio_is_flipped_with_a_warning(tmp_path, ratio, direction, expected):
    result = run_cli(tmp_path, "--ratio", ratio, "--direction", direction, "--measures", "8")
    assert result.returncode == 0, result.stderr
    assert "contradictory" in result.stdout
    assert "Auto-flipping" in result.stdout
    assert os.listdir(str(tmp_path)) == [expected]


@pytest.mark.parametrize("args,direction,expected", [
    ([], "accel", "risset_120bpm_1-2_accel_4m.mid"),
    ([], "decel", "risset_120bpm_2-1_decel_4m.mid"),
    (["--ratio", "3"], "accel", "risset_120bpm_1-3_accel_4m.mid"),
    (["--ratio", "3"], "decel", "risset_120bpm_3-1_decel_4m.mid"),
])
def test_default_and_single_number_ratio_follow_the_direction(tmp_path, args, direction, expected):
    result = run_cli(tmp_path, "--direction", direction, *args)
    assert result.returncode == 0, result.stderr
    assert "Warning" not in result.stdout
    assert os.listdir(str(tmp_path)) == [expected]


def test_flipped_ratio_gives_the_same_rhythm(tmp_path):
    for name, ratio in (("a.mid", "2/1"), ("b.mid", "1/2")):
        result = run_cli(tmp_path, "--ratio", ratio, "--direction", "accel", "-o", name)
        assert result.returncode == 0, result.stderr
    with open(str(tmp_path / "a.mid"), "rb") as a, open(str(tmp_path / "b.mid"), "rb") as b:
        assert a.read() == b.read()


@pytest.mark.parametrize("args", [
    ["--ratio", "1.5/1"],
    ["--ratio", "2/0"],
    ["--ratio", "0/1"],
    ["--ratio=-2/1"],
    ["--ratio", "2/2"],
    ["--ratio", "2/1/3"],
    ["--ratio", "abc"],
    ["--bpm", "0"],
    ["--bpm", "-120"],
    ["--bpm", "nan"],
    ["--time-sig", "4/0"],
    ["--time-sig", "0/4"],
    ["--time-sig", "4/3"],
    ["--time-sig", "4"],
    ["--pitch-low", "60", "--pitch-high", "60"],
    ["--pitch-high", "128"],
    ["--pitch-low", "-1"],
    ["--measures", "0"],
    ["--measures", "-2"],
    ["--velocity-curve", "nan"],
])
def test_bad_input_exits_with_one_line_error(tmp_path, args):
    result = run_cli(tmp_path, "--direction", "accel", *args)
    assert result.returncode == 1
    assert "Traceback" not in result.stderr
    lines = result.stdout.strip().splitlines()
    assert len(lines) == 1 and lines[0].startswith("Error: "), result.stdout
    assert os.listdir(str(tmp_path)) == []


@pytest.mark.parametrize("ratio,expected", [
    ("2", "risset_120bpm_2-1_decel_4m.mid"),
    ("3:2", "risset_120bpm_3-2_decel_4m.mid"),
])
def test_ratio_forms_shared_with_audio_risset(tmp_path, ratio, expected):
    result = run_cli(tmp_path, "--ratio", ratio, "--direction", "decel")
    assert result.returncode == 0, result.stderr
    assert os.listdir(str(tmp_path)) == [expected]


def test_non_default_time_signature_still_works(tmp_path):
    result = run_cli(tmp_path, "--direction", "decel", "--time-sig", "6/8", "-o", "out.mid")
    assert result.returncode == 0, result.stderr
    assert os.path.getsize(str(tmp_path / "out.mid")) > 100
