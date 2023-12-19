from config import Config
from randomizer import Randomizer

from random import shuffle
from icecream import ic
from pathlib import Path

import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger("pavlik")

class TextRandomizer(Randomizer):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

        self.options = self.manifest.get("Text")
    
    def parse_xml(self, xml_path: Path) -> ET.ElementTree | None:
        try:
            tree = ET.parse(xml_path)
            return tree
        except FileNotFoundError:
            self.report_error(f"File {xml_path} not found.")
        except ET.ParseError:
            self.report_error(f"Unable to parse {xml_path}. Probably bad xml.")
        except PermissionError:
            self.report_error(f"Permission error: {xml_path}")
    
    def write_xml(self, text: list, xml_info: dict) -> None:
        li = 0

        for path, info in xml_info.items():
            xml_path = self.game_path / path
            root = self.parse_xml(xml_path)

            for tag in root.iter(info.get("tag")):
                if not self.validate_tag(info, tag.attrib):
                    continue

                tag.set(info.get("text"), text[li])
                li += 1
            
            root.write(xml_path, encoding="windows-1251")

    def collect_data_from_xml(self, xml_info: dict) -> list:
        text = []

        for path, info in xml_info.items():
            xml_path = self.game_path / path
            root = self.parse_xml(xml_path)
            if not root: continue

            for tag in root.iter(info.get("tag")):
                if not self.validate_tag(info, tag.attrib):
                    continue
                text.append(tag.attrib.get(info.get("text")))
        
        return text
    
    def validate_tag(self, xml_options: dict, tag_attribs: dict) -> bool:
        """
        Validates if xml tag has attributes name and text attributes from xml_options,
        if text attribute is not empty and if this tag need to be excluded/included 
        manually via manifest settings.
        Returns False if not.
        """
        if not xml_options.get("text") in tag_attribs:
            return False
        if not xml_options.get("name") in tag_attribs:
            return False
        if not self.xml_include_or_exclude(xml_options, tag_attribs):
            return False
        if not tag_attribs.get(xml_options.get("text")):
            return False
        return True
    
    def xml_include_or_exclude(self, xml_options: dict, tag_attribs: dict) -> bool:
        name: str = tag_attribs.get(xml_options.get("name"))

        if "exclude" in xml_options:
            for ending in xml_options.get("exclude"):
                if name.endswith(ending):
                    return False
            return True
        
        elif "include" in xml_options:
            for ending in xml_options.get("include"):
                if not name.endswith(ending):
                    return False
            return True
        else:
            return True

    def randomize(self, group: dict) -> None:
        text = self.collect_data_from_xml(group)

        shuffle(text)

        self.write_xml(text, group)

    def start_randomization(self) -> None:
        working_set = self.configure_randomization()
        for group in working_set:
            self.randomize(group)
        
