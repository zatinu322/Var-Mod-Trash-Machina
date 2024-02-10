from logging import Logger
from pathlib import Path


class WorkingSetManager():
    def __init__(self, working_set: dict) -> None:
        self.logger: Logger = working_set["logger"]
        self.game_path: Path = Path(working_set["game_path"])
        self.folder_to_copy: Path = Path(working_set["folder_to_copy"])
        self.lua_to_edit: Path = Path(working_set["lua_to_edit"])
        self.server_paths: list[str] = working_set["server_paths"]
        self.server_items: list[str] = working_set["server_items"]
        self.triggers_to_change: dict = working_set["triggers_to_change"]
        self.files: list = working_set["files"]
        self.text: list = working_set["text"]
        self.models: list = working_set["models"]
        self.npc_look: list = working_set["npc_look"]
        self.landscape: list = working_set["landscape"]
        self.exe: list = working_set["exe"]
        self.lua: list = working_set["lua"]
