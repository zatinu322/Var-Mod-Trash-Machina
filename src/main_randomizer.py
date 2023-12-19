from file_copier import FileCopier
from file_randomizer import FileRandomizer
from text_randomizer import TextRandomizer
from models_randomizer import ModelsRandomizer
from config import Config

from icecream import ic

import logging

logger = logging.getLogger("pavlik")

def main(config: Config) -> None:
    total_errors = 0

    logger.info("Copying necessary files.")
    ic("Copying necessary files.")

    file_copier = FileCopier(config)
    file_copier.transfer_files()
    total_errors += file_copier.errors

    logger.info("Randomizing files.")
    ic("Randomizing files.")

    file_randomizer = FileRandomizer(config)
    file_randomizer.start_randomization()
    total_errors += file_randomizer.errors

    logger.info("Randomizing text.")
    ic("Randomizing text.")

    text_randomizer = TextRandomizer(config)
    text_randomizer.start_randomization()
    total_errors += text_randomizer.errors

    logger.info("Randomizing models.")
    ic("Randomizing models.")

    models_randomizer = ModelsRandomizer(config)
    models_randomizer.start_randomization()
    total_errors += models_randomizer.errors

    logger.info("Randomizing NPC in bars.")
    ic("Randomizing NPC in bars.")

    

    ic("Done!")
