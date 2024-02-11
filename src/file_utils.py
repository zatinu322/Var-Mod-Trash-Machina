import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

from working_set_manager import WorkingSetManager


class FileCopier(WorkingSetManager):
    def __init__(self, working_set: dict) -> None:
        super().__init__(working_set)

    def copy_files(self) -> None:
        dir_path = self.folder_to_copy
        game_dir_path = self.game_path / "data"

        self.logger.debug(f"FileCopier: copy {dir_path} to {game_dir_path}.")

        shutil.copytree(dir_path, game_dir_path, dirs_exist_ok=True)


class FileEditor(WorkingSetManager):
    def __init__(self, working_set: dict) -> None:
        super().__init__(working_set)

    def edit_lua(self, lua_path: str):
        lua_game_path = self.game_path / lua_path
        line_to_add = 'EXECUTE_SCRIPT "data/scripts/randomizer_vars.lua"\n'

        with open(lua_game_path, "a+", encoding="windows-1251") as lua:
            lua.seek(0)
            file = lua.read()

            if line_to_add not in file:
                lua.write("\n")
                lua.write(line_to_add)

    def edit_xml_servers(self, file_path: Path, items_list: list):
        tree = ET.parse(file_path)
        root = tree.getroot()

        models_server = root.find("AnimatedModelsServer")
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
                script.text = trigger_text

        tree.write(file_path, encoding="windows-1251")

    def edit_files(self):
        self.edit_lua(self.lua_to_edit)

        for path, trigger_data in self.triggers_to_change.items():
            self.edit_xml_triggers(
                self.game_path / path,
                trigger_data["name"],
                trigger_data["script"]
            )

        for server_path in self.server_paths:
            self.edit_xml_servers(
                self.game_path / server_path,
                self.server_items
            )
