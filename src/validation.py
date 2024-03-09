import logging
from pathlib import Path

from validation_data import REQUIRED_GAME_FILES, POSSIBLE_EXE_NAMES, \
    VERSIONS_INFO, NO_EXE_ALLOWED
from config import Config
from errors import ManifestMissingError, RootNotFoundError, VersionError, \
    GameNotFoundError, GDPFoundError


logger = logging.getLogger("validation")


class Validation():
    def __init__(self) -> None:
        pass

    def game_dir(
        self,
        path_to_dir: Path,
        silent: bool = True
    ) -> tuple[bool, None | Path]:
        if silent:
            logger.setLevel(logging.CRITICAL)
        else:
            logger.setLevel(logging.INFO)

        # validate main dir
        if not path_to_dir.exists():
            raise RootNotFoundError(path_to_dir)

        # validate exe
        exe = self.get_exe_name(path_to_dir)
        if not exe:
            logger.warning(f"Can't find executable in {path_to_dir}")
        else:
            logger.info(f"Executable is determined as {exe}.")

        # validate other files and dirs
        for game_dir in REQUIRED_GAME_FILES:
            full_path = path_to_dir / game_dir
            if full_path.exists():
                return True, exe

            gdp_archives = self.look_for_gdp_archives(path_to_dir)
            if gdp_archives:
                gdp_paths_str = ", ".join(
                    [str(gdp.resolve()) for gdp in gdp_archives]
                )
                logger.info(f"GDP archives found: {gdp_paths_str}")

                raise GDPFoundError(gdp_archives)

            raise GameNotFoundError(full_path)

    @staticmethod
    def look_for_gdp_archives(game_dir: Path) -> bool | list[Path]:
        data_path = game_dir / "data"
        gdps = list(data_path.glob("*.gdp"))
        if not gdps:
            return False
        return gdps

    @staticmethod
    def get_exe_name(game_dir: Path) -> Path | None:
        for exe in POSSIBLE_EXE_NAMES:
            exe_path = game_dir / exe
            if exe_path.exists():
                return exe_path
        return None

    def steam_version(
        self,
        game_version: str,
        version_info: dict,
        exe: Path
    ) -> tuple[bool, str]:
        if not exe:
            if game_version in NO_EXE_ALLOWED:
                return (True, "no_exe")
            else:
                return (False, "no_exe")

        exe_info: dict = version_info["exe"]

        for version in exe_info:
            detected_version = self.get_exe_version(
                exe,
                version["offset"],
                version["length"]
            )

            if detected_version == version["version"]:
                return True, "exe"
            else:
                logger.error(
                    f"{version['version']} expected, \
                    got {detected_version}"
                )

        raise VersionError(game_version)

    def game_version(
        self,
        game_version: str,
        exe: str
    ) -> tuple[bool, str, Path | str]:
        version_info = VERSIONS_INFO[game_version]
        if not version_info:
            raise VersionError(game_version)

        valid, exe_status = self.steam_version(
            game_version, version_info, exe
        )

        match game_version:
            case "steam" | "isl1053":
                options = None
            case "cp114" | "isl12cp":
                options = None
                exe_status = "no_fov"
            case "cr114" | "isl12cr":
                options = Path(version_info["options"])
                exe_status = "no_fov"

        return (
            valid,
            exe_status,
            Path(version_info["manifest"]),
            options
        )

    @staticmethod
    def get_exe_version(
        exe_path: Path,
        offset: int,
        length: int
    ) -> str | None:
        try:
            with open(exe_path, "r", encoding="windows-1251") as exe:
                exe.seek(offset)
                version = exe.read(length)
            return version
        except PermissionError as exc:
            logger.error(exc)

    def settings(self, settings: Config) -> tuple[bool, str] | bool:
        logger.info("Validating randomization settings.")

        if not settings.game_path:
            raise RootNotFoundError(False)
        path_valid, exe = self.game_dir(Path(settings.game_path), silent=False)
        if not path_valid:
            return False

        logger.info("Game path validated.")

        version_valid, exe_status, manifest, options = self.game_version(
            settings.game_version, exe
        )
        if not version_valid:
            return False

        logger.info("Game version validated.")

        if manifest.exists():
            settings.manifest = manifest
            logger.info(f"Manifest is set as {settings.manifest}")
        else:
            logger.error(f"Manifest not found in {manifest}")
            raise ManifestMissingError(manifest)

        if options:
            if options.exists():
                settings.options = options
                logger.info(f"Options is set as {settings.options}")
            else:
                logger.error(f"Options not found in {options}")
                raise ManifestMissingError(options)

        logger.info("Randomization settings validated.")

        return True, exe_status
