import pytest
from screenplay_pdf_to_json.utils import extractHeading


def createMockContent(text):
    return {
        "x": 3,
        "y": 4,
        "text": text
    }


def setupMultipleHeadings(headings):
    headings = [createMockContent(heading) for heading in headings]

    headings = [extractHeading(content["text"]) for content in headings]
    return headings


def assertGroup(headings, expectedHeadings):
    i = 0
    while i < len(headings):
        assert headings[i]["region"] == expectedHeadings[i]["region"]
        assert headings[i]["location"] == expectedHeadings[i]["location"]
        i += 1


def test_multiple_locaitons():
    headings = [
        'THE PAST. INT. CONCORD. MARCH HOUSE. JO & MEG’S ROOM. 1861.',
    ]
    headings = setupMultipleHeadings(headings)

    expectedHeadings = [
        {
            "region": "THE PAST. INT.",
            "location": "CONCORD. MARCH HOUSE. JO & MEG’S ROOM",
        },
    ]

    assertGroup(headings, expectedHeadings)


def test_one_location():
    headings = [
        'INT. GERMAN BEER HALL. NIGHT. 1868.',
        'INT. SHAFT. LATER.',
    ]
    headings = setupMultipleHeadings(headings)

    expectedHeadings = [
        {
            "region": "INT.",
            "location": "GERMAN BEER HALL",
        },
        {
            "region": "INT.",
            "location": "SHAFT",
        },
    ]

    assertGroup(headings, expectedHeadings)


def test_both_int_ext():
    headings = [
        'INT/EXT. GERMAN BEER HALL. NIGHT. 1868.',
        'INT./EXT GERMAN BEER HALL. NIGHT. 1868.',
        'INT./EXT. GERMAN BEER HALL. NIGHT. 1868.',
    ]
    headings = setupMultipleHeadings(headings)

    expectedHeadings = [
        {
            "region": "INT/EXT.",
            "location": "GERMAN BEER HALL",
        },
        {
            "region": "INT./EXT",
            "location": "GERMAN BEER HALL",
        },
        {
            "region": "INT./EXT.",
            "location": "GERMAN BEER HALL",
        },
    ]

    assertGroup(headings, expectedHeadings)


def test_german_innen():
    headings = [
        'INNEN. WOHNZIMMER - TAG',
    ]
    headings = setupMultipleHeadings(headings)

    expectedHeadings = [
        {
            "region": "INNEN.",
            "location": "WOHNZIMMER",
        },
    ]

    assertGroup(headings, expectedHeadings)


def test_german_aussen():
    headings = [
        'AUSSEN. STRASSE - NACHT',
        'AUßEN. PARKPLATZ - TAG',
    ]
    headings = setupMultipleHeadings(headings)

    expectedHeadings = [
        {
            "region": "AUßEN.",
            "location": "STRASSE",
        },
        {
            "region": "AUßEN.",
            "location": "PARKPLATZ",
        },
    ]

    assertGroup(headings, expectedHeadings)


def test_german_innen_aussen():
    headings = [
        'INNEN/AUSSEN. AUTO - MORGEN',
        'INNEN/AUßEN. HAUS - ABEND',
        'AUSSEN/INNEN. BÜRO - SPÄTER',
        'AUßEN/INNEN. SCHULE - TAG',
    ]
    headings = setupMultipleHeadings(headings)

    expectedHeadings = [
        {
            "region": "INNEN/AUßEN.",
            "location": "AUTO",
        },
        {
            "region": "INNEN/AUßEN.",
            "location": "HAUS",
        },
        {
            "region": "AUßEN/INNEN.",
            "location": "BÜRO",
        },
        {
            "region": "AUßEN/INNEN.",
            "location": "SCHULE",
        },
    ]

    assertGroup(headings, expectedHeadings)


def test_german_reversed_format():
    headings = [
        'RESERVAT / KONTROLLZENTRUM CHIEF / INNEN/ABEND',
        'RESERVAT / KONTROLLZENTRUM / INNEN/ABEND',
        'RESERVAT / BEI BUSCH AN STRASSE / AUSSEN/ABEND',
    ]
    headings = setupMultipleHeadings(headings)

    expectedHeadings = [
        {
            "region": "INNEN",
            "location": "RESERVAT / KONTROLLZENTRUM CHIEF",
        },
        {
            "region": "INNEN",
            "location": "RESERVAT / KONTROLLZENTRUM",
        },
        {
            "region": "AUßEN",
            "location": "RESERVAT / BEI BUSCH AN STRASSE",
        },
    ]

    assertGroup(headings, expectedHeadings)
