# risset

**MIDI generator for Shepard-like rhythmic illusions**

Creates seamless accelerando/ritardando loops using velocity crossfades between two layers.

## Quick Start

```bash
pip install midiutil
python risset.py --ratio 2/1 --direction accel --measures 8
```

## What It Does

Two layers play the same rhythm at different tempos, crossfading via velocity:

```
                    ARC MODE (default) - 8 measures
    ┌─────────────── meta-bar 1 ───────────────┬─────────────── meta-bar 2 ───────────────┐
    │                                          │                                          │
    │  Layer 1 (C3): 120→240 BPM               │  Layer 1 (E3): 120→240 BPM               │
    │  ████████████████████░░░░░░░░░░░░░░░░░░  │  ████████████████████░░░░░░░░░░░░░░░░░░  │
    │  vel 127━━━━━━━━━━━━━━━━━━━━━━━━━━━━▸1   │  vel 127━━━━━━━━━━━━━━━━━━━━━━━━━━━━▸1   │
    │                                          │                                          │
    │  Layer 2 (E3): 60→120 BPM                │  Layer 2 (C3): 60→120 BPM                │
    │  ░░░░░░░░░░░░░░░░░░████████████████████  │  ░░░░░░░░░░░░░░░░░░████████████████████  │
    │  vel 1━━━━━━━━━━━━━━━━━━━━━━━━━━━━▸120   │  vel 1━━━━━━━━━━━━━━━━━━━━━━━━━━━━▸120   │
    │                                          │                                          │
    └──────────────────────────────────────────┴──────────────────────────────────────────┘
                                               ▲
                                            seam (pitches swap)

    Each pitch completes a full arc: loud → quiet → loud (or quiet → loud → quiet)
```

```
                    RAMP MODE (--ramp) - 4 measures
    ┌─────────────────────── meta-bar 1 ───────────────────────┐
    │                                                          │
    │  Layer 1 (C3): 120→240 BPM                               │
    │  ████████████████████░░░░░░░░░░░░░░░░░░                   │
    │  vel 127━━━━━━━━━━━━━━━━━━━━━━━━━━━━▸1                    │
    │                                                          │
    │  Layer 2 (E3): 60→120 BPM                                │
    │  ░░░░░░░░░░░░░░░░░░████████████████████                   │
    │  vel 1━━━━━━━━━━━━━━━━━━━━━━━━━━━━▸120                    │
    │                                                          │
    └──────────────────────────────────────────────────────────┘

    One pitch fading out, one fading in. A building block for composition.
```

## Arc vs Ramp

| Mode | Output | Use Case |
|------|--------|----------|
| **Arc** (default) | 2 meta-bars | Complete musical statement. Each pitch has a full fade journey. |
| **Ramp** (`--ramp`) | 1 meta-bar | Building block. Stack, layer, use for transitions. |

`--measures` always equals your output length.

## Usage

```bash
# Arc mode: 8 measures (two 4-measure meta-bars)
python risset.py --ratio 2/1 --direction accel --measures 8

# Ramp mode: 4 measures (one 4-measure meta-bar)
python risset.py --ratio 2/1 --direction accel --measures 4 --ramp

# Deceleration
python risset.py --ratio 2/1 --direction decel --measures 8

# Different ratio (3:2 polyrhythm)
python risset.py --ratio 3/2 --direction accel --measures 8
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--ratio` | 2/1 | Speed ratio between layers |
| `--direction` | (required) | `accel` or `decel` |
| `--measures` | 4 | Output length in measures |
| `--bpm` | 120 | Base tempo |
| `--ramp` | off | Use ramp mode (1 meta-bar) |
| `--pitch-low` | 60 | MIDI note for layer 1 |
| `--pitch-high` | 64 | MIDI note for layer 2 |
| `-o` | auto | Output filename |

## Examples

See the `examples/` folder for ready-to-use MIDI files.

## License

MIT
