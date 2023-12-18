from file_copier import FileCopier
from file_randomizer import FileRandomizer
from config import Config

from icecream import ic

import logging

logger = logging.getLogger("pavlik")

def main(config: Config) -> None:
    logger.info("Copying necessary files.")

    file_copier = FileCopier(config)
    file_copier.transfer_files()

    logger.info("Randomizing files.")

    file_randomizer = FileRandomizer(config)
    file_randomizer.start_randomization()

    # try:
    # FileCopier(main_app)
    # ic("Copying files")
    # file_copier = FileCopier(main_app)
    # file_copier.transfer_files()

    # ic("Randomizing files")
    # file_randomizer = FileRandomizer(main_app)
    # file_randomizer.start_randomization()
    ic("Done!")

    # except Exception as exc:
    #     ic(exc)