# risset

**MIDI generator for Shepard-like rhythmic illusions**

Creates seamless accelerando and ritardando loops using the Risset rhythm technique — a rhythmic equivalent of the Shepard tone pitch illusion.

## What is a Risset Rhythm?

A Risset rhythm creates the perception of continuous acceleration (or deceleration) that loops seamlessly back to the starting tempo. Like Shepard tones create an endless rising pitch, Risset rhythms create an endless tempo change.

### How it works

The illusion uses **two rhythmic layers** that crossfade:

1. **Layer 1** starts at the base tempo and accelerates (or decelerates) according to the ratio, fading out as it goes
2. **Layer 2** starts at a different tempo and converges back to the base tempo, fading in as it goes

When Layer 1 finishes fading out, Layer 2 has arrived at the starting tempo — ready to become the new Layer 1 if you loop it.

### The Math

**Phase Accumulation:**
Each layer generates notes using phase accumulation, like an audio oscillator:
- Phase increments based on current tempo: `phase += (current_tempo / base_tempo) * time_step`
- When phase crosses 1.0, a note is placed and phase resets
- This ensures perfect synchronization between layers regardless of tempo ratio

**Linear Tempo Interpolation:**
Tempo changes linearly over the duration:
```
current_tempo = start_tempo + (end_tempo - start_tempo) * progress
```

This maintains the exact rhythmic ratio between layers throughout the transition.

**Velocity Crossfade:**
- Layer 1: velocity 127 → 1 (fades out)
- Layer 2: velocity 1 → 127 (fades in)

Range is 1-127 (never 0) so both layers remain audible throughout.

## Installation

```bash
pip install midiutil --break-system-packages
```

## Usage

### Basic Examples

```bash
# 2:1 accelerando over 4 measures at 120 BPM
python risset.py --ratio 2/1 --direction accel --measures 4 --bpm 120

# 2:1 ritardando over 8 measures
python risset.py --ratio 2/1 --direction decel --measures 8 --bpm 120

# 3:2 polyrhythmic acceleration
python risset.py --ratio 3/2 --direction accel --measures 4 --bpm 100
```

### All Parameters

```bash
python risset.py \
  --time-sig 4/4 \           # Time signature (default: 4/4)
  --bpm 120 \                # Base tempo (default: 120)
  --measures 4 \             # Number of measures (default: 4)
  --ratio 2/1 \              # Speed ratio (default: 2/1)
  --direction accel \        # accel or decel (REQUIRED)
  --pitch-low 60 \           # MIDI note for slower layer (default: 60)
  --pitch-high 64 \          # MIDI note for faster layer (default: 64)
  -o output.mid              # Output filename (default: risset.mid)
```

## Understanding the Ratio

The ratio describes the relationship between the two layers:

**2/1 ratio (doubling):**
- Layer 1: 120 → 240 BPM (accel) or 120 → 60 BPM (decel)
- Layer 2: 60 → 120 BPM (accel) or 240 → 120 BPM (decel)

**3/2 ratio (sesquialtera):**
- Layer 1: 100 → 150 BPM (accel) or 100 → 66.67 BPM (decel)
- Layer 2: 66.67 → 100 BPM (accel) or 150 → 100 BPM (decel)

Any ratio works: 3/1, 4/3, 5/3, 7/4, etc.

## Musical Applications

- **Transitions:** Seamless tempo changes between song sections
- **Builds:** Perpetual acceleration/deceleration loops
- **Rhythmic Interest:** Polyrhythmic textures that shift continuously
- **Live Performance:** Trigger layers in Ableton or other DAWs
- **Composition:** Add to larger systems with metric modulation, hemiolas, etc.

## Implementation Notes

This generator uses **linear tempo interpolation** (not logarithmic) to maintain exact rhythmic ratios between layers. This ensures that in a 2:1 ratio, one layer always plays exactly twice as fast as the other at every point in the transition.

The phase accumulation method guarantees sample-accurate synchronization — the layers will always align at their common subdivisions (e.g., every other beat in a 2:1 ratio).

## Credits

Inspired by Jean-Claude Risset's rhythmic techniques and the SuperCollider community's implementations of Shepard-like rhythmic illusions.

## License

MIT
