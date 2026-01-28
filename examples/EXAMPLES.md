# Example MIDI Files

This folder contains 20 ready-to-use Risset rhythm MIDI files covering common polyrhythmic ratios.

All files are generated at 120 BPM, 4/4 time, 4 measures. Each file contains 2 meta-bars with pitches swapped in bar 2, revealing the continuous tempo lines for both verification and better playback.

## File List

### 2:1 Ratio (Doubling)
- **risset_120bpm_2-1_accel_4m.mid** — Accelerating 120→240 BPM, classic tempo doubling
- **risset_120bpm_2-1_decel_4m.mid** — Decelerating 120→60 BPM, classic tempo halving

### 3:1 Ratio (Tripling)
- **risset_120bpm_3-1_accel_4m.mid** — Accelerating 120→360 BPM, extreme speed-up
- **risset_120bpm_3-1_decel_4m.mid** — Decelerating 120→40 BPM, extreme slow-down

### 3:2 Ratio (Triplet Feel)
- **risset_120bpm_3-2_accel_4m.mid** — Accelerating 120→180 BPM, triplet transformation
- **risset_120bpm_3-2_decel_4m.mid** — Decelerating 120→80 BPM, reverse triplet feel

### 4:3 Ratio (Perfect Fourth)
- **risset_120bpm_4-3_accel_4m.mid** — Accelerating 120→160 BPM, subtle speed-up
- **risset_120bpm_4-3_decel_4m.mid** — Decelerating 120→90 BPM, subtle slow-down

### 5:3 Ratio
- **risset_120bpm_5-3_accel_4m.mid** — Accelerating 120→200 BPM, 5-against-3 polyrhythm
- **risset_120bpm_5-3_decel_4m.mid** — Decelerating 120→72 BPM, 5-against-3 polyrhythm

### 5:4 Ratio (Major Third)
- **risset_120bpm_5-4_accel_4m.mid** — Accelerating 120→150 BPM, gentle speed-up
- **risset_120bpm_5-4_decel_4m.mid** — Decelerating 120→96 BPM, gentle slow-down

### 6:5 Ratio
- **risset_120bpm_6-5_accel_4m.mid** — Accelerating 120→144 BPM, very subtle speed-up
- **risset_120bpm_6-5_decel_4m.mid** — Decelerating 120→100 BPM, very subtle slow-down

### 7:4 Ratio
- **risset_120bpm_7-4_accel_4m.mid** — Accelerating 120→210 BPM, septuplet feel
- **risset_120bpm_7-4_decel_4m.mid** — Decelerating 120→68.6 BPM, septuplet feel

### 7:5 Ratio
- **risset_120bpm_7-5_accel_4m.mid** — Accelerating 120→168 BPM, complex polyrhythm
- **risset_120bpm_7-5_decel_4m.mid** — Decelerating 120→85.7 BPM, complex polyrhythm

### 8:5 Ratio (Golden Ratio Approximation)
- **risset_120bpm_8-5_accel_4m.mid** — Accelerating 120→192 BPM, golden ratio feel
- **risset_120bpm_8-5_decel_4m.mid** — Decelerating 120→75 BPM, golden ratio feel

## Usage

Import any file into your DAW. Each file contains two meta-bars:
- **Meta-bar 1**: The loopable pattern
- **Meta-bar 2**: Same pattern with pitches swapped, revealing the continuous tempo line

For a seamless perpetual Risset illusion, loop just meta-bar 1.

## Generating Custom Files

```bash
# Basic usage
python risset.py --ratio 2/1 --direction accel --bpm 120 --measures 4

# Different tempo and length
python risset.py --ratio 3/2 --direction decel --bpm 100 --measures 8

# Custom pitches (e.g., for drums)
python risset.py --ratio 4/3 --direction accel --pitch-low 36 --pitch-high 38
```

See the main README for full documentation.
