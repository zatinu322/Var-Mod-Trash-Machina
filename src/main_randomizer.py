from file_copier import FileCopier
from file_randomizer import FileRandomizer
from text_randomizer import TextRandomizer
from models_randomizer import ModelsRandomizer
from barnpc_randomizer import BarNpcRandomizer
from landscape_randomizer import LandscapeRandomizer
from executable_randomizer import ExecutableRandomizer
from lua_randomizer import LuaRandomizer
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

    barnpc_randomizer = BarNpcRandomizer(config)
    barnpc_randomizer.start_randomization()
    total_errors += barnpc_randomizer.errors

    logger.info("Randomizing landscape.")
    ic("Randomizing landscape.")

    landscape_randomizer = LandscapeRandomizer(config)
    landscape_randomizer.start_randomization()
    total_errors += landscape_randomizer.errors

    logger.info("Randomizing executable.")
    ic("Randomizing executable.")

    executable_randomizer = ExecutableRandomizer(config)
    executable_randomizer.start_randomization()
    total_errors += executable_randomizer.errors

    logger.info("Activating randomizing via lua.")
    ic("Activating randomizing via lua.")

    lua_randomizer = LuaRandomizer(config)
    lua_randomizer.start_randomization()
    total_errors += lua_randomizer.errors

    ic("Done!")
