import sys, design, options, os, yaml, randomizer, logging
from PyQt5 import QtWidgets, QtCore, QtGui

logging.basicConfig(filename = "randomizer.log",
                    level = logging.INFO,
                    format = "[%(levelname)s][%(asctime)s]: %(message)s", 
                    filemode= "w", 
                    datefmt="%m/%d/%Y %H:%M:%S")

logger = logging.getLogger()

VERSION = "Ex Machina Randomizer beta v1.1"

MAIN_PATH = os.getcwd()
ERRORS = 0

class OptionsWindow(QtWidgets.QMainWindow, options.Ui_Options):

    submitted = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon("resources/randomizer.ico"))

        self.btnApply.clicked.connect(self.ApplySettings)
        self.btnSelect.clicked.connect(self.select_all)
        self.btnDeselect.clicked.connect(self.deselect_all)

        RandomizerApp.ImportSetting(self, "Checkboxes")
    
    def select_all(self):
        checkboxes = [self.icons_1, self.icons_2, self.icons_3, 
                      self.icons_4, self.icons_5, self.icons_6, 
                      self.icons_7, self.icons_8, self.icons_9, 
                      self.icons_10, self.text_1, self.text_2, 
                      self.text_3, self.text_4, self.text_5, 
                      self.text_6, self.text_7, self.text_8, 
                      self.music_1, self.music_2, self.music_3, 
                      self.music_4, self.music_5, self.music_6, 
                      self.music_7, self.music_8, self.music_9, 
                      self.music_10, self.models_1, self.models_2, 
                      self.models_3, self.models_4, self.models_5, 
                      self.models_6, self.models_7, self.models_8, 
                      self.textures_1, self.textures_2, self.textures_3, 
                      self.textures_4, self.textures_5, self.textures_6, 
                      self.other_1, self.other_2, self.other_3, 
                      self.other_3_1, self.other_4, self.exe_1, 
                      self.exe_2, self.exe_3, self.exe_4]
        
        for chkbx in checkboxes:
            chkbx.setChecked(True)

    def deselect_all(self):
        checkboxes = [self.icons_1, self.icons_2, self.icons_3, 
                      self.icons_4, self.icons_5, self.icons_6, 
                      self.icons_7, self.icons_8, self.icons_9, 
                      self.icons_10, self.text_1, self.text_2, 
                      self.text_3, self.text_4, self.text_5, 
                      self.text_6, self.text_7, self.text_8, 
                      self.music_1, self.music_2, self.music_3, 
                      self.music_4, self.music_5, self.music_6, 
                      self.music_7, self.music_8, self.music_9, 
                      self.music_10, self.models_1, self.models_2, 
                      self.models_3, self.models_4, self.models_5, 
                      self.models_6, self.models_7, self.models_8, 
                      self.textures_1, self.textures_2, self.textures_3, 
                      self.textures_4, self.textures_5, self.textures_6, 
                      self.other_1, self.other_2, self.other_3, 
                      self.other_3_1, self.other_4, self.exe_1, 
                      self.exe_2,  self.exe_3, self.exe_4]
        
        for chkbx in checkboxes:
            chkbx.setChecked(False)
    
    def ApplySettings(self):
        settings = RandomizerApp.ImportSetting(self, "ReadOnly")
        checkboxes_yaml = settings["Settings"]["Checkboxes"]

        checkboxes_keys = [["Icons", "Maps"], ["Icons", "Digits"], ["Icons", "Splashes"], 
                           ["Icons", "DialogsBackground"], ["Icons", "Clans"], ["Icons", "Interface"], 
                           ["Icons", "Radar"], ["Icons", "GunsAndWares"], ["Icons", "CabinsAndBaskets"], 
                           ["Icons", "Smartcursor"], ["Text", "Names"], ["Text", "Dialogs"], 
                           ["Text", "QuestInfoGlobal"], ["Text", "BindNames"], ["Text", "FadingMsgs"], 
                           ["Text", "Interface"], ["Text", "BooksAndHistory"], ["Text", "Descriptions"], 
                           ["Sounds", "Music"], ["Sounds", "Speech"], ["Sounds", "RadioSounds"], 
                           ["Sounds", "Crash"], ["Sounds", "Explosion"], ["Sounds", "Engine"], 
                           ["Sounds", "Horn"], ["Sounds", "Hit"], ["Sounds", "Shooting"], 
                           ["Sounds", "Other"], ["Models", "Static"], ["Models", "Towns"], 
                           ["Models", "Guns"], ["Models", "Trees"], ["Models", "BarNpc"], 
                           ["Models", "Wheels"], ["Models", "Humans"], ["Models", "Dwellers"], 
                           ["Textures", "Surround"], ["Textures", "Masks"], ["Textures", "VehicleSkins"], 
                           ["Textures", "Lightmaps"], ["Textures", "WeatherTex"], ["Textures", "Tiles"], 
                           ["Other", "Weather"], ["Other", "Landscape"], ["Other", "Prototypes"], 
                           ["Other", "PlayerVehicle"], ["Other", "VehicleGuns"], ["Exe", "ModelsRender"], 
                           ["Exe", "Gravity"], ["Exe", "FOV"], ["Exe", "ArmorColor"]]

        checkboxes_values = [self.icons_1.isChecked(), self.icons_2.isChecked(), self.icons_3.isChecked(), 
                             self.icons_4.isChecked(), self.icons_5.isChecked(), self.icons_6.isChecked(), 
                             self.icons_7.isChecked(), self.icons_8.isChecked(), self.icons_9.isChecked(), 
                             self.icons_10.isChecked(), self.text_1.isChecked(), self.text_2.isChecked(), 
                             self.text_3.isChecked(), self.text_4.isChecked(), self.text_5.isChecked(), 
                             self.text_6.isChecked(), self.text_7.isChecked(), self.text_8.isChecked(), 
                             self.music_1.isChecked(), self.music_2.isChecked(), self.music_3.isChecked(), 
                             self.music_4.isChecked(), self.music_5.isChecked(), self.music_6.isChecked(), 
                             self.music_7.isChecked(), self.music_8.isChecked(), self.music_9.isChecked(), 
                             self.music_10.isChecked(), self.models_1.isChecked(), self.models_2.isChecked(), 
                             self.models_3.isChecked(), self.models_4.isChecked(), self.models_5.isChecked(), 
                             self.models_6.isChecked(), self.models_7.isChecked(), self.models_8.isChecked(), 
                             self.textures_1.isChecked(), self.textures_2.isChecked(), self.textures_3.isChecked(), 
                             self.textures_4.isChecked(), self.textures_5.isChecked(), self.textures_6.isChecked(), 
                             self.other_1.isChecked(), self.other_2.isChecked(), self.other_3.isChecked(), 
                             self.other_3_1.isChecked(), self.other_4.isChecked(), self.exe_1.isChecked(), 
                             self.exe_2.isChecked(), self.exe_3.isChecked(), self.exe_4.isChecked()]

        index = 0
        for key in checkboxes_keys:
            checkboxes_yaml[key[0]][key[1]] = checkboxes_values[index]
            index += 1
        
        if self.disable_lua.isChecked():
            settings["Settings"]["RestoreLua"] = True
        else:
            settings["Settings"]["RestoreLua"] = False
        
        if self.enable_debug.isChecked():
            settings["Settings"]["DebugMode"] = True
        else:
            settings["Settings"]["DebugMode"] = False

        with open("resources/settings.yaml", "w") as new_yaml:
            yaml.dump(settings, new_yaml)

        self.submitted.emit()

        self.close()
    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.submitted.emit()
        return super().closeEvent(a0)

class RandomizerApp(QtWidgets.QMainWindow, design.Ui_ExMachinaRandomizer):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon("resources/randomizer.ico"))

        self.btnBrowse.clicked.connect(self.browse_folder)
        self.btnOptions.clicked.connect(self.options_create)
        self.btnStart.clicked.connect(self.StartRandomizing)

        self.trans = QtCore.QTranslator(self)

        self._closable = True

        rb = self.ImportSetting("RadioButton")
        rb.setChecked(True)
        
        self.DestFolder.setText(self.ImportSetting("Path"))

        self.in_logger.append(f"{VERSION}\n")

        languages = [("Русский", "rus"), ("English", "eng")]
        for item, (text, lang) in enumerate(languages):
            self.LangSelect.addItem(text)
            self.LangSelect.setItemData(item, lang)
        
        self.LangSelect.currentIndexChanged.connect(self.lang_changed)

        self.LangSelect.setCurrentText(self.ImportSetting("Language"))

        self._translate = QtCore.QCoreApplication.translate

        global MESSAGES
        MESSAGES = self.messages_setup()

        # remove this, when cp and cr compability appears
        self.rbtn_cp.setEnabled(False)
        self.rbtn_cr.setEnabled(False)
    
    def lang_changed(self):
        data = self.LangSelect.currentData()
        if data:
            self.trans.load(f"resources/localizations/{data}/design.qm")
            QtWidgets.QApplication.instance().installTranslator(self.trans)
            self.retranslateUi(self)
        else:
            QtWidgets.QApplication.instance().removeTranslator(self.trans)
    
    def messages_setup(self):
        message_loc = os.path.join(MAIN_PATH, "resources/localizations/messages.yaml")

        if os.path.exists(message_loc):
            with open(message_loc, encoding="utf-8") as messages_yaml:
                messages = yaml.safe_load(messages_yaml)
                return messages
    
    def loc_string(self, yaml_messages, module, string):
        lang = self.LangSelect.currentData()
        localized_string = yaml_messages[module][string][lang]
        return localized_string
        
    def browse_folder(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, self.loc_string(MESSAGES, "Main", "DirectoryChoose"))
        if directory:
            self.DestFolder.setText(directory)
            return directory
    
    def options_create(self):
        self.optionsWindow = OptionsWindow()
        self.optionsWindow.submitted.connect(self.EnableMainWindow)
        self.optionsWindow.show()
        
        data = self.LangSelect.currentData()
        if data:
            self.trans.load(f"resources/localizations/{data}/options.qm")
            QtWidgets.QApplication.instance().installTranslator(self.trans)
        self.optionsWindow.retranslateUi(self.optionsWindow)

        self.setEnabled(False)
        self._closable = False
    
    def EnableMainWindow(self):
        self._closable = True
        self.setEnabled(True)
    
    def addMessage(self, message):
        self.in_logger.append(f"{message}\n")
        self.in_logger.repaint()

    def clearTextLog(self):
        self.in_logger.clear()
        self.addMessage(VERSION)
    
    def showPopUp(self, message, warning=None):
        msg = QtWidgets.QMessageBox()
        msg.setText(message)
        msg.setWindowIcon(QtGui.QIcon("resources/randomizer.ico"))
        if warning:
            msg.setWindowTitle("Warning")
            msg.setIcon(QtWidgets.QMessageBox.Warning)
        else:
            msg.setWindowTitle("Error")
            msg.setIcon(QtWidgets.QMessageBox.Critical)

            self.addMessage(self.loc_string(MESSAGES, "Main", "RandomAborted"))
        
        msg.exec_()
        
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self._closable:
            logger.info("Saving user settings before closing program...")

            last_path = self.DestFolder.text()

            if self.rbtn_steam.isChecked():
                last_version = "Steam"
            elif self.rbtn_cp.isChecked():
                last_version = "CommunityPatch"
            elif self.rbtn_cr.isChecked():
                last_version = "CommunityRemaster"
            elif self.rbtn_isl.isChecked():
                last_version = "ImprovedStoryline"
            
            last_language = self.LangSelect.currentText()

            settings = self.ImportSetting("ReadOnly")
            settings["Settings"]["LastPath"] = last_path
            settings["Settings"]["LastVersion"] = last_version
            settings["Settings"]["LastLanguage"] = last_language

            with open("resources/settings.yaml", "w") as new_yaml:
                yaml.dump(settings, new_yaml)
            
            logger.info("User settings successfuly saved.")
            logger.info("Exiting program...")

            return super().closeEvent(a0)
        else:
            a0.ignore()
    
    def getExeVersion(self, exe_name):
        try:
            with open(exe_name, "rb+") as exe:
                exe.seek((0x005906A3))
                version_identifier = exe.read(15)
            if version_identifier[8:12] == b"1.02":
                exe_version = "Steam"
            elif version_identifier[3:7] == b"1.10":
                exe_version = "CommunityRemaster"
            elif version_identifier[:4] == b"1.10":
                exe_version = "CommunityPatch"
            else:
                exe_version = "Unsupported"
            return exe_version
        except PermissionError:
            self.addMessage(f"{self.loc_string(MESSAGES, 'Main', 'PermissionErrorExe1')} {exe_name}. {self.loc_string(MESSAGES, 'Main', 'PermissionErrorExe2')}")
            logger.critical(f"Unable to open {exe_name} due to permission error. Make sure that your game is not running.")
        

    def validateUserInput(self, workpath, gameversion):
        logger.info("Starting files validation...")
        logger.info(f"UserPath: {workpath}")
        logger.info(f"UserGameVersion: {gameversion}")
    
        validation = True

        if os.path.exists(workpath):
            if os.path.exists(os.path.join(workpath, "data")):
                os.chdir(os.path.join(workpath, "data"))
                data_dir = os.listdir()
                needed_files = ["gamedata", "if", "maps", "models", "music", "sounds", "tiles", "weathertexs"]

                for file in needed_files:
                    if file in data_dir:
                        continue
                    else:
                        logger.critical(f"{file} missing in {os.getcwd()}. Randomization aborted.")
                        self.addMessage(self.loc_string(MESSAGES, 'Main', 'WrongGamePath'))
                        validation = False
                        break
                
                if validation:
                    logger.info("Files validated. Checking game version...")

                    os.chdir(workpath)
                    config = randomizer.set_yaml(self, MAIN_PATH, gameversion)
                    if config:
                        try:
                            exe_name = config["Exe"]
                        except KeyError:
                            logger.critical("Unable to read yaml-configuration file.")
                            self.showPopUp(self.loc_string(MESSAGES, "Main", "CorruptedConfig"))
                            return [False, None, None]

                        if exe_name: 
                            if exe_name in os.listdir():
                                exe_version = self.getExeVersion(exe_name)
                                if exe_version:
                                
                                    logger.info(f"Exe version determined as {exe_version}")

                                    if gameversion == "Steam":
                                        if exe_version == "Steam":
                                            return [True, gameversion, exe_version]
                                        elif exe_version == "CommunityPatch":
                                            logger.critical(f"Community Patch is installed in {workpath}, but {gameversion} version expected. Randomization aborted.")
                                            self.showPopUp(self.loc_string(MESSAGES, "Main", "CommunityPatchInstalled"))
                                            return [False, gameversion, exe_version]
                                        elif exe_version == "CommunityRemaster":
                                            logger.critical(f"Community Remaster is installed in {workpath}, but {gameversion} version expected. Randomization aborted.")
                                            self.showPopUp(self.loc_string(MESSAGES, "Main", "CommunityRemasterInstalled"))
                                            return [False, gameversion, exe_version]
                                        elif exe_version == "Unsupported":
                                            logger.warning("Unsupported game version detected. Waiting user input...")
                                            msg = QtWidgets.QMessageBox.warning(self, "Warning", self.loc_string(MESSAGES, "Main", "NotSteamLicense"), QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)
                                            if msg == QtWidgets.QMessageBox.Ok:
                                                logger.info("User proceeded randomization.")
                                                return [True, gameversion, exe_version]
                                            else:
                                                logger.info("Randomization aborted by user.")
                                                return [False, gameversion, exe_version]
                                    elif gameversion == "CommunityPatch":
                                        if exe_version == "CommunityPatch":
                                            return [True, gameversion, exe_version]
                                        else:
                                            logger.critical(f"Community Patch is not installed in {workpath}. Randomization aborted.")
                                            self.showPopUp(self.loc_string(MESSAGES, "Main", "CommunityPatchNotInstalled"))
                                            return [False, gameversion, exe_version]
                                    elif gameversion == "CommunityRemaster":
                                        if exe_version == "CommunityRemaster":
                                            return [True, gameversion, exe_version]
                                        else:
                                            logger.critical(f"Community Remaster is not installed in {workpath}. Randomization aborted.")
                                            self.showPopUp(self.loc_string(MESSAGES, "Main", "CommunityRemasterNotInstalled"))
                                            return [False, gameversion, exe_version]
                                    elif gameversion == "ImprovedStoryline":
                                        if exe_version == "Steam":
                                            check_path = os.path.join(workpath, "data/if/map/r1m5.dds")
                                            if os.path.exists(check_path):
                                                return [True, gameversion, exe_version]
                                            else:
                                                logger.critical(f"Improved Storyline is not installed in {workpath}. Randomization aborted.")
                                                self.showPopUp(self.loc_string(MESSAGES, "Main", "NotImprovedStoryline"))
                                                return(False, gameversion, exe_version)
                                        elif exe_version == "CommunityPatch":
                                            logger.critical(f"Community Patch is installed in {workpath}, but {gameversion} version expected. Randomization aborted.")
                                            self.showPopUp(self.loc_string(MESSAGES, "Main", "CommunityPatchInstalled"))
                                            return [False, gameversion, exe_version]
                                        elif exe_version == "CommunityRemaster":
                                            logger.critical(f"Community Remaster is installed in {workpath}, but {gameversion} version expected. Randomization aborted.")
                                            self.showPopUp(self.loc_string(MESSAGES, "Main", "CommunityRemasterInstalled"))
                                            return [False, gameversion, exe_version]
                                        elif exe_version == "Unsupported":
                                            logger.warning("Unsupported game version detected. Waiting user input...")
                                            msg = QtWidgets.QMessageBox.warning(self, "Warning", self.loc_string(MESSAGES, "Main", "NotSteamLicense"), QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)
                                            if msg == QtWidgets.QMessageBox.Ok:
                                                logger.info("User proceeded randomization.")
                                                check_path = os.path.join(workpath, "data/if/map/r1m5.dds")
                                                if os.path.exists(check_path):
                                                    return [True, gameversion, exe_version]
                                                else:
                                                    logger.critical(f"Improved Storyline is not installed in {workpath}. Randomization aborted.")
                                                    self.showPopUp(self.loc_string(MESSAGES, "Main", "NotImprovedStoryline"))
                                                    return(False, gameversion, exe_version)
                                            else:
                                                logger.info("Randomization aborted by user.")
                                                return [False, gameversion, exe_version]
                                else:
                                    self.showPopUp(f"{self.loc_string(MESSAGES, 'Main', 'PermissionErrorExe3')} {exe_name}")
                                    return [False, None, None]
                            else:
                                logger.critical(f"{exe_name} is missing in {workpath}")
                                self.showPopUp(f"{exe_name} {self.loc_string(MESSAGES, 'Main', 'MissingExe')}")
                                return [False, None, None]
                    else:
                        return [False, None, None]
                else:
                    return [False, None, None]
            else:
                logger.critical(f"Path {workpath} does not exists.")
                self.addMessage(self.loc_string(MESSAGES, "Main", "PathDoesNotExists"))
                return [False, None, None]

        else:
            logger.critical(f"Path {workpath} does not exists.")
            self.addMessage(self.loc_string(MESSAGES, "Main", "PathDoesNotExists"))
            return [False, None, None]
    
    def StartRandomizing(self):
        self.clearTextLog()
        self.lang_changed()

        if self.rbtn_steam.isChecked():
            gameversion = "Steam"
        elif self.rbtn_cp.isChecked():
            gameversion = "CommunityPatch"
        elif self.rbtn_cr.isChecked():
            gameversion = "CommunityRemaster"
        elif self.rbtn_isl.isChecked():
            gameversion = "ImprovedStoryline"

        settings = self.ImportSetting("ReadOnly")

        workpath = self.DestFolder.text()

        access = self.validateUserInput(workpath, gameversion)
        if access[0]:
            gameversion = access[1]
            exe_version = access[2]
            logger.info("Game version checked.")
            self.addMessage(self.loc_string(MESSAGES, "Main", "CorrectInput"))
            self.btnStart.setEnabled(False)
            self._closable = False
            self.btnStart.repaint()
            language = self.LangSelect.currentData()
            randomizer.main_randomizing_start(self, logger, MAIN_PATH, gameversion, workpath, settings, language, MESSAGES, exe_version)
            self.btnStart.setEnabled(True)
            self._closable = True
        else:
            self.in_logger.append(self.loc_string(MESSAGES, "Main", "RandomAborted"))

    def ImportSetting(self, setting):
        os.chdir(MAIN_PATH)
        with open("resources/settings.yaml", encoding="utf-8") as options_yaml:
            settings = yaml.safe_load(options_yaml)
        
        if setting == "Checkboxes":

            checkbox = settings["Settings"]["Checkboxes"]
            checkbox_values = [checkbox["Icons"]["Maps"], checkbox["Icons"]["Digits"], 
                               checkbox["Icons"]["Splashes"], checkbox["Icons"]["DialogsBackground"], 
                               checkbox["Icons"]["Clans"], checkbox["Icons"]["Interface"], 
                               checkbox["Icons"]["Radar"], checkbox["Icons"]["GunsAndWares"], 
                               checkbox["Icons"]["CabinsAndBaskets"], checkbox["Icons"]["Smartcursor"], 
                               checkbox["Text"]["Names"], checkbox["Text"]["Dialogs"], 
                               checkbox["Text"]["QuestInfoGlobal"], checkbox["Text"]["BindNames"], 
                               checkbox["Text"]["FadingMsgs"], checkbox["Text"]["Interface"], 
                               checkbox["Text"]["BooksAndHistory"], checkbox["Text"]["Descriptions"], 
                               checkbox["Sounds"]["Music"], checkbox["Sounds"]["Speech"], 
                               checkbox["Sounds"]["RadioSounds"], checkbox["Sounds"]["Crash"], 
                               checkbox["Sounds"]["Explosion"], checkbox["Sounds"]["Engine"], 
                               checkbox["Sounds"]["Horn"], checkbox["Sounds"]["Hit"], 
                               checkbox["Sounds"]["Shooting"], checkbox["Sounds"]["Other"], 
                               checkbox["Models"]["Static"], checkbox["Models"]["Towns"], 
                               checkbox["Models"]["Guns"], checkbox["Models"]["Trees"], 
                               checkbox["Models"]["BarNpc"], checkbox["Models"]["Wheels"], 
                               checkbox["Models"]["Humans"], checkbox["Models"]["Dwellers"], 
                               checkbox["Textures"]["Surround"], checkbox["Textures"]["Masks"], 
                               checkbox["Textures"]["VehicleSkins"], checkbox["Textures"]["Lightmaps"], 
                               checkbox["Textures"]["WeatherTex"], checkbox["Textures"]["Tiles"], 
                               checkbox["Other"]["Weather"], checkbox["Other"]["Landscape"], 
                               checkbox["Other"]["Prototypes"], checkbox["Other"]["PlayerVehicle"],
                               checkbox["Other"]["VehicleGuns"], checkbox["Exe"]["ModelsRender"], 
                               checkbox["Exe"]["Gravity"], checkbox["Exe"]["FOV"], 
                               checkbox["Exe"]["ArmorColor"]]
   
            checkboxes = [self.icons_1, self.icons_2, self.icons_3, 
                        self.icons_4, self.icons_5, self.icons_6,
                        self.icons_7, self.icons_8, self.icons_9, 
                        self.icons_10, self.text_1, self.text_2, 
                        self.text_3, self.text_4, self.text_5, 
                        self.text_6, self.text_7, self.text_8, 
                        self.music_1, self.music_2, self.music_3, 
                        self.music_4, self.music_5, self.music_6, 
                        self.music_7, self.music_8, self.music_9, 
                        self.music_10, self.models_1, self.models_2, 
                        self.models_3, self.models_4, self.models_5, 
                        self.models_6, self.models_7, self.models_8, 
                        self.textures_1, self.textures_2, self.textures_3, 
                        self.textures_4, self.textures_5, self.textures_6, 
                        self.other_1, self.other_2, self.other_3, 
                        self.other_3_1, self.other_4, self.exe_1, 
                        self.exe_2, self.exe_3, self.exe_4]

            index = 0
            for chkbx in checkboxes:
                if checkbox_values[index] == True:
                    chkbx.setChecked(True)
                else:
                    chkbx.setChecked(False)
                index += 1
            
            if settings["Settings"]["RestoreLua"] == True:
                self.disable_lua.setChecked(True)
            else:
                self.disable_lua.setChecked(False)
            
            if settings["Settings"]["DebugMode"] == True:
                self.enable_debug.setChecked(True)
            else:
                self.enable_debug.setChecked(False)
                
        elif setting == "Path":
            path = settings["Settings"]["LastPath"]
            if path:
                return path
            else:
                return os.getcwd()
        
        elif setting == "RadioButton":
            rb = settings["Settings"]["LastVersion"]
            if rb == "Steam":
                return self.rbtn_steam
            elif rb == "CommunityPatch":
                return self.rbtn_cp
            elif rb == "CommunityRemaster":
                return self.rbtn_cr
            elif rb == "ImprovedStoryline":
                return self.rbtn_isl
        
        elif setting == "Language":
            lang = settings["Settings"]["LastLanguage"]
            if lang:
                return lang
                
        elif setting == "ReadOnly":
            return settings

def ResourcesCheck():
    logger.info(f"Launch directory: {MAIN_PATH}")
    logger.info(f"Starting resources validation...")

    resources_path =  os.path.join(MAIN_PATH, "resources")
    necessary_resources_files = ["data", "localizations", "manifests", "settings.yaml", "randomizer.ico"]

    valid = True

    resources = os.listdir(MAIN_PATH)

    if os.path.exists(resources_path):
        resources = os.listdir(resources_path)
        
        for file in necessary_resources_files:
            if file in resources:
                continue
            else:
                valid = False
                logger.critical(f"\"{file}\" not found in {MAIN_PATH}\\resources\\")
                break
        
        os.chdir(MAIN_PATH)
        return valid
    else:
        logger.critical(f"\"resources\" folder not found in {MAIN_PATH}")
        return False

def main():
    logger.info(VERSION)

    if ResourcesCheck() == True:
        logger.info("All files validated. Starting program...")

        app = QtWidgets.QApplication(sys.argv)
        window = RandomizerApp()
        window.show()

        logger.info("Program successfully started. Waiting for user's commands...")

        app.exec_()
    else:
        logger.critical("Unable to run the program. Necessary files missing.")

if __name__ == "__main__":
    main()