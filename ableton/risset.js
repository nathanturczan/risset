/**
 * Risset Rhythm Generator for Max for Live MIDI Tool
 *
 * Generates polyrhythmic Risset rhythm patterns with velocity crossfades.
 * Port of risset.py for use in Ableton Live 12 MIDI Tools.
 */

// Max for Live globals
inlets = 1;
outlets = 1;

// Default parameters
var ratioNum = 2;
var ratioDen = 1;
var direction = "accel";  // "accel" or "decel"
var mode = "arc";         // "arc" or "ramp"
var measures = 4;
var pitchLow = 60;        // C3
var pitchHigh = 64;       // E3
var baseBpm = 120;

/**
 * Generate note times for Layer 1 (fades out), starting at t=0.
 */
function generateLayerTimesForward(totalBeats, baseBpm, startTempo, endTempo) {
    var timeStep = 0.01;
    var currentTime = 0.0;
    var phase = 0.0;
    var times = [0.0];  // Always start with a note at t=0

    while (currentTime < totalBeats) {
        var progress = currentTime / totalBeats;
        var currentTempo = startTempo + (endTempo - startTempo) * progress;
        var phaseIncrement = (currentTempo / baseBpm) * timeStep;

        var oldPhase = phase;
        phase += phaseIncrement;

        if (Math.floor(phase) > Math.floor(oldPhase)) {
            if (currentTime > 0.001) {
                times.push(currentTime);
            }
            phase = phase - Math.floor(phase);
        }

        currentTime += timeStep;
    }

    return times;
}

/**
 * Generate note times for Layer 2 (fades in), ending near totalBeats.
 */
function generateLayerTimesBackward(totalBeats, baseBpm, startTempo, endTempo) {
    var timeStep = 0.01;
    var currentTime = totalBeats;
    var phase = 0.0;
    var minEndGap = 0.05;
    var times = [totalBeats - minEndGap];

    while (currentTime > 0) {
        var progress = currentTime / totalBeats;
        var currentTempo = startTempo + (endTempo - startTempo) * progress;
        var phaseIncrement = (currentTempo / baseBpm) * timeStep;

        var oldPhase = phase;
        phase += phaseIncrement;

        if (Math.floor(phase) > Math.floor(oldPhase)) {
            if (currentTime < totalBeats - 0.1) {
                times.push(currentTime);
            }
            phase = phase - Math.floor(phase);
        }

        currentTime -= timeStep;
    }

    times.reverse();
    return times;
}

/**
 * Create notes for a layer with velocity crossfade.
 */
function createLayerNotes(times, pitch, fadeOut, metabarBeats, timeOffset) {
    var minEndGap = 0.2;
    var notes = [];

    // First pass: calculate durations and filter
    var validNotes = [];
    for (var i = 0; i < times.length; i++) {
        var t = times[i];
        var duration;

        if (i < times.length - 1) {
            var nextTime = times[i + 1];
            duration = Math.min((nextTime - t) * 0.8, metabarBeats - t - minEndGap);
        } else {
            duration = Math.min(1.0, metabarBeats - t - minEndGap);
        }

        if (duration > 0.01) {
            validNotes.push({time: t, duration: duration});
        }
    }

    // Second pass: calculate velocities and create notes
    var nNotes = validNotes.length;
    for (var i = 0; i < nNotes; i++) {
        var noteData = validNotes[i];
        var velocity;

        if (fadeOut) {
            // Fade out: 127 → 1
            var progress = (nNotes > 1) ? i / (nNotes - 1) : 0.0;
            velocity = Math.round(127 - 126 * progress);
        } else {
            // Fade in: 1 → ~120
            var progress = (nNotes > 1) ? i / nNotes : 0.0;
            velocity = Math.round(1 + 126 * progress);
        }

        velocity = Math.max(1, Math.min(127, velocity));

        notes.push({
            pitch: pitch,
            start_time: noteData.time + timeOffset,
            duration: noteData.duration,
            velocity: velocity
        });
    }

    return notes;
}

/**
 * Main generation function - called when bang received.
 */
function generate() {
    // Calculate beats
    var beatsPerMeasure = 4;  // Assuming 4/4
    var totalOutputBeats = beatsPerMeasure * measures;

    // Arc mode: 2 metabars, Ramp mode: 1 metabar
    var metabarBeats;
    if (mode === "ramp") {
        metabarBeats = totalOutputBeats;
    } else {
        metabarBeats = totalOutputBeats / 2;
    }

    // Calculate ratio - normalize to >= 1
    var ratioValue = ratioNum / ratioDen;
    if (ratioValue < 1) {
        ratioValue = 1 / ratioValue;
    }

    // Calculate tempos for each layer
    var layer1StartTempo, layer1EndTempo, layer2StartTempo, layer2EndTempo;

    if (direction === "accel") {
        layer1StartTempo = baseBpm;
        layer1EndTempo = baseBpm * ratioValue;
        layer2StartTempo = baseBpm / ratioValue;
        layer2EndTempo = baseBpm;
    } else {
        layer1StartTempo = baseBpm;
        layer1EndTempo = baseBpm / ratioValue;
        layer2StartTempo = baseBpm * ratioValue;
        layer2EndTempo = baseBpm;
    }

    // Generate layer times
    var layer1Times = generateLayerTimesForward(metabarBeats, baseBpm, layer1StartTempo, layer1EndTempo);
    var layer2Times = generateLayerTimesBackward(metabarBeats, baseBpm, layer2StartTempo, layer2EndTempo);

    // Create all notes
    var allNotes = [];

    // Metabar 1: Layer 1 on low pitch (fades out), Layer 2 on high pitch (fades in)
    var layer1Notes = createLayerNotes(layer1Times, pitchLow, true, metabarBeats, 0);
    var layer2Notes = createLayerNotes(layer2Times, pitchHigh, false, metabarBeats, 0);
    allNotes = allNotes.concat(layer1Notes, layer2Notes);

    // Metabar 2 (arc mode only): pitches swapped
    if (mode !== "ramp") {
        var layer1NotesM2 = createLayerNotes(layer1Times, pitchHigh, true, metabarBeats, metabarBeats);
        var layer2NotesM2 = createLayerNotes(layer2Times, pitchLow, false, metabarBeats, metabarBeats);
        allNotes = allNotes.concat(layer1NotesM2, layer2NotesM2);
    }

    // Output as dictionary for live.miditool.out
    var result = {
        notes: allNotes
    };

    outlet(0, "dictionary", JSON.stringify(result));
}

// Message handlers for parameters
function setRatio(num, den) {
    ratioNum = Math.max(1, Math.min(9, num));
    ratioDen = Math.max(1, Math.min(9, den));
}

function setDirection(dir) {
    if (dir === "accel" || dir === "decel" || dir === 0 || dir === 1) {
        direction = (dir === 0 || dir === "accel") ? "accel" : "decel";
    }
}

function setMode(m) {
    if (m === "arc" || m === "ramp" || m === 0 || m === 1) {
        mode = (m === 0 || m === "arc") ? "arc" : "ramp";
    }
}

function setMeasures(m) {
    measures = Math.max(1, Math.min(16, m));
}

function setPitchLow(p) {
    pitchLow = Math.max(0, Math.min(127, p));
}

function setPitchHigh(p) {
    pitchHigh = Math.max(0, Math.min(127, p));
}

function setBpm(b) {
    baseBpm = Math.max(20, Math.min(300, b));
}

// Bang triggers generation
function bang() {
    generate();
}

// List input for setting all parameters at once
// Format: ratioNum ratioDen direction mode measures pitchLow pitchHigh
function list() {
    var args = arrayfromargs(arguments);
    if (args.length >= 7) {
        ratioNum = args[0];
        ratioDen = args[1];
        direction = args[2] === 0 ? "accel" : "decel";
        mode = args[3] === 0 ? "arc" : "ramp";
        measures = args[4];
        pitchLow = args[5];
        pitchHigh = args[6];
    }
    generate();
}
