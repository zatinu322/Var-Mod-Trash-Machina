from randomizer import Randomizer
from pathlib import Path

import shutil

class FileCopier(Randomizer):
    def __init__(self, main_app) -> None:
        super().__init__(main_app)
    
    def copy_files(self, dir: Path) -> None:
        dir_path = dir / "data"
        game_dir_path = Path(self.config.game_path) / "data"
    
        shutil.copytree(dir_path, game_dir_path, dirs_exist_ok = True)
    
    def edit_lua(self, lua_path: str):
        lua_game_path = Path(self.config.game_path) / lua_path
        line_to_add = 'EXECUTE_SCRIPT "data/scripts/randomizer_vars.lua"\n'

        with open(lua_game_path, "a+", encoding="windows-1251") as lua:
            lua.seek(0)
            file = lua.read()

            if not line_to_add in file:
                lua.write("\n")
                lua.write(line_to_add)
        
    def transfer_files(self):
        dir_path = Path(self.manifest.get("FolderToCopy"))
        lua_path = Path(self.manifest.get("LuaToEdit"))

        self.copy_files(dir_path)
        self.edit_lua(lua_path)