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
    def __init__(self, path: Path) -> None:
        self.path = path
    
    def __str__(self) -> str:
        return str(self.path.resolve())
    
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

class VersionError(Exception):
    def __init__(self, version: str) -> None:
        self.version = version
    
    def __str__(self) -> str:
        return self.version