import logging

from file_utils import FileCopier, FileEditor
from file_randomizer import FileRandomizer
from text_randomizer import TextRandomizer
from models_randomizer import ModelsRandomizer
from barnpc_randomizer import BarNpcRandomizer
from landscape_randomizer import LandscapeRandomizer
from executable_randomizer import ExecutableRandomizer
from lua_randomizer import LuaRandomizer
from config import Config

logger = logging.getLogger("pavlik")


def copy_files(working_set: dict) -> None:
    logger.info("Copying necessary files.")

    file_copier = FileCopier(working_set)
    file_copier.copy_files()


def edit_files(working_set: dict) -> None:
    logger.info("Editing necessary files.")

    file_editor = FileEditor(working_set)
    file_editor.edit_files()


def randomize_files(working_set: dict):
    logger.info("Randomizing files.")

    file_randomizer = FileRandomizer(working_set)
    file_randomizer.start_randomization()


def randomize_text(working_set: dict):
    logger.info("Randomizing text.")

    text_randomizer = TextRandomizer(working_set)
    text_randomizer.start_randomization()


def randomize_models(working_set: dict):
    logger.info("Randomizing models.")

    models_randomizer = ModelsRandomizer(working_set)
    models_randomizer.start_randomization()


def randomize_barnpcs(working_set: dict):
    logger.info("Randomizing NPC in bars.")

    barnpc_randomizer = BarNpcRandomizer(working_set)
    barnpc_randomizer.start_randomization()


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
