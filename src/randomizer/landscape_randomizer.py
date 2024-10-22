import struct
from pathlib import Path
from random import random
import logging

from config.randomization_config import RandomizationParams

logger = logging.getLogger(Path(__file__).name)


class LandscapeRandomizer:
    def __init__(self, params: RandomizationParams) -> None:
        self.params = params

    def check_distortion(
        self,
        folder_path: Path,
        state_file: str,
        restriction: bool
    ) -> bool:
        # check if .landscape present in map folder
        dot_landscape = bool(list(folder_path.glob(state_file)))

        if dot_landscape and restriction:
            logger.info(
                f"Multiple landscape distortion is allowed in {folder_path}."
            )
            return True
        elif not dot_landscape:
            return True
        else:
            logger.info(
                "Multiple landscape distortion is prohibited "
                f"in {folder_path}."
            )
            return False

    def distort_landscape(self, xml_info: dict) -> None:
        for level in xml_info["maps"]:
            folder_path = self.params.game_path / level
            state_file = xml_info["state"]

            multiple_allowed = xml_info["multiple"]

            is_allowed = self.check_distortion(
                folder_path, state_file, multiple_allowed
            )

            if is_allowed:
                file_path = folder_path / xml_info["file"]
                state_file_path = folder_path / state_file

                # create file to register landscape state
                with open(state_file_path, "w") as current_state:
                    current_state.write(f"Distorted in {file_path}")

                # logic by Aleksandr "ThePlain" Fateev
                with open(file_path, "rb") as stream:
                    raw = stream.read()

                count = int(len(raw) / 4)
                fmt = "<" + "f" * count
                data = list(struct.unpack(fmt, raw))
                randomized_data = map(lambda v: v + ((random() - 0.5) * 3),
                                      data)

                with open(file_path, "wb") as stream:
                    stream.write(struct.pack(fmt, *randomized_data))

                logger.info(f"Distorted landscape in {folder_path}")

    def start_randomization(self) -> None:
        if not self.params.landscape:
            logger.info("Nothing to randomize.")
            return

        self.distort_landscape(self.params.landscape)
