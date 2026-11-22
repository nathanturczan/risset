#!/usr/bin/env python3
"""
Generate audio files from Risset rhythm MIDI files using FluidSynth.
Outputs MP3 files (smaller than WAV) with a velocity-sensitive soundfont.

Audio files are trimmed to exact MIDI duration for seamless looping.

Usage:
    python generate_audio.py [path/to/soundfont.sf2]
"""

import os
import subprocess
import sys
import tempfile
from mido import MidiFile, Message

# Soundfont - TimGM6mb is velocity-sensitive and ships with pretty_midi
SOUNDFONT_NAME = "TimGM6mb.sf2"


def find_soundfont():
    """
    Locate the soundfont: first command line argument if given,
    otherwise the copy bundled with the installed pretty_midi package.
    Returns None if it cannot be found.
    """
    if len(sys.argv) > 1:
        return sys.argv[1] if os.path.exists(sys.argv[1]) else None

    try:
        import pretty_midi
    except ImportError:
        return None

    path = os.path.join(os.path.dirname(pretty_midi.__file__), SOUNDFONT_NAME)
    return path if os.path.exists(path) else None

# Use vibraphone (program 11) for short decay and clear velocity response
# Other options: 0=piano, 12=marimba, 13=xylophone
MIDI_PROGRAM = 11  # Vibraphone


def get_midi_duration(midi_path):
    """
    Get the exact duration of a MIDI file in seconds.
    """
    mid = MidiFile(midi_path)
    return mid.length


def write_midi_with_program(midi_path, output_path, program=MIDI_PROGRAM):
    """
    Write a copy of a MIDI file with a program change at time 0 on every
    channel that plays notes (risset.py itself writes no program change).
    """
    mid = MidiFile(midi_path)
    for track in mid.tracks:
        channels = sorted(set(msg.channel for msg in track if msg.type == 'note_on'))
        for channel in channels:
            track.insert(0, Message('program_change', channel=channel, program=program, time=0))
    mid.save(output_path)


def render_midi_to_audio(midi_path, output_path, soundfont):
    """
    Render a MIDI file to MP3 using FluidSynth.
    Trims output to exact MIDI duration for seamless looping.
    """
    # Get exact duration for trimming
    duration = get_midi_duration(midi_path)

    # Create temp WAV file
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        wav_path = tmp.name

    # Create temp MIDI file with the program change applied
    with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as tmp:
        program_midi_path = tmp.name

    try:
        write_midi_with_program(midi_path, program_midi_path)

        # Render MIDI to WAV with FluidSynth
        # -ni = non-interactive, -F = output file, -r = sample rate
        # Disable reverb/chorus to avoid tail extending beyond note duration
        cmd_synth = [
            'fluidsynth',
            '-ni',                    # Non-interactive
            '-g', '1.0',              # Gain
            '-r', '44100',            # Sample rate
            '-o', 'synth.reverb.active=no',
            '-o', 'synth.chorus.active=no',
            '-F', wav_path,           # Output file
            soundfont,
            program_midi_path
        ]

        subprocess.run(cmd_synth, check=True, capture_output=True)

        # Convert WAV to MP3 using ffmpeg, trimming to exact duration
        # -y = overwrite, -t = duration, -ar = sample rate, -b:a = bitrate
        cmd_mp3 = [
            'ffmpeg',
            '-y',                     # Overwrite
            '-i', wav_path,
            '-t', f'{duration:.6f}',  # Exact duration in seconds
            '-ar', '44100',           # Sample rate
            '-b:a', '128k',           # Bitrate (good balance of size/quality)
            '-q:a', '2',              # Quality
            output_path
        ]

        subprocess.run(cmd_mp3, check=True, capture_output=True)

        print(f"Generated: {output_path} ({duration:.3f}s)")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error rendering {midi_path}: {e}")
        return False

    finally:
        # Clean up temp files
        if os.path.exists(wav_path):
            os.remove(wav_path)
        if os.path.exists(program_midi_path):
            os.remove(program_midi_path)


def main():
    """Generate audio for all MIDI files in examples/midi/."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    midi_dir = os.path.join(script_dir, '..', 'midi')
    output_dir = script_dir  # Output to audio folder

    # Locate soundfont
    soundfont = find_soundfont()
    if soundfont is None:
        print("Error: Soundfont not found.")
        print(f"Please install pretty_midi (bundles {SOUNDFONT_NAME}) or pass a soundfont path:")
        print("  python generate_audio.py path/to/soundfont.sf2")
        return

    # Find all MIDI files
    midi_files = [f for f in os.listdir(midi_dir) if f.endswith('.mid')]

    if not midi_files:
        print(f"No MIDI files found in {midi_dir}")
        return

    print(f"Found {len(midi_files)} MIDI files")
    print(f"Using soundfont: {soundfont}")
    print()

    for midi_file in sorted(midi_files):
        midi_path = os.path.join(midi_dir, midi_file)
        output_name = os.path.splitext(midi_file)[0] + '.mp3'
        output_path = os.path.join(output_dir, output_name)

        render_midi_to_audio(midi_path, output_path, soundfont)

    print(f"\nGenerated audio files in {output_dir}")


if __name__ == '__main__':
    main()
