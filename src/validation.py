from pathlib import Path
from data import REQUIRED_GAME_FILES, POSSIBLE_EXE_PATHS, VERSIONS_INFO, NO_EXE_ALLOWED
from config import Config
from errors import ManifestMissingError, RootNotFoundError, ExeMissingError, VersionError, GameNotFoundError, GDPFoundError

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
            if not silent: logger.warning(f"Can't find executable in {path_to_dir}")
            # raise ExeMissingError(path_to_dir)
        else:
            if not silent: logger.info(f"Executable is determined as {exe}.")

        # validate other files and dirs
        for game_dir in REQUIRED_GAME_FILES:
            full_path = path_to_dir / game_dir
            if not full_path.exists():
                gdp_archives = self.look_for_gdp_archives(path_to_dir)
                if gdp_archives:
                    if not silent: 
                        logger.error(f"Unable to validate game path. {full_path} is missing.")
                        gdp_paths_str = ", ".join([str(gdp.resolve()) for gdp in gdp_archives])
                        logger.info(f"GDP archives found: {gdp_paths_str}")
                    raise GDPFoundError(gdp_archives)
                if not silent: logger.error(f"Unable to validate game path. {full_path} is missing.")
                raise GameNotFoundError(full_path)
        return True
    
    @staticmethod
    def look_for_gdp_archives(game_dir: Path) -> bool | list[Path]:
        data_path = game_dir / "data"
        gdps = list(data_path.glob("*.gdp"))
        if not gdps:
            return False
        return gdps

    @staticmethod
    def get_exe_name(game_dir: Path) -> Path | None:
        for exe in POSSIBLE_EXE_PATHS:
            exe_path = game_dir / exe
            if exe_path.exists(): return exe_path
        return None
    
    def steam_version(self, game_version: str, version_info: dict, exe: str) -> tuple[bool, str]:
        if not exe:
            if game_version in NO_EXE_ALLOWED:
                return (True, "no_exe")
            else:
                return (False, "no_exe")

        exe_info: dict = version_info.get("exe")

        for version in exe_info:
            detected_version = self.get_exe_version(
                exe,
                version.get("offset"),
                version.get("length")
            )

            if detected_version == version.get("version"):
                return True, "exe"
            else: 
                logger.info(f"{version.get('version')} expected, got {detected_version}")
        
        raise VersionError(game_version)

    
    def game_version(self, game_version: str, exe: str) -> tuple[bool, str, Path | str]:
        version_info = VERSIONS_INFO.get(game_version)
        if not version_info: raise VersionError(game_version)

        match game_version:
            case "steam" | "isl1053":
                valid, exe_status = self.steam_version(game_version, version_info, exe)
            case "cp114" | "cr114" | "isl12cp" | "isl12cr":
                raise VersionError(game_version)
        
        # TODO: Add different mods validation through yaml or existing files

        return valid, exe_status, Path(version_info.get("manifest"))
                

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

        if not settings.game_path: raise RootNotFoundError(False)
        path_valid = self.game_dir(Path(settings.game_path), silent=False)
        if not path_valid:
            return False
        
        logger.info("Game path validated.")
        
        exe = self.get_exe_name(settings.game_path)
        version_valid, exe_status, manifest = self.game_version(settings.game_version, exe)
        if not version_valid:
            return False
        
        match exe_status:
            case "no_exe":
                ic('no exe')
            case "exe":
                ic("exe")
            case "no_fov":
                ic('no_fov')
        
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