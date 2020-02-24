import copy


class GroupTypes:
    def __init__(self, script):
        self.script = script
        self.newScript = []

    headingEnum = ["INT.", "EXT.", "INT./EXT.", "EXT./INT."]

    timeEnum = {
        "DAY": "DAY",
        "NIGHT": "NIGHT",
        "MORNING": "MORNING"
    }

    characterNameEnum = {
        "VOICE_OVER": "V.O.",
        "OFF_SCREEN": "O.S.",
        "CONTINUED": "CONT'D"
    }

    def determineHeading(self, textArr):
        for heading in self.headingEnum:
            if heading in textArr[0]:
                return True
        return False

    def determineDay(self, text):
        for heading in self.timeEnum:
            if heading in text:
                return True
        return False

    def determineCharacter(self, textArr):
        # char only have one line
        if len(textArr) > 1:
            return False

        character = textArr[0].split()
        if character[0] != character[0].upper():
            return False

        if len(character) > 1:
            if "(" not in character[-1]:
                return False
        elif len(character) == 1:
            if "(" in character[0]:
                return False
        # check if header?
        if "." in character[0]:
            return False
        return True

    def containsParentheticals(self, text):
        return "(" in text[0] and ")" in text[-1]

    def containsDialogue(self, y, upperY, x, correctMargin, correctWidth):
        return abs(upperY - y) <= correctMargin and abs(correctWidth - x) <= 5

    # extracts either dialogue 1 or dialogue 2 (if it's a dual dialogue)
    def getWhichDialogue(self, scene, content, i, whichDialogue):
        character = "character1" if whichDialogue == "segment" else "character2"

        correctMargin = abs(content[i-1][whichDialogue]
                            ["y"] - content[i][whichDialogue]["y"]) if whichDialogue in content[i-1] and whichDialogue in content[i] else False

        correctWidth = content[i][whichDialogue]["x"]if whichDialogue in content[i] else False

        while i < len(content):
            parenthetical = self.containsParentheticals(
                content[i][whichDialogue]["text"][0]) if whichDialogue in content[i] else False

            dialogue = self.containsDialogue(
                content[i][whichDialogue]["y"], content[i-1][whichDialogue]["y"],  content[i][whichDialogue]["x"], correctMargin, correctWidth) if (
                whichDialogue in content[i] and correctMargin != False and correctWidth != False) else False

            if dialogue:
                print(correctMargin)
                print(abs(content[i][whichDialogue]["y"] -
                          content[i-1][whichDialogue]["y"]))

            if (parenthetical or dialogue):
                meta = "parenthetical" if parenthetical else "dialogue"
                scene["nest"][-1][character]["dialogue"].append({
                    "type": meta,
                    "text": content[i][whichDialogue]["text"]
                })
            else:
                break
            i += 1
        return (scene, i - 1)

    def extractCharacter(self, scene, currentTextObj, content, i):
        split = currentTextObj["segment"]["text"][0].split()
        stitchedDialogue = {
            "character1": {
                "character": split[0],
                "modifier": split[1] if len(split) > 1 else None,
                "x": currentTextObj["segment"]["x"],
                "y": currentTextObj["segment"]["y"],
                "dialogue": []
            }
        }

        if "character2" in currentTextObj:
            split = currentTextObj["character2"]["text"][0].split()
            stitchedDialogue["character2"] = ({
                "character": split[0],
                "modifier": split[1] if len(split) > 1 else None,
                "x": currentTextObj["character2"]["x"],
                "y": currentTextObj["character2"]["y"],
                "dialogue": []
            })

        scene["nest"].append(stitchedDialogue)

        (scene, j) = self.getWhichDialogue(
            scene, content, i + 1, "segment")

        if "character2" in currentTextObj:
            (scene, j) = self.getWhichDialogue(
                scene, content, i + 1, "character2")
        return (scene, j)

    def extractHeader(self, text):
        curr = text[0].split(".")
        location = []
        time = None
        region = curr[0]
        if len(curr) > 1:
            divider = "."
            dayOrNot = self.determineDay(curr[len(curr) - 1])
            location = curr[1:-1] if dayOrNot else curr

            if (len(curr) == 2):
                divider = ","
                if any("-" in el for el in curr):
                    divider = "-"
                curr = curr[1].split(divider)
                location = curr[0:-1] if dayOrNot else curr

            time = curr[len(curr) - 1] if dayOrNot else None

        return {
            "region": region,
            "location": location,
            "time": time
        }

    def groupTypes(self, pageWidth):
        groupedTypes = []
        scene = {
            "region": None,
            "location": None,
            "time": None,
            "nest": []
        }

        for page in self.script:
            groupedTypes.append({"page": page["page"], "content": []})
            i = 0
            content = page["content"]
            while i < len(content):
                currentTextObj = content[i]
                if self.determineHeading(currentTextObj["segment"]["text"]):
                    if len(scene["nest"]) > 0:
                        groupedTypes[-1]["content"].append(copy.copy(scene))
                    heading = self.extractHeader(
                        currentTextObj["segment"]["text"])
                    region = heading["region"]
                    location = heading["location"]
                    time = heading["time"]
                    scene = {
                        "region": region,
                        "location": location,
                        "time": time,
                        "nest": []
                    }
                if self.determineCharacter(currentTextObj["segment"]["text"]) and i + 1 < len(content):
                    (scene, x) = self.extractCharacter(
                        scene, currentTextObj, content, i)
                    i = x
                else:
                    scene["nest"].append(currentTextObj)
                i += 1
            groupedTypes[-1]["content"].append(copy.copy(scene))
            scene["nest"] = []
            # if page["page"] == 0:
            #     break

        self.newScript = groupedTypes
