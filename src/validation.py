from contextlib import contextmanager
import logging
from pathlib import Path

from validation_data import REQUIRED_GAME_PATHS, POSSIBLE_EXE_NAMES, \
    VERSIONS
from config import Config
from errors import ManifestMissingError, RootNotFoundError, VersionError, \
    GameNotFoundError, GDPFoundError, ExecutableNotFoundError, \
    NoGamePathError, NotAbsolutePathError

logger = logging.getLogger("validation")


def serialize_game_path(game_path: str) -> Path:
    if not game_path:
        raise NoGamePathError(game_path)

    serialized_path = Path(game_path.strip())

    if not serialized_path.is_absolute():
        raise NotAbsolutePathError()

    return serialized_path


def validate_context(settings: Config) -> tuple[bool, Path]:
    """
    Validates randomization context.

    Returns: `fov_allowed`, `manifest_path`, `options_path`
    """
    logger.info("Validating randomization settings.")

    game_path = serialize_game_path(settings.game_path)

    exe_path = validate_game_dir(game_path, silent=False)

    logger.info("Game path validated.")

    fov_allowed, manifest_path, options_path = validate_game_version(
        settings.game_version, exe_path
    )

    logger.info("Game version validated.")

    validate_manifest(manifest_path)

    if options_path:
        validate_manifest(options_path)

    return fov_allowed, manifest_path, options_path


def validate_manifest(manifest_path: Path) -> None:
    """
    Validates manifest path.

    Raises `ManifestMissingError` if it doesn't exists.
    """
    if not manifest_path.exists():
        raise ManifestMissingError(manifest_path)


def validate_game_version(game_version: str,
                          exe_path: Path) -> tuple[bool, Path | None]:
    """
    Validates game version.

    Returns `fov_allowed`, `manifest_path`, 'option_path'
    """
    version_info = VERSIONS[game_version]
    exe_info = version_info["exe"]

    exe_version = validate_exe_version(exe_path, exe_info)
    if not exe_version:
        raise VersionError(game_version)

    fov_allowed = version_info["fov_allowed"]
    manifest_path = Path(version_info["manifest"])
    options = version_info.get("options")
    options_path = Path(options) if options else None

    return fov_allowed, manifest_path, options_path


def validate_exe_version(exe_path: Path, exe_info: dict) -> str | None:
    """
    Validates executable version.

    Returns detection version if version is correct, `None` otherwise.
    """
    for version in exe_info:
        detected_version = get_exe_version(
            exe_path,
            version["offset"],
            version["length"]
        )

        if detected_version == version["version"]:
            return detected_version


def get_exe_version(
        exe_path: Path,
        offset: int,
        length: int) -> str | None:
    """
    Detects executable version based on version data.

    Returns detected version.
    """
    try:
        with open(exe_path, 'r', encoding='windows-1251') as stream:
            stream.seek(offset)
            version = stream.read(length)
        return version
    except PermissionError as e:
        logger.error(e)


def validate_game_dir(dir_path: Path, silent: bool = True) -> Path:
    """
    Validates that game is installed in given directory.

    May raise `RootNotFoundError`, `GameNotFoundError`,
    `GDPFoundError` if it doesn't.

    Returns path to executable file, if one was found. `None` otherwise.
    """
    with change_logging_level(silent):
        # validate main dir
        if not dir_path or not dir_path.exists():
            raise RootNotFoundError(dir_path)

        # locate executable
        exe_path = get_exe_name(dir_path)
        if not exe_path:
            logger.error(f"Can't find executable in {dir_path}")
            raise ExecutableNotFoundError(dir_path)

        logger.info(f"Executable found: {exe_path}")

        # validate other files and dirs
        for game_dir in REQUIRED_GAME_PATHS:
            full_path = dir_path / game_dir
            if not full_path.exists():
                gdp_archives = look_for_gdp_archives(dir_path)
                if not gdp_archives:
                    raise GameNotFoundError(full_path)
                gdp_paths = ", ".join(
                    [str(gdp.resolve()) for gdp in gdp_archives]
                )

                logger.info(f"GDP archives found: {gdp_paths}")

                raise GDPFoundError

        return exe_path


@contextmanager
def change_logging_level(silent: bool):
    """
    Completely disables logging if silent is True.
    """
    previous_level = logger.getEffectiveLevel()
    if silent:
        logger.setLevel(logging.CRITICAL)
    try:
        yield
    finally:
        logger.setLevel(previous_level)


def get_exe_name(game_dir: Path) -> Path | None:
    """
    Detects executable and returns it's path if it matches one of known names.

    Returns `None` otherwise.
    """
    for exe in POSSIBLE_EXE_NAMES:
        exe_path = game_dir / exe
        if exe_path.exists():
            return exe_path


def look_for_gdp_archives(game_dir: Path) -> list[Path]:
    """
    Returns list with all `.gdp` files paths.
    """
    data_dir = game_dir / "data"
    gdps = list(data_dir.glob("*.gdp"))
    return gdps
