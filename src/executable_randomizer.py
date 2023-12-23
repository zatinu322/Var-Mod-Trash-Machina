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
        # we should not overwrite global const
        offsets_exe = OFFSETS_EXE.copy()
        offsets = generate_offsets()

        if "Render" in self.options.values():
            offsets_exe.update(offsets.get("render"))
        if "Gravity" in self.options.values():
            offsets_exe.update(offsets.get("gravity"))
        if "FOV" in self.options.values():
            offsets_exe.update(offsets.get("fov"))
        if "Armor" in self.options.values():
            offsets_exe.update(offsets.get("armor"))

        return offsets_exe

    def collect_info(self, config: dict):
        info = {}
        if "Render" in self.options.values():
            info.update({"new_models_render": config.get(0x30808B)})
        if "Gravity" in self.options.values():
            info.update({"new_gravity": config.get(0x202D25)})
        if "FOV" in self.options.values():
            info.update({"new_fov": round(config.get(0x5E5A74), 3)})

        return info

    def randomize(self) -> dict:
        file_path = self.game_path / self.options.get("File")
        offsets_exe = self.generate_offsets()

        # code by Aleksandr "Seel" Parfenenkov
        with open(file_path, "rb+") as exe:
            for offset in offsets_exe:
                exe.seek(offset)
                if type(offsets_exe[offset]) == int:
                    exe.write(struct.pack("i", offsets_exe[offset]))
                elif type(offsets_exe[offset]) == str: # hex address
                    exe.write(struct.pack("<L", int(offsets_exe[offset], base=16)))
                elif type(offsets_exe[offset]) == float:
                    exe.write(struct.pack("f", offsets_exe[offset]))
        
        return offsets_exe
        
        
    def start_randomization(self) -> None:
        self.configure_randomization()
        if len(self.options) <= 1:
            self.logger.info("Nothing to randomize.")
            return
        
        offsets_exe = self.randomize()

        ic(self.collect_info(offsets_exe))