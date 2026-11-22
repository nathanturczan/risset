# MIDI Tool Development Notes

Reference notes for building Max for Live MIDI Tools (Generators and Transformers) for Ableton Live 12+. Compiled from Philip Meyer's Discord discussions (meyer-devices.com).

## Key Concepts

### Generators vs Transformers

| Type | Purpose | Input | Output |
|------|---------|-------|--------|
| Generator | Creates new MIDI patterns | Parameters only | Note dictionary |
| Transformer | Modifies existing MIDI | Note dictionary | Note dictionary |

Risset is a **Generator**.

## Data Flow Architecture

### Basic Generator Flow
```
[parameters] → [generation logic] → dict.pack notes: → live.miditool.out
```

### Basic Transformer Flow
```
live.miditool.in → dict.unpack notes: → [array processing] → dict.pack notes: → live.miditool.out
```

### Note Dictionary Structure
Notes come as an array of dictionaries with these fields:
- `note_id` - unique identifier
- `pitch` - MIDI note number (0-127)
- `start_time` - position in beats
- `duration` - length in beats
- `velocity` - note velocity (0-127)
- `mute` - boolean
- `probability` - 0.0 to 1.0
- `velocity_deviation` - variation amount
- `release_velocity` - release velocity value

### Array Processing
- `dict.unpack notes:` outputs an array
- Use `array.iter` or `array.map` to iterate over notes
- Use `array.push` to combine/add notes
- Use `set` message on array object to replace contents

## Accessing Clip Data via Live API

Generators can access the entire clip (not limited to selection):

### JavaScript Example
```javascript
// Get the currently selected clip
var view = new LiveAPI('live_set view');
var detailClipId = view.get('detail_clip');
var notes = JSON.parse(detailClip.call('get_all_notes_extended')).notes;
```

### Max Patching
```
live.thisdevice
    ↓
live.path live_set view → get detail_clip
    ↓
live.object → call get_all_notes_extended
    ↓
route detail_clip get_all_notes_extended
```

### Writing Notes
- Use `add_new_notes` to add notes to a clip
- Generators can wipe and rewrite the entire clip

## Critical Gotchas

### 1. Bang Requires Output
**When you bang `live.miditool.in`, Live expects a note dictionary back and will throw an error if you don't provide one.**

You cannot just query for context without performing a generation/transformation.

### 2. Random Numbers and Apply Cycle
`Math.random()` in JS and `random` in Max regenerate on every apply cycle with no awareness of state. This causes:
- Transformations to change unexpectedly when reapplied
- No way to preserve random values between cycles

**Workarounds:**
- Save generated random numbers and reuse them
- Control when random numbers are generated
- Use deterministic algorithms (like Risset does)

Philip's devices Phrase Shuffler and Even Seed implement random number persistence.

### 3. Selection Start/End Not Available
Cannot get the selection boundaries via Live API. Generators work around this by operating on the entire clip.

### 4. Sample Rate Mismatch
When working with audio (Simpler slices), use the **audio file's sample rate**, not the Live session sample rate. Slice positions must be scaled to warp marker/sample length.

## MIDI Mapping Workarounds

MIDI Tools cannot be directly MIDI-mapped. Known workarounds:

1. **OSC Injection** - Add `udpreceive` inside the device (ports 9999/10000 commonly used). Requires modifying the device.

2. **Performance Pack by Iftah** - Uses variations system

3. **Button Parameter Mapper 2.0** - Third-party M4L device

4. **Note Cursor Link by MGF Audio** - External linking

## JavaScript vs Max Patching

Philip Meyer recommends JavaScript for complex devices:
> "it can sometimes be a bit easier than max patching for these types of devices, especially as the devices become more complex"

Considerations:
- JS is better for complex logic and data manipulation
- Max patching works well for simpler devices (Noah Pred's approach)
- V8 JS engine available in newer Max versions
- jsui provides UI capabilities within Max

## Current Limitations (as of 2025)

- **No MPE data access** in MIDI Tools (expected to come eventually)
- **No apply cycle information** shared with devices
- **Cannot get context without outputting** - no read-only queries

## Debugging Tips

- Check for scheduler interactions (delay objects, etc.) causing lag
- Verify nothing accumulating in JS (memory leaks)
- Console errors may not always appear
- Test with minimal patches to isolate issues

## References

- [Clip - Live Object Model](https://docs.cycling74.com/apiref/lom/clip/) - Official Cycling '74 documentation
- [meyer-devices.com](https://meyer-devices.com) - Philip Meyer's MIDI Tool devices
- [maxforlive.com](https://maxforlive.com) - Community device library

## About the Author

Nathan Turczan is a composer and creative technologist based in Los Angeles, CA. You can find his website at [nathanturczan.com](https://nathanturczan.com), follow him on Instagram [@nathan_turczan](https://www.instagram.com/nathan_turczan/), or reach him at nathanturczan@gmail.com.
