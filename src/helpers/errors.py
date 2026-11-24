from pathlib import Path


class NoGamePathError(Exception):
    def __init__(self) -> None:
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


class ExecutableVersionError(Exception):
    def __init__(self, version: str) -> None:
        self.version = version
        self.ui_message_key = "incorrect_version_exe"
        self.ui_message_text = ""

    def __str__(self) -> str:
        return " ".join([
            "Executable version does not match given version:",
            f"{self.version}"
        ])


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
        self.ui_message_key = "file_missing"
        self.ui_message_text = str(path.resolve())

    def __str__(self) -> str:
        return f"Required file missing: {self.path.resolve()}"


class ModsNotFoundError(Exception):
    def __init__(self, mod_names: set) -> None:
        self.ui_message_key = "mod_not_found"
        self.ui_message_text = ", ".join(mod_names)

    def __str__(self) -> str:
        return f"Required modifications not found: {self.ui_message_text}"


class ModsFoundError(Exception):
    def __init__(self, mod_names: set) -> None:
        self.ui_message_key = "mods_found"
        self.ui_message_text = ", ".join(mod_names)

    def __str__(self) -> str:
        return f"Found incompatible modifications: {self.ui_message_text}"


class ModVersionError(Exception):
    def __init__(self, mod: str,
                 installed_version: str,
                 required_version: str) -> None:
        self.version = installed_version
        self.ui_message_key = "incorrect_version_mod"
        self.ui_message_text = (f"{mod} - {self.version} "
                                f"(required {required_version})")

    def __str__(self) -> str:
        return " ".join([
            "Incorrect modification version detected:",
            self.ui_message_text
        ])


class ManifestKeyError(Exception):
    def __init__(self, key_name: str, key_type: type) -> None:
        self.key_type = key_type
        self.key_name = key_name

    def __str__(self) -> str:
        return f"{self.key_name}: {str(self.key_type)}"


class LocalisationMissingError(Exception):
    def __init__(self, path: Path, lang: str) -> None:
        self.path = path
        self.lang = lang

    def __str__(self) -> str:
        return " ".join([
            f"Unable to load {self.lang} localisation",
            f"from {self.path.resolve()}"
        ])


class ElementNotFoundError(Exception):
    def __init__(self, element: str, file_path: Path) -> None:
        self.element = element
        self.file_path = file_path
        self.ui_message_key = ""
        self.ui_message_text = ""

    def __str__(self) -> str:
        return " ".join([
            f"Required element \"{self.element}\"",
            f"not found in {self.file_path.resolve()}.",
            "Probably wrong or corrupted file."
        ])
