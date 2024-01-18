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

def copy_files(config: Config, need_validation: bool = False):
    logger.info("Copying necessary files.")

    file_copier = FileCopier(config, need_validation)
    file_copier.transfer_files()

    return file_copier.errors

def randomize_files(config: Config):
    logger.info("Randomizing files.")

    file_randomizer = FileRandomizer(config)
    status = file_randomizer.start_randomization()
    
    return file_randomizer.errors, status

def randomize_text(config: Config):
    logger.info("Randomizing text.")

    text_randomizer = TextRandomizer(config)
    text_randomizer.start_randomization()

    return text_randomizer.errors

def randomize_models(config: Config):
    logger.info("Randomizing models.")

    models_randomizer = ModelsRandomizer(config)
    models_randomizer.start_randomization()
    
    return models_randomizer.errors

def randomize_barnpcs(config: Config):
    logger.info("Randomizing NPC in bars.")

    barnpc_randomizer = BarNpcRandomizer(config)
    barnpc_randomizer.start_randomization()
    
    return barnpc_randomizer.errors

def randomize_landscape(config: Config):
    logger.info("Randomizing landscape.")

    landscape_randomizer = LandscapeRandomizer(config)
    landscape_randomizer.start_randomization()
    
    return landscape_randomizer.errors

def randomize_executable(config: Config):
    logger.info("Randomizing executable.")

    executable_randomizer = ExecutableRandomizer(config)
    executable_randomizer.start_randomization()

    return executable_randomizer.errors

def randomize_lua(config: Config):
    logger.info("Activating randomizing via lua.")

    lua_randomizer = LuaRandomizer(config)
    lua_randomizer.start_randomization()
    
    return lua_randomizer.errors