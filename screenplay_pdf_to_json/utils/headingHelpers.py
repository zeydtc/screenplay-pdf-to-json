import re

headingEnum = [
    # English headings
    "EXT./INT.", "EXT/INT.", "INT./EXT.", "EXT/INT", "INT/EXT",
    "INT.", "EXT.", "INT --", "EXT --", "I/E.",
    # French headings
    "EXT./", "EXT/", "INT./", "INT/"
]


def isHeading(content):
    text = content["text"]
    for heading in headingEnum:
        if not text.endswith(heading) and heading in text:
            return True
    return False


def extractTime(text):
    timeVocab = "|".join([
        "NIGHT",
        "AFTERNOON",
        "MORNING",
        "DAYS",
        "DAY",
        "NIGHT",
        "DAYS",
        "DAY",
        "ANOTHER DAY",
        "LATER",
        "NIGHT",
        "SAME",
        "CONTINUOUS",
        "MOMENTS LATER",
        "LATER",
        "SUNSET",

        # French 
        "JOUR",
        "MATIN",
        "NUIT",
        "SOIR",
        "AUBE",
        "CRÉPUSCULE"
    ])
    regex = '[-,]?[ ]?(DAWN|DUSK|((LATE|EARLY) )?' + timeVocab + ')|\d{4}'
    findTime = re.search(
        regex, text)

    time = list(filter(lambda x: len(x) > 0, [x.strip(
        "-,. ") for x in text[findTime.start():].split()])) if findTime else None
    return time


def extractHeading(text):
    """
    English formats:
    EXT./INT., INT./EXT., EXT/INT, INT/EXT
    EXT., INT., EXT --, INT --
    I/E.

    French formats:
    EXT./, EXT/, INT./, INT/
    """
    region = re.search(
        r'((?:.* )?(?:EXT[\.]?\/(?:INT[\.]?|)?|INT[\.]?\/(?:EXT[\.]?|)?|INT(?:\.| --)|EXT(?:\.| --)|I\/E\.))', text).groups()[0]

    time = extractTime(text)

    location = text.replace(region, "")

    if time and len(time) > 0:
        location = location[:location.index(time[0])]

    if len(region) > 0 and region[0].isdigit():
        region = region.lstrip('0123456789.- ')
        location = location.rstrip('0123456789.- ') if location else location
    time = time[:-1] if time and time[-1].isdigit() else time

    return {
        "region": region,
        "location": location.strip("-,. "),
        "time": time
    }

