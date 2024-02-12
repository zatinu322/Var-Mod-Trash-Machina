from random import shuffle

from models_randomizer import ModelsRandomizer


class BarNpcRandomizer(ModelsRandomizer):
    def __init__(self, working_set: dict) -> None:
        super().__init__(working_set)

    def collect_data_from_xml(self, xml_info: dict) -> list:
        npcs_outfit = []
        for level in xml_info["maps"]:
            xml_path = self.game_path / level / xml_info["file"]
            root = self.parse_xml(xml_path)

            for tag in root.iter(xml_info["tag"]):
                if not xml_info["name"] in tag.attrib:
                    continue
                if "prototype" in xml_info:
                    if not tag.attrib.get(
                        xml_info["name"]
                    ) == xml_info["prototype"]:
                        continue

                # filter tags with no NPC
                has_npc = False
                outfit = {}

                for option in xml_info["config"]:
                    if option in tag.attrib:
                        has_npc = True
                        outfit[option] = tag.attrib[option]

                if has_npc:
                    npcs_outfit.append(outfit)

        return npcs_outfit

    def set_data_to_xml(self, xml_info: dict, content: list[dict]) -> None:
        li = 0
        for level in xml_info["maps"]:
            xml_path = self.game_path / level / xml_info["file"]
            root = self.parse_xml(xml_path)

            for tag in root.iter(xml_info["tag"]):
                if not xml_info["name"] in tag.attrib:
                    continue
                if "prototype" in xml_info:
                    if not tag.attrib.get(
                        xml_info["name"]
                    ) == xml_info["prototype"]:
                        continue

                # check if tag has npc
                has_npc = False
                for option in xml_info["config"]:
                    if option in tag.attrib:
                        has_npc = True
                        break

                if has_npc:
                    for option in xml_info["config"]:
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
        if not self.npc_look:
            self.logger.info("Nothing to randomize.")
            return
        for group in self.npc_look:
            self.randomize(group)
