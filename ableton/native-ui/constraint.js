/**
 * Ratio Constraint Enforcer for Risset Generator Native UI
 *
 * Enforces:
 * - Accel (direction=0): numerator < denominator
 * - Decel (direction=1): numerator > denominator
 */

inlets = 3;  // 0: direction, 1: numerator, 2: denominator
outlets = 2; // 0: corrected numerator, 1: corrected denominator

var direction = 0;  // 0 = accel, 1 = decel
var num = 2;
var den = 3;

function setDirection(d) {
    direction = d;
    enforce();
}

function setNum(n) {
    num = Math.max(1, Math.min(9, n));
    enforce();
}

function setDen(d) {
    den = Math.max(1, Math.min(9, d));
    enforce();
}

function msg_int(v) {
    if (inlet === 0) {
        setDirection(v);
    } else if (inlet === 1) {
        setNum(v);
    } else if (inlet === 2) {
        setDen(v);
    }
}

function enforce() {
    var correctedNum = num;
    var correctedDen = den;

    if (direction === 0) {
        // Accel: num must be < den
        if (num >= den) {
            // Swap so smaller is on top
            correctedNum = Math.min(num, den);
            correctedDen = Math.max(num, den);
            // If equal, adjust
            if (correctedNum === correctedDen) {
                if (correctedDen < 9) {
                    correctedDen = correctedNum + 1;
                } else {
                    correctedNum = correctedDen - 1;
                }
            }
        }
    } else {
        // Decel: num must be > den
        if (num <= den) {
            // Swap so larger is on top
            correctedNum = Math.max(num, den);
            correctedDen = Math.min(num, den);
            // If equal, adjust
            if (correctedNum === correctedDen) {
                if (correctedNum < 9) {
                    correctedNum = correctedDen + 1;
                } else {
                    correctedDen = correctedNum - 1;
                }
            }
        }
    }

    // Clamp to valid range
    correctedNum = Math.max(1, Math.min(9, correctedNum));
    correctedDen = Math.max(1, Math.min(9, correctedDen));

    // Keep the corrected values so the next edit starts from what is displayed
    num = correctedNum;
    den = correctedDen;

    // Output corrected values (right to left in Max)
    outlet(1, correctedDen);
    outlet(0, correctedNum);
}

function bang() {
    enforce();
}
