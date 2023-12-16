from pathlib import Path

import logging

logger = logging.getLogger("pavlik")

class Validation():
    def __init__(self) -> None:
        pass

    @staticmethod
    def path(path_to_file: Path, *paths):
        if not isinstance(path_to_file, Path): path_to_file
        
        for path in paths:
            path_to_file = Path(path_to_file) / path
        
        return path_to_file.exists()
    
    def game_dir(self, path_to_dir: Path) -> bool:
        pass

    
    def path_list(self, paths_list: list[str] | str):
        if isinstance(paths_list, str): paths_list = [paths_list]

        for file_path in paths_list:
            if not self.path(file_path):
                logger.error(f"File not found: {file_path}")
                return (False, file_path)
        return (True, "")
    
    def generate_path_list(self, main_path: str, add_paths: list[str]):
        """
        Generates list of paths from one main path and additional paths to it.
        """
        paths = []

        for path in add_paths:
            paths.append(Path(main_path) / Path(path))        
        return paths

    def executable(self):
        pass

    def determine_exe_name(self):
        pass