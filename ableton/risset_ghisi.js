/**
 * Risset Rhythm Generator for Max for Live MIDI Tool (Ghisi Closed-Form)
 *
 * Uses a closed-form formula for onset times (derived from Ghisi's framework)
 * instead of phase accumulation. Drop-in alternative to risset.js for A/B comparison.
 *
 * Key difference: exponential tempo curve (rate linear in logical time)
 * vs linear tempo curve (rate linear in physical time) in risset.js.
 *
 * Reference: Ghisi, D. (2023). "Barberpole tempo illusions."
 * Journal of Mathematics and Music, 17:2, 266-281.
 * DOI: 10.1080/17459737.2021.2001699
 */

// Max for Live globals
inlets = 1;
outlets = 1;

post("\n========================================\n");
post("Risset Ghisi JS compiled successfully!\n");
post("========================================\n");

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
var velocityGamma = 1.5;          // Velocity curve: <1 = punch, 1 = linear, >1 = gentle


/**
 * Compute onset times using closed-form formula for exponential rate growth.
 *
 * For rate function r(t) = r0 * D^(t/tau), onset times are:
 * t(n) = tau * ln(1 + n * ln(D) / (r0 * tau)) / ln(D)
 *
 * where D = endRate/startRate, r0 = startRate, tau = metabar duration.
 * For constant rate (D ~ 1): t(n) = n / startRate.
 *
 * This is derived from integrating the rate function and solving for
 * elapsed time given note index n. Related to Ghisi (2023) Equation 6
 * but reparameterized for direct rate specification.
 *
 * Returns array of onset times in [0, tau).
 */
function ghisiOnsetTimes(tau, startRate, endRate) {
    var D = endRate / startRate;
    var times = [];
    var maxNotes = 10000; // Safety cap

    // Special case: constant rate (D ~ 1)
    if (Math.abs(D - 1) < 1e-6) {
        var n = 0;
        while (n < maxNotes) {
            var t = n / startRate;
            if (t >= tau) break;
            times.push(t);
            n++;
        }
        return times;
    }

    var lnD = Math.log(D);
    var coeff = lnD / (startRate * tau);
    var n = 0;

    while (n < maxNotes) {
        var arg = 1 + n * coeff;
        if (arg <= 0) break; // No more valid onsets (decel case)

        var t = tau * Math.log(arg) / lnD;
        if (t >= tau) break;

        times.push(t);
        n++;
    }

    return times;
}


/**
 * Generate note times for Layer 1 (fades out), starting at t=0.
 */
function generateLayerTimesForward(totalBeats, baseBpm, startTempo, endTempo) {
    var startRate = startTempo / baseBpm;
    var endRate = endTempo / baseBpm;
    return ghisiOnsetTimes(totalBeats, startRate, endRate);
}

/**
 * Generate note times for Layer 2 (fades in), ending near totalBeats.
 * Adds an anchor note near tau if the last computed onset leaves a gap.
 *
 * Note: Phase alignment between layers is approximate. For seamless looping,
 * Layer 2's final note should align with where Layer 1's first note would
 * be in the next loop iteration. The anchor note is a practical workaround.
 */
function generateLayerTimesBackward(totalBeats, baseBpm, startTempo, endTempo) {
    var startRate = startTempo / baseBpm;
    var endRate = endTempo / baseBpm;
    var times = ghisiOnsetTimes(totalBeats, startRate, endRate);

    // Ensure a note near tau for seamless looping
    var minEndGap = 0.05;
    var anchorTime = totalBeats - minEndGap;
    var anchorThreshold = 0.5;

    if (times.length === 0 || (anchorTime - times[times.length - 1]) > anchorThreshold) {
        times.push(anchorTime);
    }

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

        // Calculate linear velocity first
        // Both use (nNotes - 1) so crossfades sum to constant amplitude
        var linearVel;
        var progress = (nNotes > 1) ? i / (nNotes - 1) : 0.0;
        if (fadeOut) {
            linearVel = 1.0 - progress;  // 1.0 → 0.0
        } else {
            linearVel = progress;  // 0.0 → 1.0
        }

        // Apply velocity curve (gamma)
        // gamma < 1: hard/compensatory (boosts middle)
        // gamma = 1: linear (no shaping)
        // gamma > 1: soft (reduces middle, conservative)
        var shaped = Math.pow(linearVel, velocityGamma);
        velocity = Math.round(1 + 126 * shaped);

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
    post("=== GENERATE (GHISI) CALLED ===\n");
    post("clipDuration:", clipDuration, "\n");
    post("mode:", mode, "\n");
    post("direction:", direction, "\n");
    post("ratioNum:", ratioNum, "ratioDen:", ratioDen, "\n");

    var totalOutputBeats = clipDuration;

    var metabarBeats;
    if (mode === "ramp") {
        metabarBeats = totalOutputBeats;
    } else {
        metabarBeats = totalOutputBeats / 2;
    }

    // Normalize ratio to always be > 1 - direction controls tempo change direction
    var ratioValue = Math.max(ratioNum, ratioDen) / Math.min(ratioNum, ratioDen);
    post("ratioValue (normalized):", ratioValue, "\n");
    post("metabarBeats:", metabarBeats, "\n");

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
    post("setRatio called with:", num, den, "\n");
    ratioNum = Math.max(1, Math.min(9, num));
    ratioDen = Math.max(1, Math.min(9, den));
    post("ratioNum:", ratioNum, "ratioDen:", ratioDen, "\n");
}

function setDirection(dir) {
    post("setDirection called with:", dir, "\n");
    if (dir === "accel" || dir === "decel" || dir === 0 || dir === 1) {
        direction = (dir === 0 || dir === "accel") ? "accel" : "decel";
    }
    post("direction:", direction, "\n");
}

function setMode(m) {
    post("setMode called with:", m, "\n");
    if (m === "arc" || m === "ramp" || m === 0 || m === 1) {
        mode = (m === 0 || m === "arc") ? "arc" : "ramp";
    }
    post("mode:", mode, "\n");
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

function setVelocityCurve(gamma) {
    // Range: 0.5 (hard/compensatory) to 3.0 (soft/conservative)
    velocityGamma = Math.max(0.5, Math.min(3.0, gamma));
    post("velocityGamma:", velocityGamma, "\n");
}

function bang() {
    post("bang received\n");
    generate();
}

function anything() {
    var args = arrayfromargs(messagename, arguments);
    post("anything received:", args, "\n");
}

/**
 * Handle dictionary input from live.miditool.in
 * Outlet 1 sends notes dictionary (triggers generate)
 * Outlet 2 sends clip/scale/grid info (extract duration)
 */
function dictionary(dictName) {
    var d = new Dict(dictName);
    var keys = d.getkeys();

    post("Dictionary received:", dictName, "\n");
    post("Keys:", keys, "\n");

    // Check if this is the clip info dictionary (outlet 2)
    if (d.contains("clip")) {
        var clipDict = d.get("clip");
        if (clipDict) {
            var selStart = d.get("clip::time_selection_start");
            var selEnd = d.get("clip::time_selection_end");
            post("time_selection_start:", selStart, "time_selection_end:", selEnd, "\n");
            if (selStart !== undefined && selEnd !== undefined && selEnd > selStart) {
                clipDuration = selEnd - selStart;
                post("Set clipDuration from clip info:", clipDuration, "\n");
            }
        }
        // Don't generate yet - wait for notes dictionary
        return;
    }

    // Check if this is the notes dictionary (outlet 1) - triggers generate
    if (d.contains("notes")) {
        post("Notes dictionary received, generating with clipDuration:", clipDuration, "\n");
        generate();
    }
}
