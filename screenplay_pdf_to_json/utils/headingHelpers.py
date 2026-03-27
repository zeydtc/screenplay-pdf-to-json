import re

headingEnum = [
    # English headings
    "EXT./INT.", "EXT/INT.", "INT./EXT.", "EXT/INT", "INT/EXT",
    "INT.", "EXT.", "INT --", "EXT --", "I/E.",
    # French headings
    "EXT./", "EXT/", "INT./", "INT/",
    # German headings
    "INNEN/AUSSEN.", "AUSSEN/INNEN.", "INNEN/AUßEN.", "AUßEN/INNEN.",
    "INNEN.", "AUSSEN.", "AUßEN.",
    # Spanish headings
    "EXT./INT.", "EXT/INT.", "INT./EXT.", "EXT/INT", "INT/EXT",
    "INT.", "EXT.", "INT --", "EXT --", "I/E."
]


def isHeading(content):
    text = content["text"]
    for heading in headingEnum:
        if not text.endswith(heading) and heading in text:
            return True
    # German reversed format: LOCATION / INNEN/TIME or LOCATION / AUSSEN/TIME
    if re.search(r'/ (?:INNEN|AU(?:SS|ß)EN)(?:/\w+)?$', text):
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
        "CRÉPUSCULE",

        # German
        "TAG",
        "NACHT",
        "MORGEN",
        "MORGENS",
        "ABEND",
        "ABENDS",
        "NACHMITTAG",
        "NACHMITTAGS",
        "DÄMMERUNG",
        "SPÄTER",
        "FORTLAUFEND",
        "SONNENUNTERGANG",

        # Spanish
        "NOCHE",
        "TARDE",
        "MAÑANA",
        "DÍAS",
        "DÍA",
        "NOCHE",
        "DÍAS",
        "DÍA",
        "OTRO DÍA",
        "DESPUÉS",
        "NOCHE",
        "MISMO",
        "CONTINUO",
        "MOMENTOS DESPUÉS",
        "DESPUÉS",
        "ATARDECER"
    ])
    regex = '[-,]?[ ]?(DAWN|DUSK|((LATE|EARLY) )?' + timeVocab + ')|\d{4}'
    findTime = re.search(regex, text)

    time = list(filter(lambda x: len(x) > 0, [x.strip(
        "-,. ") for x in text[findTime.start():].split()])) if findTime else None
    return time

# TODO: French scenes aren't being detected properly:
# Only the first word is being detected as the region, the rest is considered part of time.
# We need to fix this by doing the following:
# Check whether it's an English heading, if so proceed normally, if it's not then check for french with its cases separately
# in a different function and distinguish between the region, time and location accordingly.
def extractHeading(text):
    """
    English formats:
    EXT./INT., INT./EXT., EXT/INT, INT/EXT
    EXT., INT., EXT --, INT --
    I/E.

    French formats:
    EXT./, EXT/, INT./, INT/

    German formats:
    INNEN., AUSSEN., AUßEN.
    INNEN/AUSSEN., AUSSEN/INNEN., INNEN/AUßEN., AUßEN/INNEN.

    German reversed format (location-first):
    LOCATION / INNEN/TIME
    LOCATION / SUBLOCATION / AUSSEN/TIME

    Spanish formats:
    EXT./INT., INT./EXT., EXT/INT, INT/EXT
    EXT., INT., EXT --, INT --
    I/E.
    """
    # German reversed format: LOCATION / INNEN/TIME or LOCATION / AUSSEN/TIME
    german_reversed = re.search(r'^(.*)\s*/\s*(INNEN|AU(?:SS|ß)EN)(?:/(\w+))?$', text)
    if german_reversed:
        location = german_reversed.group(1).strip().strip('-,. /')
        region = german_reversed.group(2).replace('AUSSEN', 'AUßEN')
        time_word = german_reversed.group(3)
        return {
            "region": region,
            "location": location,
            "time": [time_word] if time_word else None
        }

    # print('new scene: ', text)
    region = re.search(
        r'((?:.* )?(?:EXT[\.]?\/(?:INT[\.]?|)?|INT[\.]?\/(?:EXT[\.]?|)?|INT(?:\.| --)|EXT(?:\.| --)|I\/E\.|INNEN[\.]?\/AU(?:SS|ß)EN[\.]?|AU(?:SS|ß)EN[\.]?\/INNEN[\.]?|INNEN\.|AU(?:SS|ß)EN\.))', text).groups()[0]

    # print('region: ', region)

    time = extractTime(text)

    # print('time: ', time)

    location = text.replace(region, "")

    # For french headings, remove '/'
    if region.endswith("/"):
        region = region[:-1]

    # Normalize German AUSSEN to AUßEN
    region = region.replace("AUSSEN", "AUßEN")

    # print('location: ', location)

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

