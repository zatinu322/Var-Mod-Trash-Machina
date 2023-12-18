from pathlib import Path
from data import REQUIRED_GAME_FILES, POSSIBLE_EXE_PATHS, VERSIONS_INFO
from config import Config
from errors import ManifestMissingError, RootNotFoundError, ExeMissingError, VersionError, GameNotFoundError

import logging
from icecream import ic

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
    
    def game_dir(self, path_to_dir: Path, silent: bool = True) -> tuple[bool, str]:
        # validate main dir
        if not path_to_dir.exists():
            if not silent: logger.error(f"Unable to validate game path. {path_to_dir} does not exists.")
            raise RootNotFoundError(path_to_dir)
        
        # validate exe
        exe = self.get_exe_name(path_to_dir)
        if not exe:
            if not silent: logger.error(f"Unable to validate game path. Executable is missing.")
            raise ExeMissingError(path_to_dir)
        else:
            if not silent: logger.info(f"Executable is determined as {exe}.")

        # validate other files and dirs
        for game_dir in REQUIRED_GAME_FILES:
            full_path = path_to_dir / game_dir
            if not full_path.exists():
                if self.look_for_gdp_archives(path_to_dir):
                    if not silent: 
                        logger.error(f"Unable to validate game path. {full_path} is missing.")
                        logger.info(f"GDP archives found in {path_to_dir / 'data'}.")
                    return False, "gdp"
                if not silent: logger.error(f"Unable to validate game path. {full_path} is missing.")
                raise GameNotFoundError(full_path)
        return True, ""
    
    @staticmethod
    def look_for_gdp_archives(game_dir: Path) -> bool:
        data_path = game_dir / "data"
        if list(data_path.glob("*.gdp")):
            return True
        return False

    @staticmethod
    def get_exe_name(game_dir: Path) -> Path | None:
        for exe in POSSIBLE_EXE_PATHS:
            exe_path = game_dir / exe
            if exe_path.exists(): return exe_path
        return None
    
    def game_version(self, game_version: str, exe: str) -> tuple[bool, Path | str]:
        version_info = VERSIONS_INFO.get(game_version)
        exe_info: dict = version_info.get("exe")
        for version in exe_info:
            detected_version = self.get_exe_version(
                exe,
                version.get("offset"),
                version.get("length")
            )
            
            if not detected_version == version.get("version"):
                logger.error(f"Unable to validate game version. \"{version.get('version')}\" expected, got \"{detected_version}\"")
                raise VersionError(game_version)
            
            # TODO: Add different mods validation through yaml or existing files

            return True, Path(version_info.get("manifest"))
                

    @staticmethod
    def get_exe_version(exe_path: Path, offset: int, length: int) -> str | None:
        try:
            with open(exe_path) as exe:
                exe.seek(offset)
                version = exe.read(length)
            return version
        except PermissionError as exc:
            logger.error(exc)
    
    def settings(self, settings: Config):
        logger.info("Validating randomization settings.")

        path_valid, _ = self.game_dir(Path(settings.game_path), silent=False)
        if not path_valid:
            return False
        
        logger.info("Game path validated.")
        
        exe = self.get_exe_name(settings.game_path)
        version_valid, manifest = self.game_version(settings.game_version, exe)
        if not version_valid:
            return False
        
        logger.info("Game version validated.")

        if manifest.exists():
            settings.manifest = manifest
            logger.info(f"Manifest is set as {settings.manifest}")
        else:
            logger.error(f"Manifest not found in {manifest}")
            raise ManifestMissingError(manifest)

        logger.info("Randomization settings validated.")
        
        return True

    
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