"""Rule engine: determine a note name from clef, staff position and accidentals.

This module deliberately contains no ML. It is fully covered by unit tests so that
every later error can be attributed clearly to either the model or the logic.
"""

from typing import Literal

Clef = Literal["treble", "bass"]
Accidental = Literal["sharp", "flat", "natural"]
Naming = Literal["de", "en"]


def note_name(
    clef: Clef,
    staff_position: int,
    key_signature: int,
    accidentals_in_measure: dict[int, Accidental],
    naming: Naming = "de",
) -> str:
    """Return the name of a note.

    Args:
        clef: Clef at the start of the staff or at this point in the staff.
        staff_position: Position on the staff. 0 = bottom line, 1 = first space,
            2 = second line and so on. Negative values and values above 8 are on ledger lines.
        key_signature: Positive = number of sharps, negative = number of flats, 0 = none.
        accidentals_in_measure: Accidentals already set in this measure before this note,
            as {staff_position: accidental}. They apply until the barline.
        naming: "de" (C D E F G A H, Fis, B) or "en" (C D E F G A B, F#, Bb).

    Returns:
        The note name, e.g. "Fis" or "F#".
    """
    raise NotImplementedError("See issue 1.1")
