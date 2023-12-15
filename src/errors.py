class ResourcesMissingError(Exception):
    def __init__(self, path: str, message: str = "File not found") -> None:
        self.path = path
        self.message = message
    
    def __str__(self) -> str:
        return f"{self.message}: '{self.path}'"

class ManifestMissingError(Exception):
    def __init__(self, path: str = None) -> None:
        self.path = path
    
    def __str__(self) -> str:
        return self.path

class LocalisationMissingError(Exception):
    def __init__(self, path: str, lang: str) -> None:
        self.path = path
        self.lang = lang
    
    def __str__(self):
        return f"Unable to load {self.lang} localisation from {self.path}"