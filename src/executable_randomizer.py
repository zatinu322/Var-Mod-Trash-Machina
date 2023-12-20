from config import Config
from randomizer import Randomizer
from data import OFFSETS_EXE, generate_offsets

import struct

from icecream import ic

class ExecutableRandomizer(Randomizer):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

        self.options: dict = self.manifest.get("Executable")

    def configure_randomization(self) -> None:
        for param, status in self.params.items():
            if not param in self.options: continue 
            if status: continue
            
            self.options.pop(param)

    def generate_offsets(self) -> dict:
        # we should not overwrite global var
        offsets_exe = OFFSETS_EXE.copy()
        offsets = generate_offsets()

        if "Render" in self.options.values():
            offsets_exe.update(offsets.get("render"))
        if "Gravity" in self.options.values():
            offsets_exe.update(offsets["gravity"])
        if "FOV" in self.options.values():
            offsets_exe.update(offsets["fov"])
        if "Armor" in self.options.values():
            offsets_exe.update(offsets["armor"])

        return offsets_exe

    def collect_info(self, config: dict):
        info = {
            "new_models_render": config.get(0x30808B),
            "new_gravity": config[0x202D25],
            "new_fov": round(config[0x5E5A74], 3)
        }

        return info

    def randomize(self) -> None:
        file_path = self.game_path / self.options.get("File")
        offsets_exe = self.generate_offsets()

        with open(file_path, "rb+") as exe:
            for offset in offsets_exe:
                exe.seek(offset)
                if type(offsets_exe[offset]) == int:
                    exe.write(struct.pack("i", offsets_exe[offset]))
                elif type(offsets_exe[offset]) == str: # hex address
                    exe.write(struct.pack("<L", int(offsets_exe[offset], base=16)))
                elif type(offsets_exe[offset]) == float:
                    exe.write(struct.pack("f", offsets_exe[offset]))
        
        ic(self.collect_info(offsets_exe))

    def start_randomization(self) -> None:
        self.configure_randomization()
        if len(self.options) <= 1:
            self.logger.info("Nothing to randomize.")
            return
        
        self.randomize()
        