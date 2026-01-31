/**
 * Risset Rhythm Generator for Max for Live MIDI Tool
 *
 * Generates polyrhythmic Risset rhythm patterns with velocity crossfades.
 * Port of risset.py for use in Ableton Live 12 MIDI Tools.
 */

// Max for Live globals
inlets = 1;
outlets = 1;

// Create dict once at load time
var outputDict = new Dict("risset_output");

// Default parameters
var ratioNum = 3;             // Ratio numerator
var ratioDen = 2;             // Ratio denominator
var direction = "accel";      // "accel" or "decel"
var mode = "arc";             // "arc" or "ramp"
var clipDuration = 16;        // Duration in beats (will be set from clip)
var pitchLow = 60;            // C3
var pitchHigh = 64;           // E3
var baseBpm = 120;


/**
 * Generate note times for Layer 1 (fades out), starting at t=0.
 */
function generateLayerTimesForward(totalBeats, baseBpm, startTempo, endTempo) {
    var timeStep = 0.01;
    var currentTime = 0.0;
    var phase = 0.0;
    var times = [0.0];

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

    var nNotes = validNotes.length;
    for (var i = 0; i < nNotes; i++) {
        var noteData = validNotes[i];
        var velocity;

        if (fadeOut) {
            var progress = (nNotes > 1) ? i / (nNotes - 1) : 0.0;
            velocity = Math.round(127 - 126 * progress);
        } else {
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
    var totalOutputBeats = clipDuration;

    var metabarBeats;
    if (mode === "ramp") {
        metabarBeats = totalOutputBeats;
    } else {
        metabarBeats = totalOutputBeats / 2;
    }

    var ratioValue = ratioNum / ratioDen;

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

    var layer1Times = generateLayerTimesForward(metabarBeats, baseBpm, layer1StartTempo, layer1EndTempo);
    var layer2Times = generateLayerTimesBackward(metabarBeats, baseBpm, layer2StartTempo, layer2EndTempo);

    var allNotes = [];

    var layer1Notes = createLayerNotes(layer1Times, pitchLow, true, metabarBeats, 0);
    var layer2Notes = createLayerNotes(layer2Times, pitchHigh, false, metabarBeats, 0);
    allNotes = allNotes.concat(layer1Notes, layer2Notes);

    if (mode !== "ramp") {
        var layer1NotesM2 = createLayerNotes(layer1Times, pitchHigh, true, metabarBeats, metabarBeats);
        var layer2NotesM2 = createLayerNotes(layer2Times, pitchLow, false, metabarBeats, metabarBeats);
        allNotes = allNotes.concat(layer1NotesM2, layer2NotesM2);
    }

    // Clear and rebuild dictionary using setparse for nested data
    outputDict.clear();
    outputDict.setparse("notes", JSON.stringify(allNotes));

    outlet(0, "dictionary", outputDict.name);
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

function setClipDuration(beats) {
    clipDuration = Math.max(1, beats);
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

function bang() {
    generate();
}

/**
 * Handle dictionary input from live.miditool.in
 * Extracts clip duration before generating
 */
function dictionary(dictName) {
    var d = new Dict(dictName);

    // Try duration_beats first (custom), then calculate from clip_start/clip_end
    var duration = d.get("duration_beats");
    if (duration && duration > 0) {
        clipDuration = duration;
    } else {
        var clipStart = d.get("clip_start");
        var clipEnd = d.get("clip_end");
        if (clipStart !== undefined && clipEnd !== undefined && clipEnd > clipStart) {
            clipDuration = clipEnd - clipStart;
        }
    }

    generate();
}
