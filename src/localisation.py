from yaml_operations import YamlConfig
from errors import LocalisationMissingError

class Localisation(YamlConfig):
    def __init__(self, path_to_file) -> None:
        super().__init__(path_to_file)

        self.lang = "eng"

        if self.yaml:
            self.cur_locale: dict = self.yaml.get(self.lang, {})
            if not self.cur_locale:
                raise LocalisationMissingError(self.path, self.lang)
        else:
            raise LocalisationMissingError(self.path, self.lang)
    
    def update_lang(self, lang: str):
        self.lang = lang
        self.cur_locale = self.yaml.get(self.lang)

    def tr(self, k: str) -> str:
        return self.cur_locale.get(k, "null")