from random import shuffle

from config import Config
from models_randomizer import ModelsRandomizer


class BarNpcRandomizer(ModelsRandomizer):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

        self.options = self.manifest.get("bar_npc_models")

    def collect_data_from_xml(self, xml_info: dict) -> list:
        npcs_outfit = []
        for level in xml_info.get("maps"):
            xml_path = self.game_path / level / xml_info.get("file")
            root = self.parse_xml(xml_path)

            for tag in root.iter(xml_info.get("tag")):
                if not xml_info.get("name") in tag.attrib:
                    continue
                if "prototype" in xml_info:
                    if not tag.attrib.get(
                        xml_info.get("name")
                    ) == xml_info.get("prototype"):
                        continue

                outfit = {}

                for option in xml_info.get("config"):
                    if option in tag.attrib:
                        outfit.update({option: tag.attrib.get(option)})

                npcs_outfit.append(outfit)

        return npcs_outfit

    def set_data_to_xml(self, xml_info: dict, content: list[dict]) -> None:
        li = 0
        for level in xml_info.get("maps"):
            xml_path = self.game_path / level / xml_info.get("file")
            root = self.parse_xml(xml_path)

            for tag in root.iter(xml_info.get("tag")):
                if not xml_info.get("name") in tag.attrib:
                    continue
                if "prototype" in xml_info:
                    if not tag.attrib.get(
                        xml_info.get("name")
                    ) == xml_info.get("prototype"):
                        continue

                for option in xml_info.get("config"):
                    # removing modelAutosized tag
                    # because it breaks normal mask models
                    if "modelAutosized" in tag.attrib:
                        tag.attrib.pop("modelAutosized")
                    if option not in content[li]:
                        continue

                    tag.set(option, content[li].get(option))

                li += 1

            self.write_xml(root, xml_path)

    def randomize(self, group: dict) -> None:
        npcs_outfit = self.collect_data_from_xml(group)

        shuffle(npcs_outfit)

        self.set_data_to_xml(group, npcs_outfit)

    def start_randomization(self) -> None:
        working_set = self.configure_randomization()
        if not working_set:
            self.logger.info("Nothing to randomize.")
            return
        for group in working_set:
            self.randomize(group)
