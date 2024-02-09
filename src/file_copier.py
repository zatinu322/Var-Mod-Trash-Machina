from randomizer import Randomizer
from pathlib import Path
from config import Config

import shutil


class FileCopier(Randomizer):
    def __init__(self, config: Config, need_validation: bool = False) -> None:
        super().__init__(config, need_validation)

    def copy_files(self, dir: Path) -> None:
        dir_path = dir / "data"
        game_dir_path = Path(self.game_path) / "data"

        self.logger.debug(f"FileCopier: copy {dir_path} to {game_dir_path}.")
        shutil.copytree(dir_path, game_dir_path, dirs_exist_ok=True)

    def edit_lua(self, lua_path: str):
        lua_game_path = Path(self.game_path) / lua_path
        line_to_add = 'EXECUTE_SCRIPT "data/scripts/randomizer_vars.lua"\n'

        with open(lua_game_path, "a+", encoding="windows-1251") as lua:
            lua.seek(0)
            file = lua.read()

            if line_to_add not in file:
                lua.write("\n")
                lua.write(line_to_add)

    def edit_xml_servers(self):
        pass

    def edit_xml_triggers(self):
        pass

    def transfer_files(self):
        dir_path = Path(self.manifest.get("FolderToCopy"))
        lua_path = Path(self.manifest.get("LuaToEdit"))

        self.copy_files(dir_path)
        self.edit_lua(lua_path)
