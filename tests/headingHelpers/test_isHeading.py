import pytest
from screenplay_pdf_to_json.utils import isHeading, extractTime, extractHeading


def createMockContent(text):
    return {
        "x": 3,
        "y": 4,
        "text": text
    }


def test_word_region_first():
    text = createMockContent(
        'INT. GERMAN BEER HALL. NIGHT. 1868.')
    assert isHeading(text) == True


def test_word_before_region():
    text = createMockContent(
        'THE PAST. INT. CONCORD. MARCH HOUSE. JO & MEG’S ROOM. 1861.')
    assert isHeading(text) == True


def test_region_location_time():
    text = createMockContent(
        'EXT. WATERFORD HOUSE - CONTINUOUS')
    assert isHeading(text) == True


def test_ext_int_combo():
    text1 = createMockContent(
        'EXT/INT. WATERFORD HOUSE - CONTINUOUS')
    text2 = createMockContent(
        'INT/EXT. WATERFORD HOUSE - CONTINUOUS')
    assert isHeading(text1) == True
    assert isHeading(text2) == True


def test_region_location():
    text = createMockContent(
        'INT. ELEVATOR')
    assert isHeading(text) == True


def test_time_2_dashes():
    text = createMockContent(
        'INT. DON DRAPER’S OFFICE -- LATER')
    assert isHeading(text) == True


def test_word_before_region():
    text = createMockContent(
        'RIGHT IN THE STINT.')
    assert isHeading(text) == False


def test_german_innen():
    text = createMockContent(
        'INNEN. WOHNZIMMER - TAG')
    assert isHeading(text) == True


def test_german_aussen():
    text = createMockContent(
        'AUSSEN. STRASSE - NACHT')
    assert isHeading(text) == True


def test_german_aussen_eszett():
    text = createMockContent(
        'AUßEN. PARKPLATZ - TAG')
    assert isHeading(text) == True


def test_german_innen_aussen_combo():
    text1 = createMockContent(
        'INNEN/AUSSEN. AUTO - MORGEN')
    text2 = createMockContent(
        'AUSSEN/INNEN. HAUS - ABEND')
    assert isHeading(text1) == True
    assert isHeading(text2) == True


def test_german_innen_aussen_eszett_combo():
    text1 = createMockContent(
        'INNEN/AUßEN. AUTO - MORGEN')
    text2 = createMockContent(
        'AUßEN/INNEN. HAUS - ABEND')
    assert isHeading(text1) == True
    assert isHeading(text2) == True


def test_german_reversed_innen():
    text = createMockContent(
        'RESERVAT / KONTROLLZENTRUM / INNEN/ABEND')
    assert isHeading(text) == True


def test_german_reversed_aussen():
    text = createMockContent(
        'RESERVAT / BEI BUSCH AN STRASSE / AUSSEN/ABEND')
    assert isHeading(text) == True


def test_german_reversed_multi_location():
    text = createMockContent(
        'RESERVAT / KONTROLLZENTRUM CHIEF / INNEN/ABEND')
    assert isHeading(text) == True
