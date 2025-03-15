from contextlib import contextmanager
import logging
from pathlib import Path
from typing import Any, Generator

from .validation_data import REQUIRED_GAME_PATHS, POSSIBLE_EXE_NAMES, \
    VERSIONS
from config.app_config import Config
from helpers.errors import ManifestMissingError, RootNotFoundError, \
    ExecutableVersionError, GameNotFoundError, GDPFoundError, \
    ExecutableNotFoundError, NoGamePathError, NotAbsolutePathError, \
    ResourcesMissingError, ModsNotFoundError, ModsFoundError, ModVersionError
from .manifest_schema import validate_manifest_types
from helpers.yaml_utils import serialize_yaml

logger = logging.getLogger(Path(__file__).name)


def serialize_game_path(game_path: str) -> Path:
    if not game_path:
        raise NoGamePathError()

    serialized_path = Path(game_path.strip())

    if not serialized_path.is_absolute():
        raise NotAbsolutePathError()

    return serialized_path


def validate_context(settings: Config) -> tuple[bool, dict]:
    """
    Validates randomization context.

    Returns: `fov_allowed`, `manifest_path`, `options_path`
    """
    logger.info("Validating randomization settings.")

    game_path = serialize_game_path(settings.game_path)
    version_info = VERSIONS[settings.game_version]

    exe_path = validate_game_dir(game_path, silent=False)

    logger.info("Game path validated.")

    fov_allowed, manifest_path, options_path = validate_game_version(
        version_info, exe_path
    )

    logger.info("Game version validated.")

    serialized_manifest = validate_manifest(
        manifest_path
    )

    mod_manifest = validate_game_installation(
        serialized_manifest,
        game_path,
        settings.resources_path,
        version_info
    )

    if "options" not in version_info \
            or mod_manifest is None \
            or options_path is None:
        return fov_allowed, serialized_manifest

    updated_manifest = update_manifest_with_options(
        serialized_manifest,
        mod_manifest,
        options_path
    )

    return fov_allowed, updated_manifest


def validate_game_installation(manifest: dict,
                               game_path: Path,
                               resources_path: Path,
                               version_info: dict) -> dict | None:
    files_to_validate = [
        *[resources_path / file
          for file in manifest["resources_validation"]],
        *[game_path / file for file in manifest["server_paths"]],
        *[game_path / file
          for file in manifest["triggers_to_change"]],
    ]

    for file in files_to_validate:
        if not file.exists():
            raise ResourcesMissingError(file)

    game_validation = manifest["version_validation"]
    if not game_validation:
        logger.info("Additional game validation is not specified.")
        return None

    if isinstance(game_validation, str):
        mod_manifest_path = game_path / game_validation
        if not mod_manifest_path.exists():
            raise ResourcesMissingError(mod_manifest_path)

        mod_manifest = serialize_yaml(mod_manifest_path)

        allowed_mods = version_info["allowed_mods"]
        allowed_mod_names = {mod for mod in allowed_mods}
        installed_mod_names = set(mod_manifest)

        missing_mods = allowed_mod_names.difference(installed_mod_names)
        if missing_mods:
            raise ModsNotFoundError(missing_mods)
        extra_mods = installed_mod_names.difference(allowed_mod_names)
        if extra_mods:
            raise ModsFoundError(extra_mods)

        for title, info in mod_manifest.items():
            required_version = allowed_mods[title]["version"]
            installed_version = info["version"]
            if installed_version != required_version:
                raise ModVersionError(title,
                                      installed_version,
                                      required_version)

        return mod_manifest
    else:
        raise NotImplementedError()


def update_manifest_with_options(manifest: dict,
                                 mod_manifest: dict,
                                 options_path: Path) -> dict:
    if not options_path.exists():
        raise ManifestMissingError(options_path)

    serialized_options = serialize_yaml(options_path)
    for mod, mod_info in mod_manifest.items():
        options_to_update = serialized_options.get(mod, {})
        for option in options_to_update:
            if mod_info.get(option) == "yes":
                manifest.update(
                    options_to_update[option]
                )
    return manifest


def validate_manifest(manifest_path: Path) -> dict:
    """
    Validates manifest structure.

    Returns serialized_manifest if manifest is valid.

    Raises exceptions otherwise.
    """
    logger.info("Validating manifest")

    if not manifest_path.exists():
        raise ManifestMissingError(manifest_path)

    serialized_manifest = serialize_yaml(manifest_path)

    validate_manifest_types(serialized_manifest)

    return serialized_manifest


def validate_game_version(version_info: dict,
                          exe_path: Path) -> tuple[bool, Path, Path | None]:
    """
    Validates game version.

    Returns `fov_allowed`, `manifest_path`, `option_path`
    """
    exe_info = version_info["exe"]

    exe_version = validate_exe_version(exe_path, exe_info)
    if not exe_version:
        raise ExecutableVersionError(version_info["title"])

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
    return None


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
    return None


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

                logger.info(f"GDP archives found: {gdp_archives}")

                raise GDPFoundError(gdp_archives)

        return exe_path


@contextmanager
def change_logging_level(silent: bool) -> Generator[Any, None, None]:
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
    return None


def look_for_gdp_archives(game_dir: Path) -> list[Path]:
    """
    Returns list with all `.gdp` files paths.
    """
    data_dir = game_dir / "data"
    gdps = list(data_dir.glob("*.gdp"))
    return gdps
