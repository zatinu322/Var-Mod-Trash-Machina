from pathlib import Path

class ManifestMissingError(Exception):
    def __init__(self, path: Path) -> None:
        self.path = path
    
    def __str__(self) -> str:
        return str(self.path.resolve())

class LocalisationMissingError(Exception):
    def __init__(self, path: str, lang: str) -> None:
        self.path = path
        self.lang = lang
    
    def __str__(self) -> str:
        return f"Unable to load {self.lang} localisation from {self.path}"

class RootNotFoundError(Exception):
    def __init__(self, path: Path | bool) -> None:
        if not path: self.message = ""
        else: self.message = str(path.resolve())
    
    def __str__(self) -> str:
        return self.message
    
class ExeMissingError(Exception):
    def __init__(self, path: Path) -> None:
        self.path = path
    
    def __str__(self) -> str:
        return str(self.path.resolve())

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