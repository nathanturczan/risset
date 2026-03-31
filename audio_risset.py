#!/usr/bin/env python3
"""
Audio Risset rhythm generator.

Creates perpetual acceleration/deceleration illusion with audio loops
by applying variable-rate time-stretching and amplitude crossfades.

Two modes:
- Simple: Two copies at fixed stretch ratios, crossfaded (stepped but fast)
- Variable: Continuously varying playback rate (smooth but requires pyrubberband)

Usage:
    python audio_risset.py input.wav output.wav --ratio 2 --direction accel
    python audio_risset.py input.wav output.wav --ratio 3/2 --direction decel --mode variable
"""

import argparse
import numpy as np
import soundfile as sf
import warnings
from pathlib import Path

# Try to import optional dependencies
try:
    import librosa
    HAS_LIBROSA = True
except ImportError:
    HAS_LIBROSA = False

try:
    import pyrubberband as pyrb
    HAS_PYRUBBERBAND = True
except ImportError:
    HAS_PYRUBBERBAND = False


def parse_ratio(ratio_str):
    """Parse ratio string like '2/1' or '3:2' into float >= 1."""
    if '/' in ratio_str:
        parts = ratio_str.split('/')
    elif ':' in ratio_str:
        parts = ratio_str.split(':')
    else:
        return float(ratio_str)

    num, den = float(parts[0]), float(parts[1])
    ratio = num / den
    return ratio if ratio >= 1 else 1 / ratio


def apply_amplitude_envelope(audio, fade_out=True, gamma=1.5):
    """
    Apply amplitude envelope to audio.

    fade_out=True: 1.0 → 0.0 (loud at start, quiet at end)
    fade_out=False: 0.0 → 1.0 (quiet at start, loud at end)

    gamma controls curve shape (matches MIDI velocity_gamma):
    - 0.5 = "Punch" (hard, compensatory)
    - 1.0 = Linear
    - 1.5 = Default (balanced)
    - 3.0 = "Gentle" (soft, conservative)
    """
    n_samples = len(audio)
    t = np.linspace(0, 1, n_samples)

    if fade_out:
        linear = 1.0 - t  # 1.0 → 0.0
    else:
        linear = t  # 0.0 → 1.0

    # Apply gamma curve
    envelope = np.power(linear, gamma)

    # Handle stereo
    if audio.ndim == 2:
        envelope = envelope[:, np.newaxis]

    return audio * envelope


def time_stretch_simple(audio, sr, rate):
    """
    Simple time-stretch using librosa.
    rate > 1 = faster (shorter), rate < 1 = slower (longer)
    """
    if not HAS_LIBROSA:
        raise ImportError("librosa required for time-stretching. Install with: pip install librosa")

    # librosa works with mono or multi-channel
    if audio.ndim == 1:
        return librosa.effects.time_stretch(audio, rate=rate)
    else:
        # Process each channel
        channels = []
        for ch in range(audio.shape[1]):
            stretched = librosa.effects.time_stretch(audio[:, ch], rate=rate)
            channels.append(stretched)
        return np.column_stack(channels)


def time_stretch_variable(audio, sr, start_rate, end_rate):
    """
    Variable-rate time-stretch using pyrubberband time-map.

    The rate changes continuously from start_rate to end_rate.

    start_rate, end_rate: playback rates (>1 = faster, <1 = slower)
    """
    if not HAS_PYRUBBERBAND:
        raise ImportError("pyrubberband required for variable-rate stretching. Install with: pip install pyrubberband")

    n_samples = len(audio)
    duration = n_samples / sr

    # Build time map: list of (source_time, target_time) tuples
    # For linearly changing rate from r0 to r1:
    # rate(t) = r0 + (r1 - r0) * (t / T)
    # target_time = integral of 1/rate(t) dt

    n_points = 100  # Number of time-map points
    source_times = np.linspace(0, duration, n_points)
    target_times = []

    for src_t in source_times:
        # Numerical integration of 1/rate from 0 to src_t
        # Using trapezoidal rule
        n_int = max(2, int(src_t * sr / 100))  # Integration steps
        int_t = np.linspace(0, src_t, n_int) if n_int > 1 else np.array([0, src_t])
        progress = int_t / duration if duration > 0 else np.zeros_like(int_t)
        rates = start_rate + (end_rate - start_rate) * progress
        inv_rates = 1.0 / rates
        target_t = np.trapezoid(inv_rates, int_t) if len(int_t) > 1 else 0
        target_times.append(target_t)

    time_map = list(zip(source_times, target_times))

    # pyrubberband expects (n_samples, n_channels) for stereo
    if audio.ndim == 1:
        audio = audio[:, np.newaxis]

    # Use rubberband's time-map stretching
    stretched = pyrb.timemap_stretch(audio, sr, time_map)

    # Squeeze back to 1D if mono
    if stretched.shape[1] == 1:
        stretched = stretched[:, 0]

    return stretched


def generate_audio_risset_simple(
    audio,
    sr,
    ratio=2.0,
    direction="accel",
    gamma=1.5,
    n_layers=2
):
    """
    Generate Risset audio using simple fixed-rate stretching.

    Creates two layers:
    - Layer 1: Original rate, fading out
    - Layer 2: Stretched by ratio, fading in

    The output is designed to loop seamlessly.
    """
    n_samples = len(audio)

    if direction == "accel":
        # Layer 1: base tempo → faster (but we use original audio)
        # Layer 2: slower tempo → base (stretched = longer = slower)
        layer1_audio = audio.copy()
        layer2_audio = time_stretch_simple(audio, sr, rate=1.0/ratio)  # Slower
    else:
        # Decel: Layer 1 base→slower, Layer 2 faster→base
        layer1_audio = audio.copy()
        layer2_audio = time_stretch_simple(audio, sr, rate=ratio)  # Faster

    # Match lengths: trim or pad layer2 to match layer1
    target_len = n_samples
    if len(layer2_audio) > target_len:
        layer2_audio = layer2_audio[:target_len]
    elif len(layer2_audio) < target_len:
        # Pad with zeros (or loop if you prefer)
        if audio.ndim == 2:
            padding = np.zeros((target_len - len(layer2_audio), audio.shape[1]))
        else:
            padding = np.zeros(target_len - len(layer2_audio))
        layer2_audio = np.concatenate([layer2_audio, padding])

    # Apply amplitude envelopes
    layer1 = apply_amplitude_envelope(layer1_audio, fade_out=True, gamma=gamma)
    layer2 = apply_amplitude_envelope(layer2_audio, fade_out=False, gamma=gamma)

    # Mix layers
    output = layer1 + layer2

    # Normalize to prevent clipping
    max_val = np.max(np.abs(output))
    if max_val > 0:
        output = output / max_val * 0.95

    return output


def generate_audio_risset_variable(
    audio,
    sr,
    ratio=2.0,
    direction="accel",
    gamma=1.5
):
    """
    Generate Risset audio using variable-rate time-stretching.

    Creates two layers with continuously varying playback rates,
    matching the MIDI implementation more closely.
    """
    n_samples = len(audio)

    if direction == "accel":
        # Layer 1: rate goes 1.0 → ratio (speeding up)
        # Layer 2: rate goes 1/ratio → 1.0 (also speeding up, from slower)
        layer1_start, layer1_end = 1.0, ratio
        layer2_start, layer2_end = 1.0/ratio, 1.0
    else:
        # Decel: rates going the other way
        layer1_start, layer1_end = 1.0, 1.0/ratio
        layer2_start, layer2_end = ratio, 1.0

    # Generate layers with variable rate
    layer1_audio = time_stretch_variable(audio, sr, layer1_start, layer1_end)
    layer2_audio = time_stretch_variable(audio, sr, layer2_start, layer2_end)

    # Match lengths
    target_len = max(len(layer1_audio), len(layer2_audio))

    def pad_or_trim(arr, target):
        if len(arr) > target:
            return arr[:target]
        elif len(arr) < target:
            if arr.ndim == 2:
                padding = np.zeros((target - len(arr), arr.shape[1]))
            else:
                padding = np.zeros(target - len(arr))
            return np.concatenate([arr, padding])
        return arr

    layer1_audio = pad_or_trim(layer1_audio, target_len)
    layer2_audio = pad_or_trim(layer2_audio, target_len)

    # Apply amplitude envelopes
    layer1 = apply_amplitude_envelope(layer1_audio, fade_out=True, gamma=gamma)
    layer2 = apply_amplitude_envelope(layer2_audio, fade_out=False, gamma=gamma)

    # Mix
    output = layer1 + layer2

    # Normalize
    max_val = np.max(np.abs(output))
    if max_val > 0:
        output = output / max_val * 0.95

    return output


def generate_audio_risset_shepard(
    audio,
    sr,
    ratio=2.0,
    direction="accel",
    gamma=1.5,
    n_layers=8
):
    """
    Generate Risset audio using Shepard-style multiple layers.

    Creates N layers at logarithmically spaced rates with bell-curve
    amplitude envelopes. More computationally expensive but smoother.
    """
    n_samples = len(audio)

    # Create layers at different rates
    # Rates span from 1/ratio to ratio (in log space)
    log_rates = np.linspace(-np.log(ratio), np.log(ratio), n_layers)
    rates = np.exp(log_rates)

    layers = []
    for i, rate in enumerate(rates):
        # Time-stretch this layer
        stretched = time_stretch_simple(audio, sr, rate=rate)

        # Calculate position in the "spectrum" (0 to 1)
        position = i / (n_layers - 1) if n_layers > 1 else 0.5

        # Bell curve amplitude based on position
        # Center of the bell moves based on direction
        if direction == "accel":
            # Bell moves from low rates to high rates
            center = np.linspace(0, 1, n_samples)
        else:
            # Bell moves from high rates to low rates
            center = np.linspace(1, 0, n_samples)

        # Gaussian envelope
        sigma = 0.3
        envelope = np.exp(-0.5 * ((position - center) / sigma) ** 2)

        # Apply gamma
        envelope = np.power(envelope, gamma)

        # Trim/pad to match length
        if len(stretched) > n_samples:
            stretched = stretched[:n_samples]
        elif len(stretched) < n_samples:
            if audio.ndim == 2:
                padding = np.zeros((n_samples - len(stretched), audio.shape[1]))
            else:
                padding = np.zeros(n_samples - len(stretched))
            stretched = np.concatenate([stretched, padding])

        # Apply envelope
        if stretched.ndim == 2:
            envelope = envelope[:, np.newaxis]

        layers.append(stretched * envelope)

    # Sum all layers
    output = sum(layers)

    # Normalize
    max_val = np.max(np.abs(output))
    if max_val > 0:
        output = output / max_val * 0.95

    return output


def main():
    parser = argparse.ArgumentParser(
        description="Generate audio with Risset perpetual acceleration/deceleration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Simple two-layer version (fast, stepped)
    python audio_risset.py drum_loop.wav output.wav --ratio 2 --direction accel

    # Variable-rate version (smooth, requires pyrubberband)
    python audio_risset.py drum_loop.wav output.wav --ratio 3/2 --direction decel --mode variable

    # Shepard-style with 8 layers (smoothest)
    python audio_risset.py melodic.wav output.wav --ratio 2 --direction accel --mode shepard --layers 8

    # Adjust crossfade curve
    python audio_risset.py input.wav output.wav --ratio 2 --direction accel --gamma 1.0
"""
    )

    parser.add_argument("input", type=str, help="Input audio file")
    parser.add_argument("output", type=str, help="Output audio file")

    parser.add_argument("--ratio", type=str, default="2",
                        help="Speed ratio (e.g., '2', '2/1', '3:2'). Default: 2")
    parser.add_argument("--direction", type=str, required=True,
                        choices=["accel", "decel"],
                        help="Direction: accel or decel (REQUIRED)")
    parser.add_argument("--mode", type=str, default="simple",
                        choices=["simple", "variable", "shepard"],
                        help="Processing mode (default: simple)")
    parser.add_argument("--gamma", type=float, default=1.5,
                        help="Amplitude curve gamma (0.5=punch, 1.0=linear, 1.5=default, 3.0=gentle)")
    parser.add_argument("--layers", type=int, default=8,
                        help="Number of layers for shepard mode (default: 8)")

    args = parser.parse_args()

    # Check dependencies
    if not HAS_LIBROSA:
        print("Error: librosa required. Install with: pip install librosa")
        return 1

    if args.mode == "variable" and not HAS_PYRUBBERBAND:
        print("Error: pyrubberband required for variable mode.")
        print("Install with: pip install pyrubberband")
        print("Also requires rubberband library: brew install rubberband")
        return 1

    # Load audio
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}")
        return 1

    print(f"Loading: {args.input}")
    audio, sr = sf.read(args.input)

    # Parse ratio
    ratio = parse_ratio(args.ratio)
    print(f"Ratio: {ratio:.3f}")
    print(f"Direction: {args.direction}")
    print(f"Mode: {args.mode}")
    print(f"Gamma: {args.gamma}")

    # Generate
    if args.mode == "simple":
        output = generate_audio_risset_simple(
            audio, sr, ratio=ratio, direction=args.direction, gamma=args.gamma
        )
    elif args.mode == "variable":
        output = generate_audio_risset_variable(
            audio, sr, ratio=ratio, direction=args.direction, gamma=args.gamma
        )
    elif args.mode == "shepard":
        output = generate_audio_risset_shepard(
            audio, sr, ratio=ratio, direction=args.direction,
            gamma=args.gamma, n_layers=args.layers
        )

    # Write output
    sf.write(args.output, output, sr)

    duration = len(output) / sr
    print(f"Generated: {args.output}")
    print(f"Duration: {duration:.3f}s")
    print(f"Sample rate: {sr} Hz")

    return 0


if __name__ == "__main__":
    exit(main())
