import logging
from pathlib import Path

from working_set_manager import RandomizationParams

logger = logging.getLogger(Path(__file__).name)


class LuaRandomizer:
    def __init__(self, params: RandomizationParams) -> None:
        self.params = params

        # self.options: dict = self.manifest.get("lua")
        self.vars_path = \
            self.params.game_path / "data/scripts/randomizer_vars.lua"

    def create_var_file(self) -> None:
        with open(self.vars_path, "w", encoding="windows-1251") as stream:
            stream.write("LOG(\"Setting randomizer globals...\")\n\n")

    def enable_var(self, lua_info: dict) -> None:
        content = ""

        var: str = lua_info["variable"]
        prototypes: dict = lua_info.get("prototypes")

        # setting variable status
        # .lower because of lua syntax
        content = f"{var} = true\n\n"
        # setting prototypes lists
        if prototypes:
            for num, group in enumerate(prototypes):
                # this is terrible and horrific code
                # maybe one day I'll refactor it
                content = f"{content}{var}_{num+1} = "  # var name
                arr = "{\"" + "\", \"".join(group) + "\"}"  # prototypes list
                content = f"{content}{arr}\n\n"

        with open(self.vars_path, "a", encoding="windows-1251") as stream:
            stream.write(content)

    def set_ending_to_file(self):
        with open(self.vars_path, "a", encoding="windows-1251") as stream:
            stream.write(
                "LOG(\"Randomizer globals set.\")\n\n\
                EXECUTE_SCRIPT \"data/scripts/randomizer.lua\""
            )

    def start_randomization(self) -> None:
        if not self.params.lua:
            logger.info("Nothing to randomize.")
            return

        self.create_var_file()

        for group in self.params.lua:
            self.enable_var(group)

        self.set_ending_to_file()
