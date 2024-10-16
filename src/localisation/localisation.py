from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(Path(__file__).name)


@dataclass
class Localisation:
    locales: dict
    language: str = "eng"
    current_locale: Optional[dict] = None

    def update_language(self, language: str) -> None:
        """
        Updates current locale dict.
        """
        self.language = language
        self.current_locale = self.locales.get(self.language, {})

        if not self.current_locale:
            logger.error(f"Locale for {self.language} is missing.")
            return

    def tr(self, message_key: str) -> str:
        """
        Returns phrase in current language by requested key.

        If key is missing - returns key.
        """
        if message_key not in self.current_locale:
            logger.error(f"{message_key} key is missing "
                         f"for {self.language} language.")
            return message_key
        return self.current_locale[message_key]
