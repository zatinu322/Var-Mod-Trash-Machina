import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
import logging

from config.randomization_config import RandomizationParams
from helpers.errors import ElementNotFoundError

logger = logging.getLogger(Path(__file__).name)


class FileCopier:
    def __init__(self, params: RandomizationParams) -> None:
        self.params = params

    def copy_files(self) -> None:
        (self.params.game_path / "data" / "profiles" / "1")\
            .mkdir(exist_ok=True, parents=True)

        logger.debug("Created directory for profile \"1\"")

        for file in self.params.resources:
            file_path = self.params.resources_path / file
            file_game_path = self.params.game_path / file

            logger.debug(
                f"Copy {file_path} to {file_game_path}."
            )
            shutil.copy(file_path, file_game_path)


class FileEditor:
    def __init__(self, params: RandomizationParams) -> None:
        self.params = params

    def edit_lua(self, lua_path: Path) -> None:
        lua_game_path = self.params.game_path / lua_path
        line_to_add = 'EXECUTE_SCRIPT "data/scripts/randomizer_vars.lua"\n'

        with open(lua_game_path, "a+", encoding="windows-1251") as lua:
            lua.seek(0)
            file = lua.read()

            if line_to_add not in file:
                lua.write("\n")
                lua.write(line_to_add)

    def edit_xml_servers(self, file_path: Path, items_list: list) -> None:
        tree = ET.parse(file_path)
        root = tree.getroot()

        models_server = root.find("AnimatedModelsServer")
        if models_server is None:
            raise ElementNotFoundError("AnimatedModelsServer", file_path)
        existing_tags = {tag.attrib["id"] for tag in models_server}

        for item in items_list:
            if isinstance(item, str):
                if item in existing_tags:
                    continue
                else:
                    new_item = ET.SubElement(models_server, "Item")
                    new_item.attrib.update({
                        "id": item,
                        "file": "data\\models\\AnimModels.xml"
                    })
            elif isinstance(item, dict):
                for name, params in item.items():
                    if name in existing_tags:
                        continue
                    else:
                        new_item = ET.SubElement(models_server, "Item")
                        new_item.attrib.update({
                            "id": name,
                            "file": "data\\models\\AnimModels.xml",
                            "params": params
                        })

        tree.write(file_path, encoding="windows-1251")

    def edit_xml_triggers(
        self,
        file_path: Path,
        trigger_name: str,
        trigger_text: str
    ) -> None:
        # fix text formatting
        trigger_text = trigger_text.replace("\\n", "\n")
        trigger_text = trigger_text.replace("\\t", "\t")

        tree = ET.parse(file_path)
        root = tree.getroot()

        for tag in root.iter("trigger"):
            if tag.attrib.get("Name") == trigger_name:
                script = tag.find("script")
                if script is None:
                    raise ElementNotFoundError("Trigger.script", file_path)
                script.text = trigger_text

        tree.write(file_path, encoding="windows-1251")

    def edit_files(self) -> None:
        self.edit_lua(self.params.lua_to_edit)

        for path, trigger_data in self.params.triggers_to_change.items():
            self.edit_xml_triggers(
                self.params.game_path / path,
                trigger_data["name"],
                trigger_data["script"]
            )

        for server_path in self.params.server_paths:
            self.edit_xml_servers(
                self.params.game_path / server_path,
                self.params.server_items
            )
