import xml.etree.ElementTree as ET
from random import shuffle
from pathlib import Path

from text_randomizer import TextRandomizer


class ModelsRandomizer(TextRandomizer):
    def __init__(self, working_set) -> None:
        super().__init__(working_set)

        # self.options = self.manifest.get("models")

    def clear_animmodels(self) -> None:
        """
        Clears animmodels.xml from duplicates that original game has.
        """
        animmodels_path = self.game_path / "data/models/animmodels.xml"
        root = self.parse_xml(animmodels_path)

        for tag in root.iter("model"):
            if "file" in tag.attrib:
                if tag.attrib.get("file") == "data\\models\\ammo\\shell02.gam":
                    del tag.attrib["id"]
                    del tag.attrib["file"]

        for duplicate in [
            "data\\models\\buildings\\region4\\kladbishe\\1_riback.gam",
            "data\\models\\buildings\\region2\\helvecia.gam"
        ]:
            status = 0
            for tag in root.iter("model"):
                if "file" in tag.attrib:
                    if tag.attrib.get("file") == duplicate:
                        if status == 1:
                            del tag.attrib["id"]
                            del tag.attrib["file"]
                        elif status == 0:
                            status = 1

        self.write_xml(root, animmodels_path)

    def write_xml(self, parsed_file: ET.ElementTree, xml_path: Path) -> None:
        parsed_file.write(xml_path, encoding="windows-1251")

    def randomize(self, groups: list) -> None:
        for group in groups:
            xml_path = self.game_path / self.path
            root = self.parse_xml(xml_path)

            for tag in root.iter(self.tag):
                if self.name in tag.attrib:
                    if tag.attrib.get(self.name) in group:
                        tag.set(self.name, "PLACEHOLDER")

            shuffle(group)

            li = 0
            for tag in root.iter(self.tag):
                if self.name in tag.attrib:
                    if "PLACEHOLDER" == tag.attrib.get(self.name):
                        tag.set(self.name, group[li])
                        li += 1

            self.write_xml(root, xml_path)

    def start_randomization(self) -> None:
        if not self.models:
            self.logger.info("Nothing to randomize.")
            return

        self.tag = self.models[0]["tag"]
        self.name = self.models[0]["name"]
        self.path = self.models[0]["path"]

        if self.game_version == "steam":
            self.clear_animmodels()
        for groups in self.models:
            self.randomize(groups["groups"])
