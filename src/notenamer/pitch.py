"""Regel-Engine: aus Schlüssel, Linienposition und Vorzeichen einen Notennamen bestimmen.

Dieses Modul ist bewusst frei von ML. Es wird vollständig mit Unit-Tests abgesichert,
damit sich später jeder Fehler eindeutig dem Modell oder der Logik zuordnen lässt.
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
    """Bestimmt den Namen einer Note.

    Args:
        clef: Schlüssel am Anfang bzw. an dieser Stelle des Systems.
        staff_position: Position auf dem System. 0 = unterste Linie, 1 = erster Zwischenraum,
            2 = zweite Linie usw. Negative Werte und Werte über 8 liegen auf Hilfslinien.
        key_signature: Generalvorzeichen. Positiv = Anzahl Kreuze, negativ = Anzahl b, 0 = keine.
        accidentals_in_measure: Versetzungszeichen, die in diesem Takt vor dieser Note bereits
            gesetzt wurden, als {staff_position: Vorzeichen}. Sie gelten bis zum Taktstrich.
        naming: "de" (C D E F G A H, Fis, B) oder "en" (C D E F G A B, F#, Bb).

    Returns:
        Den Notennamen, z. B. "Fis" oder "F#".
    """
    raise NotImplementedError("Siehe Issue «note_name(): Tonhöhe aus Schlüssel und Linienposition»")
