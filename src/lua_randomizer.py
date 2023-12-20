from config import Config
from randomizer import Randomizer

from icecream import ic

class LuaRandomizer(Randomizer):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

        self.options: dict = self.manifest.get("Lua")
        self.vars_path = self.game_path / "data/scripts/randomizer_vars.lua"
        self.var_statuses = {}
    
    def configure_randomization(self):
        working_set = []
        var_statuses = {}
        for option, group in self.options.items():
            if not self.params.get(option, False):
                status = False
            else:
                status = True
            var_statuses.update({group.get("Variable"): status})
            self.var_statuses = var_statuses

            working_set.append(group)
        
        return working_set

    def create_var_file(self) -> None:
        with open(self.vars_path, "w", encoding="windows-1251") as stream:
            stream.write("LOG(\"Setting randomizer globals...\")\n\n")

    def enable_var(self, lua_info: dict) -> None:
        content = ""

        var: str = lua_info.get("Variable")
        prototypes: dict = lua_info.get("Prototypes")

        if var: content = f"{var} = {str(self.var_statuses.get(var)).lower()}\n\n"
        if prototypes:
            for num, group in enumerate(prototypes.values()):
                # this is terrible and horrific code
                # maybe one day I'll refactor it
                content = f"{content}{var}_{num+1} = "
                arr = "{\"" + "\", \"".join(group) + "\"}"
                content = f"{content}{arr}\n\n"
        
        with open(self.vars_path, "a", encoding="windows-1251") as stream:
            stream.write(content)

    def set_ending_to_file(self):
        with open(self.vars_path, "a", encoding="windows-1251") as stream:
            stream.write(f"LOG(\"Randomizer globals set.\")\n\nEXECUTE_SCRIPT \"data/scripts/randomizer.lua\"")
    
    def start_randomization(self) -> None:
        working_set = self.configure_randomization()

        if not any(self.var_statuses.values()):
            self.logger.info("Nothing to randomize.")
            return
    
        self.create_var_file()

        for group in working_set:
            self.enable_var(group)
    
        self.set_ending_to_file()