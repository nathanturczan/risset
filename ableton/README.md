# Risset Rhythm Generator - Max for Live MIDI Tool

A MIDI Tool Generator for Ableton Live 12 that creates polyrhythmic Risset rhythm patterns directly in MIDI clips.

## Requirements

- Ableton Live 12.0 or later
- Max for Live

## Installation

1. Copy `risset.js` to your Max for Live search path, or keep it alongside the .amxd file
2. Load `Risset Generator.amxd` into Ableton (or create it using the instructions below)
3. The tool will appear in the MIDI Tools panel under Generators

## Creating the Max Patch

Since .amxd files are binary, you'll need to create the patch in Max. Here's how:

### Step 1: Create New MIDI Tool Generator

1. In Ableton Live 12, create a new MIDI track
2. Create an empty MIDI clip and double-click to open it
3. In the clip view, click the **Tools Tab** (waveform icon)
4. From the Generator dropdown, select **"MIDI Generator Template"**
5. Click the **Edit** button (bottom left) to open in Max

### Step 2: Build the Patch

Delete the template contents and create this structure:

```
[live.miditool.in]
        |
        | (bang on left outlet)
        v
[trigger b b b b b b b b]
        |
        | (from right to left, set all parameters then trigger)
        v
[js risset.js]
        |
        | (outputs dictionary)
        v
[dict.unpack notes:]
        |
        v
[dict.pack notes:]
        |
        v
[live.miditool.out]
```

### Step 3: Add UI Controls (Presentation Mode)

Add these `live.*` objects and connect them to trigger the js object:

| Object | Parameter | Range | Links to |
|--------|-----------|-------|----------|
| `live.dial` | Ratio Num | 1-9 | `[prepend setRatio] → [js]` (combine with Den) |
| `live.dial` | Ratio Den | 1-9 | (same as above) |
| `live.menu` | Direction | Accel, Decel | `[prepend setDirection] → [js]` |
| `live.menu` | Mode | Arc, Ramp | `[prepend setMode] → [js]` |
| `live.dial` | Measures | 1-16 | `[prepend setMeasures] → [js]` |
| `live.dial` | Pitch Low | 0-127 | `[prepend setPitchLow] → [js]` |
| `live.dial` | Pitch High | 0-127 | `[prepend setPitchHigh] → [js]` |

### Step 4: Wire the Logic

```
[live.miditool.in]
        |
        v
    [t b b]
        |    \
        |     [js risset.js]
        |           |
        v           v
[dict.unpack notes:]
        |
        |  (array of note dicts)
        v
[dict.pack notes:]
        |
        v
[live.miditool.out]
```

The key insight: `live.miditool.in` outputs a bang when the user clicks Apply. This triggers the js object to generate notes, which are then packed and sent to `live.miditool.out`.

### Step 5: Handle Dictionary Output from JS

The JS outputs a JSON string. Parse it with:

```
[js risset.js]
        |
        v
[fromsymbol]
        |
        v
[dict.deserialize]
        |
        v
[live.miditool.out]
```

### Step 6: Save as MIDI Tool

1. File → Save As...
2. Name it "Risset Generator.amxd"
3. Save to your User Library or a location in your Max search path

## Development Workflow

The `.maxpat` file is the human-readable source, but the `.amxd` file is what actually runs in Ableton. These are separate files - **changes to the `.maxpat` do not automatically update the `.amxd`**.

When making changes:

1. Edit the `.maxpat` file (directly or via code)
2. Open the `.amxd` in Max (click Edit on the device in Ableton)
3. Manually copy/paste the changes from `.maxpat` to the `.amxd`, or rewire as needed
4. Save the `.amxd`

Alternatively, you can rebuild the `.amxd` from scratch by opening the `.maxpat` in Max and exporting (File → Export as Max for Live Device), but this may lose device-specific settings.

## Usage

1. Create a MIDI track with any instrument
2. Create an empty MIDI clip (or select an existing one)
3. Double-click the clip to open it
4. Click the **Tools Tab** in clip view
5. Select **"Risset Generator"** from the Generators dropdown
6. Adjust parameters:
   - **Ratio**: Polyrhythmic ratio (e.g., 3:2, 5:4)
   - **Direction**: Accel (speeds up) or Decel (slows down)
   - **Mode**: Arc (2 metabars) or Ramp (1 metabar)
   - **Measures**: Output length
   - **Pitch Low/High**: MIDI notes for the two layers
7. Click **Apply** to generate the pattern

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| Ratio Num/Den | Tempo ratio between layers | 2:1 |
| Direction | Accel (speeding up) or Decel (slowing down) | Accel |
| Mode | Arc (complete cycle) or Ramp (building block) | Arc |
| Measures | Number of measures to generate | 4 |
| Pitch Low | MIDI note for Layer 1 | 60 (C3) |
| Pitch High | MIDI note for Layer 2 | 64 (E3) |

## Ratio Constraints

The ratio numerator/denominator relationship depends on direction:

- **Accelerating**: numerator < denominator (e.g., 2:9)
  - Think of it as speeding up from a smaller number to a larger number
- **Decelerating**: numerator > denominator (e.g., 9:2)
  - Think of it as slowing down from a larger number to a smaller number

The UI enforces these constraints automatically and displays a reminder at the bottom of the panel.

## How It Works

The generator creates two layers:
- **Layer 1** (Pitch Low): Fades out, tempo changes from base
- **Layer 2** (Pitch High): Fades in, tempo approaches base

When looped, the velocity crossfade creates the illusion of perpetual tempo change.

## Tips

- **Arc mode** is best for standalone loops that create the full illusion
- **Ramp mode** is useful for building blocks you can stack or transition with
- Try different pitch combinations - octaves work well, as do thirds
- The effect is most pronounced with percussive sounds (vibraphone, marimba, piano)
