from pathlib import Path


class ManifestMissingError(Exception):
    def __init__(self, path: Path) -> None:
        self.path = path

    def __str__(self) -> str:
        return str(self.path.resolve())


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


class RootNotFoundError(Exception):
    def __init__(self, path: Path | bool) -> None:
        if not path:
            self.message = ""
        else:
            self.message = str(path.resolve())

    def __str__(self) -> str:
        return self.message


class GameNotFoundError(Exception):
    def __init__(self, path: Path) -> None:
        self.path = path

    def __str__(self) -> str:
        return str(self.path.resolve())


class GDPFoundError(Exception):
    def __init__(self, archives: list[Path]) -> None:
        self.archives = [str(gdp.resolve()) for gdp in archives]
        self.message = ",\n".join(self.archives)

    def __str__(self) -> str:
        return self.message


class VersionError(Exception):
    def __init__(self, version: str) -> None:
        self.version = version

    def __str__(self) -> str:
        return self.version


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
