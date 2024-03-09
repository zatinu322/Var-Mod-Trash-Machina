import logging
from pathlib import Path

from validation_data import REQUIRED_GAME_FILES, POSSIBLE_EXE_NAMES, \
    VERSIONS_INFO, NO_EXE_ALLOWED
from config import Config
from errors import ManifestMissingError, RootNotFoundError, VersionError, \
    GameNotFoundError, GDPFoundError

from icecream import ic


logger = logging.getLogger("validation")

def validate_settings(
        game_path: str,
        game_version: str
) -> dict | None:
    if not validate_path(game_path):
        raise RootNotFoundError(game_path)
    
    if not validate_game_dir(Path(game_path)):
        pass


def validate_path(path: str) -> bool:
    if not path or not Path(path).absolute().exists():
        return False
    return True


def validate_game_dir(game_path: Path, log: bool = True):
    # TODO: disable logger if logging is False
    if not validate_game_files(game_path, REQUIRED_GAME_FILES):
        pass
    exe_path = get_exe_path(game_path, POSSIBLE_EXE_NAMES)


def look_for_gdp_archives(game_path: Path) -> None:
    data_path = game_path / "data"
    gdps = data_path.glob("*.gdp")
    if next(gdps, None) is not None:
        return gdps


def get_exe_path(game_path: Path, exe_names: list[str]) -> Path | None:
    for name in exe_names:
        exe_path = game_path / name
        if exe_path.exists():
            return exe_path


def validate_game_files(game_path: Path, required_paths: list[Path]) -> bool:
    for path in required_paths:
        full_path = game_path / path
        if not full_path.exists():
            logger.error(f"{full_path.absolute()} not found.")
            return False
        return True


if __name__ == "__main__":
    # ic(validate_path(""))
    # ic(validate_path("src/"))
    # ic(validate_path("src/biba.txt"))
    # ic(get_exe_path(Path(r"C:\Users\User\Desktop\Ex Machina"), POSSIBLE_EXE_NAMES))
    # ic(validate_game_files(Path(r"C:\Users\User\Desktop\Ex Machina"), REQUIRED_GAME_FILES))
    # ic(validate_game_files(Path(r"C:\Users\User\Desktop"), REQUIRED_GAME_FILES))
    gener = Path().glob("scr/*")
    ic(next(gener, None))