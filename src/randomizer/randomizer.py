import logging
from pathlib import Path

from helpers.file_utils import FileCopier, FileEditor
from .file_randomizer import FileRandomizer
from .text_randomizer import TextRandomizer
from .models_randomizer import ModelsRandomizer
from .barnpc_randomizer import BarNpcRandomizer
from .landscape_randomizer import LandscapeRandomizer
from .executable_randomizer import ExecutableRandomizer
from .lua_randomizer import LuaRandomizer
from config.randomization_config import RandomizationParams

logger = logging.getLogger(Path(__file__).name)


class Randomizer:
    def __init__(self, params: RandomizationParams) -> None:
        self.params = params

    def copy_files(self) -> None:
        logger.info("Copying necessary files.")

        file_copier = FileCopier(self.params)
        file_copier.copy_files()

    def edit_files(self) -> None:
        logger.info("Editing necessary files.")

        file_editor = FileEditor(self.params)
        file_editor.edit_files()

    def randomize_files(self):
        logger.info("Randomizing files.")

        file_randomizer = FileRandomizer(self.params)
        file_randomizer.start_randomization()

    def randomize_text(self):
        logger.info("Randomizing text.")

        text_randomizer = TextRandomizer(self.params)
        text_randomizer.start_randomization()

    def randomize_models(self):
        logger.info("Randomizing models.")

        models_randomizer = ModelsRandomizer(self.params)
        models_randomizer.start_randomization()

    def randomize_barnpcs(self):
        logger.info("Randomizing NPC in bars.")

        barnpc_randomizer = BarNpcRandomizer(self.params)
        barnpc_randomizer.start_randomization()

    def randomize_landscape(self):
        logger.info("Randomizing landscape.")

        landscape_randomizer = LandscapeRandomizer(self.params)
        landscape_randomizer.start_randomization()

    def randomize_executable(self) -> dict:
        logger.info("Randomizing executable.")

        executable_randomizer = ExecutableRandomizer(self.params)
        exe_options = executable_randomizer.start_randomization()

        return exe_options

    def randomize_lua(self):
        logger.info("Activating randomizing via lua.")

        lua_randomizer = LuaRandomizer(self.params)
        lua_randomizer.start_randomization()
