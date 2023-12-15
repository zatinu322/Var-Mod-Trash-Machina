from randomizer import Randomizer
from pathlib import Path

import logging

from random import shuffle
from icecream import ic

import shutil
import os

logger = logging.getLogger("pavlik")

class FileRandomizer(Randomizer):
    def __init__(self, main_app) -> None:
        super().__init__(main_app)

        self.temp_dir = Path(self.config.game_path) / "temp_random"
        self.files = self.manifest.get("Files")

    def copy_files(self, groups: list[dict], repeated_files: list = None, dest = "temp") -> list[bool]:
        repeatitions = 0
        if not repeated_files: repeated_files = []
        for group in groups:
            for k,v in group.items():
                for file in v:
                    data_path = Path(self.config.game_path) / k / file
                    temp_path = Path(self.temp_dir) / file
                    try:
                        if dest == "temp":
                            if temp_path.exists():
                                new_temp_path = temp_path / f"_{str(repeatitions)}"
                                repeated_files.append((data_path, new_temp_path))
                                repeated_files += 1
                                temp_path = new_temp_path
                            shutil.copyfile(data_path, temp_path)
                        elif dest == "data":
                            if temp_path.exists():
                                shutil.copyfile(temp_path, data_path)
                                os.remove(temp_path)
                            else:
                                for dp, ntp in repeated_files:
                                    if dp == data_path:
                                        os.rename(ntp, temp_path)
                                        shutil.copyfile(temp_path, data_path)
                                        os.remove(temp_path)
                    except FileNotFoundError as e:
                        logger.error(e)
        return [True, repeated_files]

    def rename_files(self, files_list: list, bckw = False) -> bool:
        filename = 0
        for file in files_list:
            old_file_path = self.temp_dir / file
            new_file_path = self.temp_dir / str(filename)
            try:
                if not bckw:
                    os.rename(old_file_path, new_file_path)
                elif bckw:
                    os.rename(new_file_path, old_file_path)
            except FileNotFoundError as exc:
                logger.error(exc)
            except FileExistsError as exc:
                logger.error(exc)
            
            filename += 1
        
        return True
    
    def randomize(self, groups: list) -> bool:
        repeatitions = self.copy_files(groups, dest="temp")

        files_list = os.listdir(self.temp_dir)

        self.rename_files(files_list)

        shuffle(files_list)

        self.rename_files(files_list, bckw=True)

        if repeatitions[1]:
            self.copy_files(groups, repeated_files=repeatitions[1], dest="data")
        else:
            self.copy_files(groups, dest="data")
        
        return True

    def start_randomization(self):
        ic(self.main_app.config.config)
        working_set = self.manifest.exclude_disabled(self.files, self.main_app.config.config)
        ic(working_set)
        # print(self.manifest)
        # print(self.main_app.config)
        # working_set = self.manifest.exclude_disabled(self.main_app.config.)
        pass