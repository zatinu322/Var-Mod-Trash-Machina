from pathlib import Path


class NoGamePathError(Exception):
    def __init__(self, path: Path | None = None) -> None:
        self.path = path
        self.ui_message_key = "no_game_path"
        self.ui_message_text = ""

    def __str__(self) -> str:
        return ("Game path is empty.")


class NotAbsolutePathError(Exception):
    def __init__(self, path: Path | None = None) -> None:
        self.path = path
        self.ui_message_key = "not_absolute_path"
        self.ui_message_text = ""

    def __str__(self) -> str:
        return ("Game path is not absolute.")


class RootNotFoundError(Exception):
    def __init__(self, path: Path | None = None) -> None:
        self.path = path
        self.ui_message_key = "game_path_missing"
        self.ui_message_text = str(path.resolve())

    def __str__(self) -> str:
        return ("Unable to validate game_path. "
                f"{self.path.resolve()} does not exists.")


class ExecutableNotFoundError(Exception):
    def __init__(self, path: Path) -> None:
        self.path = path
        self.ui_message_key = "exe_not_found"
        self.ui_message_text = str(path.resolve())

    def __str__(self) -> str:
        return (f"Executable not found in {self.path.resolve()}")


class GameNotFoundError(Exception):
    def __init__(self, path: Path) -> None:
        self.path = path
        self.ui_message_key = "not_game_dir"
        self.ui_message_text = str(path.resolve())

    def __str__(self) -> str:
        return ("Unable to validate game path. "
                f"{self.path.resolve()} is missing.")


class GDPFoundError(Exception):
    def __init__(self, archives: list[Path]) -> None:
        archives = [gdp.resolve() for gdp in archives]
        self.ui_message_key = "gdp_found"
        self.ui_message_text = "\n".join(archives)

    def __str__(self) -> str:
        return ("Unable to validate game path. "
                f"GDP archives found: {self.ui_message_text}")


class VersionError(Exception):
    def __init__(self, version: str) -> None:
        self.version = version
        self.ui_message_key = "incorrect_version"
        self.ui_message_text = ""

    def __str__(self) -> str:
        return ("Executable version does not match given version: "
                f"{self.version}")


class ManifestMissingError(Exception):
    def __init__(self, path: Path) -> None:
        self.path = path
        self.ui_message_key = "manifest_missing"
        self.ui_message_text = str(path.resolve())

    def __str__(self) -> str:
        return f"Manifest not found: {self.path.resolve()}"


class ResourcesMissingError(Exception):
    def __init__(self, path: Path) -> None:
        self.path = path

    def __str__(self) -> str:
        return str(self.path.resolve())


class ManifestKeyError(Exception):
    def __init__(self, key_name: str, key_type: type) -> None:
        self.key_type = key_type
        self.key_name = key_name

    def __str__(self) -> str:
        return f"{self.key_name}: {str(self.key_type)}"


class LocalisationMissingError(Exception):
    def __init__(self, path: str, lang: str) -> None:
        self.path = path
        self.lang = lang

    def __str__(self) -> str:
        return f"Unable to load {self.lang} localisation from {self.path}"


class ModsFoundError(Exception):
    def __init__(self, mods: list) -> None:
        self.mods = mods

    def __str__(self) -> str:
        return str(self.mods)


class ModNotFoundError(Exception):
    def __init__(self, mod_name: str) -> None:
        self.mod_name = mod_name

    def __str__(self) -> str:
        return self.mod_name
