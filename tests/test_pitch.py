"""Tests für die Regel-Engine. Entferne den Skip, sobald note_name() implementiert ist."""

import pytest

from notenamer.pitch import note_name

pytestmark = pytest.mark.skip(reason="note_name() noch nicht implementiert")


def test_treble_bottom_line_is_e():
    assert note_name("treble", 0, 0, {}) == "E"


def test_bass_bottom_line_is_g():
    assert note_name("bass", 0, 0, {}) == "G"


def test_german_h_vs_english_b():
    assert note_name("treble", 4, 0, {}, naming="de") == "H"
    assert note_name("treble", 4, 0, {}, naming="en") == "B"


def test_key_signature_one_sharp():
    assert note_name("treble", 1, 1, {}) == "Fis"


def test_natural_cancels_key_signature_until_barline():
    assert note_name("treble", 1, 1, {1: "natural"}) == "F"
