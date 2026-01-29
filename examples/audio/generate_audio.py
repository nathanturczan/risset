#!/usr/bin/env python3
"""
Generate audio files from Risset rhythm MIDI files using FluidSynth.
Outputs MP3 files (smaller than WAV) with a velocity-sensitive soundfont.

Audio files are trimmed to exact MIDI duration for seamless looping.
"""

import os
import subprocess
import tempfile
from mido import MidiFile

# Soundfont path - TimGM6mb is velocity-sensitive and widely available
SOUNDFONT = "/usr/local/lib/python3.9/site-packages/pretty_midi/TimGM6mb.sf2"

# Use vibraphone (program 11) for short decay and clear velocity response
# Other options: 0=piano, 12=marimba, 13=xylophone
MIDI_PROGRAM = 11  # Vibraphone


def get_midi_duration(midi_path):
    """
    Get the exact duration of a MIDI file in seconds.
    """
    mid = MidiFile(midi_path)
    return mid.length


def render_midi_to_audio(midi_path, output_path, soundfont=SOUNDFONT):
    """
    Render a MIDI file to MP3 using FluidSynth.
    Trims output to exact MIDI duration for seamless looping.
    """
    # Get exact duration for trimming
    duration = get_midi_duration(midi_path)

    # Create temp WAV file
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        wav_path = tmp.name

    try:
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
            midi_path
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
        # Clean up temp WAV
        if os.path.exists(wav_path):
            os.remove(wav_path)


def main():
    """Generate audio for all MIDI files in examples/midi/."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    midi_dir = os.path.join(script_dir, '..', 'midi')
    output_dir = script_dir  # Output to audio folder

    # Verify soundfont exists
    if not os.path.exists(SOUNDFONT):
        print(f"Error: Soundfont not found at {SOUNDFONT}")
        print("Please install pretty_midi or specify a different soundfont.")
        return

    # Find all MIDI files
    midi_files = [f for f in os.listdir(midi_dir) if f.endswith('.mid')]

    if not midi_files:
        print(f"No MIDI files found in {midi_dir}")
        return

    print(f"Found {len(midi_files)} MIDI files")
    print(f"Using soundfont: {SOUNDFONT}")
    print()

    for midi_file in sorted(midi_files):
        midi_path = os.path.join(midi_dir, midi_file)
        output_name = os.path.splitext(midi_file)[0] + '.mp3'
        output_path = os.path.join(output_dir, output_name)

        render_midi_to_audio(midi_path, output_path)

    print(f"\nGenerated audio files in {output_dir}")


if __name__ == '__main__':
    main()
