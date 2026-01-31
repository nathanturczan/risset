# Claude Code Settings

## Commit Guidelines
- Commit without any AI attribution or co-authors
- No "Co-Authored-By" lines for Claude/Anthropic

## README Requirements
Every README must end with an "About the Author" section:

```markdown
## About the Author

Nathan Turczan is a composer and creative technologist based in Los Angeles, CA. You can find his website at [nathanturczan.com](https://nathanturczan.com), follow him on Instagram [@nathan_turczan](https://www.instagram.com/nathan_turczan/), or reach him at nathanturczan@gmail.com.
```

## Ratio Constraints
The ratio numerator/denominator constraints differ by direction:
- **Accelerating**: numerator < denominator (e.g., 2:9) - smaller number on top, speeding up to larger
- **Decelerating**: numerator > denominator (e.g., 9:2) - larger number on top, slowing down to smaller

The UI enforces these constraints and displays a reminder. The JS normalizes the ratio internally to always be > 1, so the direction toggle controls the tempo change direction.

## Terminology
- Use "metabar" (no hyphen) to match academic literature (Stowell 2011)
- Always say "polyrhythmic", NEVER "polymetric" - remind the user if they make this mistake

## References
- Stowell, D. (2011). "Scheduling and Composing with Risset Eternal Accelerando Rhythms." Proceedings of the International Computer Music Conference 2011.

## File Locations
Development and testing happen in two different directories:
- **Development**: `/Users/soney/Github/risset/ableton/` - all code changes happen here
- **Testing**: `/Users/soney/Music/Ableton/User Library/MIDI Tools/Max Generators/` - where Ableton loads from

After making changes, files must be copied from development to testing:
```bash
cp /Users/soney/Github/risset/ableton/* "/Users/soney/Music/Ableton/User Library/MIDI Tools/Max Generators/"
```

The .amxd file bundles its own copies of JS/HTML. To update:
1. Copy .js and .html to User Library
2. Open .amxd in Max
3. Compile JS (double-click js object, Cmd+S)
4. Save .amxd (Cmd+S)

Before pushing to git, copy the tested .amxd back to the repo.

## Design Philosophy
We are emulating Philip Meyer's approach to packaging and form factor for Max MIDI Tool devices:
- **meyer-devices.com** - Reference for device categories (Generators, Transformers)
- Generators create rhythmic/harmonic patterns from parameters
- Transformers modify existing MIDI data
- Compact, focused UI with intuitive controls
- Emphasis on creative exploration and "grid-defying" rhythmic approaches
- Clean jweb-based interfaces that integrate seamlessly with Live 12 MIDI Tools
