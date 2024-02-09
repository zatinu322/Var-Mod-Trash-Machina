import struct
from pathlib import Path

from config import Config
from randomizer import Randomizer
from random import random


class LandscapeRandomizer(Randomizer):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

        self.options = self.manifest.get("landscape")

    def check_distortion(
        self,
        folder_path: Path,
        state_file: str,
        restriction: bool
    ) -> bool:
        # check if .landscape present in map folder
        dot_landscape = bool(list(folder_path.glob(state_file)))

        if dot_landscape and restriction:
            self.logger.info(
                f"Multiple landscape distortion is allowed in {folder_path}."
            )
            return True
        elif not dot_landscape:
            return True
        else:
            self.logger.info(
                f"Multiple landscape distortion is prohibited \
                in {folder_path}."
            )
            return False

    def distort_landscape(self, xml_info: dict) -> None:
        for level in xml_info.get("maps"):
            folder_path = self.game_path / level
            state_file = xml_info.get("state")

            multiple_allowed = xml_info.get("multiple")

            is_allowed = self.check_distortion(
                folder_path, state_file, multiple_allowed
            )

            if is_allowed:
                file_path = folder_path / xml_info.get("file")
                state_file_path = folder_path / state_file

                # create file to register landscape state
                with open(state_file_path, "w") as current_state:
                    current_state.write(str(file_path.resolve()))

                # logic by Aleksandr "ThePlain" Fateev
                with open(file_path, "rb") as stream:
                    raw = stream.read()

                count = int(len(raw) / 4)
                fmt = "<" + "f" * count
                data = list(struct.unpack(fmt, raw))
                data = map(lambda v: v + ((random() - 0.5) * 3), data)

                with open(file_path, "wb") as stream:
                    stream.write(struct.pack(fmt, *data))

                self.logger.info(f"Distorted landscape in {folder_path}")

    def start_randomization(self) -> None:
        working_set = self.configure_randomization()
        if not working_set:
            self.logger.info("Nothing to randomize.")
            return

        for group in working_set:
            self.distort_landscape(group)
