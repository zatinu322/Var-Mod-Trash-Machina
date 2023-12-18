from randomizer import Randomizer
from config import Config
from pathlib import Path

import logging

from random import shuffle
from icecream import ic

import shutil
import os

logger = logging.getLogger("pavlik")

class FileRandomizer(Randomizer):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

        self.temp_dir = self.game_path / "temp_random"
        self.options = self.manifest.get("Files")

    def copy_files(self, groups: list[dict], repeated_files: list = [], dest = "temp") -> list[bool]:
        repeatitions = 0

        for group in groups:
            for k,v in group.items():
                for file in v:
                    data_path = Path(self.game_path) / k / file
                    temp_path = Path(self.temp_dir) / file
                    try:
                        if dest == "temp":
                            if temp_path.exists():
                                new_temp_path = self.temp_dir / f"{file}_{str(repeatitions)}"
                                repeated_files.append((data_path, new_temp_path))
                                repeatitions += 1
                                logger.debug(f"FileRandomizer: Detected file with the same name. {temp_path} will be changed to {new_temp_path}.")
                                temp_path = new_temp_path
                            logger.debug(f"FileRandomizer: Copying {data_path} to {temp_path}.")
                            shutil.copyfile(data_path, temp_path)
                        elif dest == "data":
                            if temp_path.exists():
                                logger.debug(f"FileRandomizer: Copying {temp_path} to {data_path}.")
                                shutil.copyfile(temp_path, data_path)
                                logger.debug(f"FileRandomizing: Removing {temp_path}.")
                                os.remove(temp_path)
                            else:
                                for dp, ntp in repeated_files:
                                    if dp == data_path:
                                        logger.debug(f"FileRandomizing: Renaming {ntp} to {temp_path}.")
                                        os.rename(ntp, temp_path)
                                        logger.debug(f"FileRandomizing: Copying {temp_path} to {data_path}.")
                                        shutil.copyfile(temp_path, data_path)
                                        logger.debug(f"FileRandomizing: Removing {temp_path}.")
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
                    logger.debug(f"FileRandomizing: Renaming {old_file_path} to {new_file_path}.")
                    os.rename(old_file_path, new_file_path)
                elif bckw:
                    logger.debug(f"FileRandomizing: Renaming {new_file_path} to {old_file_path}.")
                    os.rename(new_file_path, old_file_path)
            except FileNotFoundError as exc:
                logger.error(exc)
            except FileExistsError as exc:
                logger.error(exc)
            
            filename += 1
        
        return True
    
    def randomize(self, groups: list) -> bool:
        if not self.temp_dir.exists():
            os.mkdir(self.temp_dir)
        status, repeatitions = self.copy_files(groups, dest="temp")

        files_list = os.listdir(self.temp_dir)

        self.rename_files(files_list)

        shuffle(files_list)

        self.rename_files(files_list, bckw=True)

        if repeatitions:
            self.copy_files(groups, repeated_files=repeatitions, dest="data")
        else:
            self.copy_files(groups, dest="data")

        os.rmdir(self.temp_dir)
        
        return True

    def start_randomization(self):
        working_set = self.configure_randomization()
        for groups in working_set:
            self.randomize(groups)