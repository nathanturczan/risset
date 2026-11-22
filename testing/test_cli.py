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


@pytest.mark.parametrize("ratio,direction,expected", [
    ("2/1", "accel", "risset_120bpm_2-1_accel_8m.mid"),
    ("1/2", "accel", "risset_120bpm_1-2_accel_8m.mid"),
    ("3/5", "decel", "risset_120bpm_3-5_decel_8m.mid"),
    ("5/3", "decel", "risset_120bpm_5-3_decel_8m.mid"),
])
def test_ratio_ordering_is_accepted_without_warning(tmp_path, ratio, direction, expected):
    result = run_cli(tmp_path, "--ratio", ratio, "--direction", direction, "--measures", "8")
    assert result.returncode == 0, result.stderr
    assert "Warning" not in result.stdout
    assert "contradictory" not in result.stdout
    assert os.listdir(str(tmp_path)) == [expected]


def test_ratio_ordering_does_not_change_the_rhythm(tmp_path):
    for name, ratio in (("a.mid", "2/1"), ("b.mid", "1/2")):
        result = run_cli(tmp_path, "--ratio", ratio, "--direction", "accel", "-o", name)
        assert result.returncode == 0, result.stderr
    with open(str(tmp_path / "a.mid"), "rb") as a, open(str(tmp_path / "b.mid"), "rb") as b:
        assert a.read() == b.read()
