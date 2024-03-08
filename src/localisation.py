import logging

from yaml_parser import YamlConfig
from errors import LocalisationMissingError

logger = logging.getLogger("localisation")


class Localisation(YamlConfig):
    def __init__(self, path_to_file, lang="eng") -> None:
        super().__init__(path_to_file)

        if not self.yaml or not isinstance(self.yaml, dict):
            raise LocalisationMissingError(self.path, "any")

        self.lang = lang

        self.cur_locale: dict = self.yaml.get(self.lang, {})
        if not self.cur_locale:
            logger.error(f"\"{self.lang}\" key is missing in {self.path}.")
            raise LocalisationMissingError(self.path, self.lang)

    def update_lang(self, lang: str) -> None:
        self.lang = lang
        self.cur_locale = self.yaml.get(self.lang, {})
        if not self.cur_locale:
            logger.error(
                f"\"{self.lang}\" language info is missing in {self.path}."
            )

    def tr(self, message: str) -> str:
        if message in self.cur_locale:
            return self.cur_locale.get(message)
        else:
            logger.error(f"{message} key is missing for {self.lang} language.")
            return message
