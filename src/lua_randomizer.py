from working_set_manager import WorkingSetManager


class LuaRandomizer(WorkingSetManager):
    def __init__(self, working_set: dict) -> None:
        super().__init__(working_set)

        # self.options: dict = self.manifest.get("lua")
        self.vars_path = self.game_path / "data/scripts/randomizer_vars.lua"

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
        if not self.lua:
            self.logger.info("Nothing to randomize.")
            return

        self.create_var_file()

        for group in self.lua:
            self.enable_var(group)

        self.set_ending_to_file()
