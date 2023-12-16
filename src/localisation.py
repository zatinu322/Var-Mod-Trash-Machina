import logging

from yaml_operations import YamlConfig
from errors import LocalisationMissingError

logger = logging.getLogger("pavlik")

class Localisation(YamlConfig):
    def __init__(self, path_to_file) -> None:
        super().__init__(path_to_file)

        if not self.yaml or not isinstance(self.yaml, dict):
            raise LocalisationMissingError(self.path, "any")

        self.lang = "eng"

        self.cur_locale: dict = self.yaml.get(self.lang, {})
        if not self.cur_locale:
            logger.error(f"\"{self.lang}\" key is missing in {self.path}.")
            raise LocalisationMissingError(self.path, self.lang)
    
    def update_lang(self, lang: str):
        self.lang = lang
        self.cur_locale = self.yaml.get(self.lang, {})
        if not self.cur_locale:
            logger.error(f"\"{self.lang}\" key is missing in {self.path}.")

    def tr(self, k: str) -> str:
        return self.cur_locale.get(k, "null")