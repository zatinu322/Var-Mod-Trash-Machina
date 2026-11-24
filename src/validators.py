from pathlib import Path

from exceptions import ExecutableNotFoundError, GameNotFoundError, GDPFoundError, RootNotFoundError

POSSIBLE_EXE_NAMES = [
    "hta.exe",
    "game.exe",
    "start.exe",
    "ExMachina.exe",
]

REQUIRED_GAME_PATHS = [
    "data",
    "data/gamedata",
    "data/if",
    "data/maps",
    "data/models",
    "data/music",
    "data/scripts",
    "data/sounds",
    "data/textures",
    "data/tiles",
    "data/weathertexs",
    "data/weather.xml",
]


def validate_file_path(file_path: Path) -> Path:
    if not file_path.exists():
        raise ValueError(f"File does not exists: {file_path}.")
    if not file_path.is_file():
        raise ValueError(f"{file_path} is not file")
    return file_path


def validate_game_directory(game_path: Path) -> Path:
    """Validate installed game in given directory.

    Raise:
        `RootNotFoundError` when game directory is missing.
        `ExecutableNotFoundError` when game executable is not found.
        `GameNotFoundError` when required game files are missing.
        `GDPFoundError` when game contains GDP-archives.

    Return:
        Path to game executable.
    """
    if not game_path.exists():
        raise RootNotFoundError(f"Path not found: {game_path.resolve()}.")

    for required_path in REQUIRED_GAME_PATHS:
        full_path = game_path / required_path
        if not full_path.exists():
            gdp_archives = _locate_gdp_archives(game_path)
            if gdp_archives:
                raise GDPFoundError(f"GDP archives found: {", ".join(gdp_archives)}")
            raise GameNotFoundError(f"Required game resources not found at {game_path.resolve()}.")

    executable_path = _get_executable_path(game_path)
    if not executable_path:
        raise ExecutableNotFoundError(f"Game executable not found at {game_path.resolve()}.")

    return executable_path


def _get_executable_path(game_path: Path) -> Path | None:
    for executable in POSSIBLE_EXE_NAMES:
        executable_path = game_path / executable
        if executable_path.exists():
            return executable_path
    return None


def _locate_gdp_archives(game_path: Path) -> list[str]:
    data_path = game_path / "data"
    return [str(path) for path in data_path.glob("*.gdp")]
