import xml.etree.ElementTree as ET
from random import shuffle
from pathlib import Path

from working_set_manager import WorkingSetManager


class TextRandomizer(WorkingSetManager):
    def __init__(self, working_set: dict) -> None:
        super().__init__(working_set)

    def parse_xml(self, xml_path: Path) -> ET.ElementTree | None:
        try:
            tree = ET.parse(xml_path)
            return tree
        except FileNotFoundError:
            self.logger.error(f"File {xml_path} not found.")
            # self.report_error(f"File {xml_path} not found.")
        except ET.ParseError:
            self.logger.error(f"Unable to parse {xml_path}. Probably bad xml.")
            # self.report_error(
            #     f"Unable to parse {xml_path}. Probably bad xml."
            # )
        except PermissionError:
            self.logger.error(f"Permission error: {xml_path}")
            # self.report_error(f"Permission error: {xml_path}")

    def write_xml(self, text: list, groups: list) -> None:
        li = 0

        for xml_info in groups:
            for path, info in xml_info.items():
                xml_path = self.game_path / path
                root = self.parse_xml(xml_path)

                for tag in root.iter(info["tag"]):
                    if not self.validate_tag(info, tag.attrib):
                        continue

                    tag.set(info["text"], text[li])
                    li += 1

                root.write(xml_path, encoding="windows-1251")

    def collect_data_from_xml(self, groups: list) -> list:
        text = []
        for xml_info in groups:
            for path, info in xml_info.items():
                xml_path = self.game_path / path
                root = self.parse_xml(xml_path)
                if not root:
                    continue

                for tag in root.iter(info["tag"]):
                    if not self.validate_tag(info, tag.attrib):
                        continue
                    text.append(tag.attrib[info["text"]])

        return text

    def validate_tag(self, xml_options: dict, tag_attribs: dict) -> bool:
        """
        Validates if xml tag has attributes name and text.

        attributes from xml_options,
        if text attribute is not empty and if this tag
        need to be excluded/included
        manually via manifest settings.

        Returns:
            True if attributes present\n
            False otherwise.
        """
        if xml_options["text"] not in tag_attribs:
            return False
        if xml_options["name"] not in tag_attribs:
            return False
        if not self.xml_include_or_exclude(xml_options, tag_attribs):
            return False
        if not tag_attribs.get(xml_options["text"]):
            return False
        return True

    def xml_include_or_exclude(
        self,
        xml_options: dict,
        tag_attribs: dict
    ) -> bool:
        name: str = tag_attribs[xml_options["name"]]

        if "exclude" in xml_options:
            for ending in xml_options["exclude"]:
                if name.endswith(ending):
                    return False
            return True

        elif "include" in xml_options:
            for ending in xml_options["include"]:
                if not name.endswith(ending):
                    return False
            return True
        else:
            return True

    def randomize(self, groups: list) -> None:
        text = self.collect_data_from_xml(groups)

        shuffle(text)

        self.write_xml(text, groups)

    def start_randomization(self) -> None:
        if not self.text:
            self.logger.info("Nothing to randomize.")
            return
        for groups in self.text:
            self.randomize(groups)
