import xml.etree.ElementTree as ET
from random import shuffle
from pathlib import Path

from config import Config
from text_randomizer import TextRandomizer


class ModelsRandomizer(TextRandomizer):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

        self.options = self.manifest.get("Models")

    def clear_animmodels(self) -> None:
        """
        Clears animmodels.xml from duplicates that original game has.
        """
        animmodels_path = self.game_path / Path("data/models/animmodels.xml")
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

    def randomize(self, group: dict) -> None:
        for path, info in group.items():
            xml_path = self.game_path / path
            root = self.parse_xml(xml_path)

            for tag in root.iter(info.get("tag")):
                if info.get("name") in tag.attrib:
                    if tag.attrib.get(info.get("name")) in info.get("models"):
                        tag.set(info.get("name"), "PLACEHOLDER")

            shuffle(info.get("models"))

            li = 0
            for tag in root.iter(info.get("tag")):
                if info.get("name") in tag.attrib:
                    if "PLACEHOLDER" == tag.attrib.get(info.get("name")):
                        tag.set(info.get("name"), info.get("models")[li])
                        li += 1

            self.write_xml(root, xml_path)

    def start_randomization(self) -> None:
        working_set = self.configure_randomization()
        if not working_set:
            self.logger.info("Nothing to randomize.")
            return
        if self.game_version == "steam":
            self.clear_animmodels()
        for group in working_set:
            self.randomize(group)
