import main, random, shutil, struct, math
import xml.etree.ElementTree as ET
from distutils.dir_util import copy_tree

def set_yaml(mainwindow, windowpath, gameversion):
    # loads whole config from yaml
    main.logger.debug(f"SET_YAML: STARTING")

    if gameversion == "Steam" or gameversion == "Unsupported":
        manifest = "manifest.yaml"
    elif gameversion == "CommunityPatch":
        manifest = "manifest_compatch.yaml"
    elif gameversion == "CommunityRemaster":
        manifest = "manifest_comrem.yaml"
    elif gameversion == "ImprovedStoryline":
        manifest = "manifest_isl.yaml"
    
    main.logger.debug(f"SET_YAML: PARSING: {manifest}")

    manifest_path = main.os.path.join(windowpath, f"resources/manifests/{manifest}")

    try:
        with open(manifest_path, encoding="utf-8") as config_file:
            config = main.yaml.safe_load(config_file)
            main.logger.info(f"SET_YAML: SUCCESS: {manifest}")
            return config
    except FileNotFoundError:
        main.logger.critical(f"SET_YAML: FileNotFoundError: {manifest_path}")
        mainwindow.showPopUp(f"{loc_string('Randomizer', 'FileNotFound')} {manifest_path}")
        return False
    except:
        main.logger.critical(f"SET_YAML: CRITICAL: {manifest_path}")
        mainwindow.showPopUp(f"{loc_string('Randomizer', 'UnableToLoad')} {manifest_path}")
        return False
    
def get_yaml(yaml, category, subcategory, sub1=None, sub2=None, sub3=None, sub4=None):
    # getting specific setting from previously loaded yaml
    try:
        main.logger.debug(f"GET_YAML: STARTING: {category} : {subcategory} : {sub1} : {sub2} : {sub3}")
        cat = yaml[category]
        subcat = cat[subcategory]
        if sub1 != None and sub2 == None:
            sub1cat = subcat[sub1]
            main.logger.debug(f"GET_YAML: SUB1CAT: {sub1cat}")
            return sub1cat
        elif sub2 != None and sub3 == None:
            sub1cat = subcat[sub1]
            sub2cat = sub1cat[sub2]
            main.logger.debug(f"GET_YAML: SUB2CAT: {sub2cat}")
            return sub2cat
        elif sub3 != None and sub4 == None:
            sub1cat = subcat[sub1]
            sub2cat = sub1cat[sub2]
            sub3cat = sub2cat[sub3]
            main.logger.debug(f"GET_YAML: SUB3CAT: {sub3cat}")
            return sub3cat
        elif sub4 != None:
            sub1cat = subcat[sub1]
            sub2cat = sub1cat[sub2]
            sub3cat = sub2cat[sub3]
            sub4cat = sub3cat[sub4]
            main.logger.debug(f"GET_YAML: SUB3CAT: {sub4cat}")
            return sub4cat
        else:
            main.logger.debug(f"GET_YAML: SUBCAT: {subcat}")
            return subcat
    except KeyError:
        main.logger.error(f"GET_YAML: KeyError: {category} : {subcategory} : {sub1} : {sub2} : {sub3}")
    except:
        main.logger.critical(f"GET_YAML: CRITICAL: {category} : {subcategory} : {sub1} : {sub2} : {sub3}")

def get_type(variable):
    # determines whether input is list or string
    main.logger.debug(f"GET_TYPE: STARTING: {variable}")
    main.logger.debug(f"GET_TYPE: TYPE: {type(variable)}")
    if isinstance(variable, list):
        main.logger.debug(f"GET_TYPE: TYPE: Determined as \"list\"")
        return "list"
    elif isinstance(variable, str):
        main.logger.debug(f"GET_TYPE: TYPE: Determined as \"str\"")
        return "str"
    
def current_dir(dir, workpath):
    main.logger.debug(f"CURRENT_DIR: STARTING: {dir}")
    directory = main.os.path.join(workpath, dir)
    if main.os.path.exists(directory):
        main.os.chdir(directory)
        main.logger.debug(f"CURRENT_DIR: SUCCESS: {dir}")
        return True
    else:
        main.logger.error(f"CURRENT_DIR: ERROR: {directory} does not exists.")
        return False

def copy(to_copy, where_copy, workpath, filename = None):
    var_type = get_type(to_copy)
    if var_type == "list":

        for file in to_copy:
            dest_path = main.os.path.join(workpath, where_copy, file)

            main.logger.debug(f"COPY: STARTING: {file} to {dest_path}")
            try:
                shutil.copyfile(file, dest_path)
                main.logger.debug(f"COPY: SUCCESS: {file} to {dest_path}")
                return True
            except FileNotFoundError:
                main.logger.error(f"COPY: FileNotFoundError: {file}")
            except:
                main.logger.error(f"COPY: ERROR: Unable to copy {file} from {main.os.getcwd()} to {dest_path}")

    elif var_type == "str":
        if filename == None:
            filename = to_copy
        main.logger.debug(f"COPY: filename={filename}")
        dest_path = main.os.path.join(workpath, where_copy, filename)

        main.logger.debug(f"COPY: STARTING: {to_copy} to {dest_path}")
        try:
            shutil.copyfile(to_copy, dest_path)
            main.logger.debug(f"COPY: SUCCESS: {to_copy} to {dest_path}")
            return True
        except FileNotFoundError:
            main.logger.error(f"COPY: FileNotFoundError: {to_copy}")
        except:
            main.logger.error(f"COPY: ERROR: Unable to copy {to_copy} from {main.os.getcwd()} to {dest_path}")

def copy_folder(to_copy, where_copy):
    main.logger.debug(f"COPY_TREE: STARTING: {to_copy} to {where_copy}")
    if main.os.path.exists(to_copy):
        try:
            copy_tree(to_copy, where_copy)
            main.logger.debug(f"COPY_TREE: SUCCESS: {to_copy} to {where_copy}")
            return True
        except:
            main.logger.error(f"COPY_TREE: ERROR: Unable to copy {to_copy} to {where_copy}")
            return False
    else:
        main.logger.error(f"COPY_TREE: {to_copy} directory does not exists.")
        return False

def move(to_move, where_move, workpath):
    var_type = get_type(to_move)
    dest_path = main.os.path.join(workpath, where_move)
    if main.os.path.exists(dest_path):
        if var_type == "list":
            for file in to_move:
                main.logger.debug(f"MOVE: STARTING: {file} to {dest_path}")
                try:
                    shutil.move(file, dest_path)
                    main.logger.debug(f"MOVE: SUCCESS: {file} to {dest_path}")
                except shutil.Error:
                    main.logger.error(f"MOVE: shutil.Error: {file} is already in {dest_path}")
                except FileNotFoundError:
                    main.logger.error(f"MOVE: FileNotFoundError: {file}")
                except:
                    main.logger.error(f"MOVE: ERROR: Unable to move {file} from {main.os.getcwd()} to {dest_path}")

        elif var_type == "str":
            main.logger.debug(f"MOVE: STARTING: {to_move} to {dest_path}")
            try:
                shutil.move(to_move, dest_path)
                main.logger.debug(f"MOVE: SUCCESS: {to_move} to {dest_path}")
            except shutil.Error:
                main.logger.error(f"MOVE: shutil.Error: {to_move} is already in {dest_path}")
            except FileNotFoundError:
                main.logger.error(f"MOVE: FileNotFoundError: {to_move}")
            except:
                main.logger.error(f"MOVE: ERROR: Unable to move {to_move} from {main.os.getcwd()} to {dest_path}")
    else:
        main.logger.error(f"MOVE: ERROR: {dest_path} does not exists.")

def include(to_include, where_include):
    # adds file or list of files in another list
    main.logger.debug(f"INCLUDE: STARTING")
    to_include_type = get_type(to_include)
    if to_include_type == "list":
        for file in to_include:
            file_type = get_type(file)
            if file_type == "list":
                for subfile in file:
                    where_include.append(subfile)
                    main.logger.debug(f"INCLUDE: SUCCESS: {subfile}")
            elif file_type == "str":
                where_include.append(file)
                main.logger.debug(f"INCLUDE: SUCCESS: {file}")
    elif to_include_type == "str":
        where_include.append(to_include)
        main.logger.debug(f"INCLUDE: SUCCESS: {to_include}")


def remove(to_remove, path, workpath):
    # removes files in current directory
    var_type = get_type(to_remove)
    if var_type == "list":
        for file in to_remove:
            full_path = main.os.path.join(workpath, path, file)
            main.logger.debug(f"REMOVE: STARTING: {full_path}")
            if main.os.path.exists(full_path):
                try:               
                    main.os.remove(file)
                    main.logger.debug(f"REMOVE: SUCCESS: {full_path}")
                except:
                    main.logger.error(f"REMOVE: ERROR: Unable to remove {full_path}")
            else:
                main.logger.error(f"REMOVE: {full_path} does not exists.")
    elif var_type == "str":
        full_path = main.os.path.join(workpath, path, to_remove)
        main.logger.debug(f"REMOVE: STARTING: {full_path}")
        if main.os.path.exists(full_path):
            try:
                main.os.remove(full_path)
                main.logger.debug(f"REMOVE: SUCCESS: {full_path}")
            except:
                main.logger.error(f"REMOVE: ERROR: Unable to remove {full_path} in {main.os.getcwd()}")
        else:
            main.logger.error(f"REMOVE: {full_path} does not exists.")

def rename(renamelist, prefix, need_list_changing=0, backward=0):
    var_type = get_type(renamelist)
    if var_type == "list":
        if backward == 0:
            main.logger.debug(f"RENAME: FORWARD")
            for file in renamelist:
                try:
                    main.logger.debug(f"RENAME: STARTING: {file} to {file}{prefix}")
                    main.os.rename(file, file + prefix)
                    main.logger.debug(f"RENAME: SUCCESS: {file} to {file}{prefix}")
                except FileNotFoundError:
                    main.logger.error(f"RENAME: FileNotFoundError: {file}")
                except FileExistsError:
                    main.logger.error(f"RENAME: FileExistsError: {file}")
                except PermissionError:
                    main.logger.error(f"RENAME: PermissionError: {file}")
                except:
                    main.logger.error(f"RENAME: ERROR: Unable to rename {file} in {main.os.getcwd()}")
            
            if need_list_changing == 1:
                main.logger.debug(f"RENAME: LIST_CHANGING_REQUIRED")
                index = 0
                try:
                    for file in renamelist:
                        main.logger.debug(f"RENAME: LIST_CHANGING: STARTING: {renamelist[index]} to {file}{prefix}")
                        renamelist[index] = file + prefix
                        main.logger.debug(f"RENAME: LIST_CHANGING: SUCCESS: {renamelist[index]} to {file}{prefix}")
                        index += 1
                except:
                    main.logger.error(f"RENAME: LIST_CHANGING: ERROR: {renamelist[index]} to {file}{prefix}")
    
        elif backward == 1:
            main.logger.debug(f"RENAME: BACKWARD")
            for file in renamelist:
                try:
                    main.logger.debug(f"RENAME: STARTING: {file} to {file[0:len(file)-len(prefix)]}")
                    main.os.rename(file, file[0:len(file)-len(prefix)])
                    main.logger.debug(f"RENAME: SUCCESS: {file} to {file[0:len(file)-len(prefix)]}")
                except FileNotFoundError:
                    main.logger.error(f"RENAME: FileNotFoundError: {file}")
                except FileExistsError:
                    main.logger.error(f"RENAME: FileExistsError: {file}")
                except PermissionError:
                    main.logger.error(f"RENAME: PermissionError: {file}")
                except:
                    main.logger.error(f"RENAME: ERROR: Unable to rename {file} in {main.os.getcwd()}")
    elif var_type == "str":
        if backward == 0:
            main.logger.debug(f"RENAME: FORWARD")
            try:
                main.logger.debug(f"RENAME: STARTING: {renamelist} to {renamelist}{prefix}")
                main.os.rename(renamelist, f"{renamelist}{prefix}")
                main.logger.debug(f"RENAME: SUCCESS: {renamelist} to {renamelist}{prefix}")
                new_name = f"{renamelist}{prefix}"
                return new_name
            except FileNotFoundError:
                main.logger.error(f"RENAME: FileNotFoundError: {renamelist}")
            except FileExistsError:
                main.logger.error(f"RENAME: FileExistsError: {renamelist}")
            except PermissionError:
                main.logger.error(f"RENAME: PermissionError: {renamelist}")
            except:
                main.logger.error(f"RENAME: ERROR: Unable to rename {renamelist} in {main.os.getcwd()}")
        elif backward == 1:
            main.logger.debug(f"RENAME: BACKWARD")
            try:
                main.logger.debug(f"RENAME: STARTING: {renamelist} to {renamelist[0:len(renamelist)-len(prefix)]}")
                main.os.rename(renamelist, renamelist[0:len(renamelist)-len(prefix)])
                main.logger.debug(f"RENAME: SUCCESS: {renamelist} to {renamelist[0:len(renamelist)-len(prefix)]}")
                new_name = renamelist[0:len(renamelist)-len(prefix)]
                return new_name
            except FileNotFoundError:
                main.logger.error(f"RENAME: FileNotFoundError: {renamelist}")
            except FileExistsError:
                main.logger.error(f"RENAME: FileExistsError: {renamelist}")
            except PermissionError:
                main.logger.error(f"RENAME: PermissionError: {renamelist}")
            except:
                main.logger.error(f"RENAME: ERROR: Unable to rename {renamelist} in {main.os.getcwd()}")

def randomize(randomizing_list):
    filename = 0
    for file in randomizing_list:
        try:
            main.logger.debug(f"RANDOMIZE_1: STARTING: {file} in {filename}")
            main.os.rename(file, str(filename))
            main.logger.debug(f"RANDOMIZE_1: SUCCESS: {file} in {filename}")
            filename += 1
        except FileNotFoundError:
            main.logger.error(f"RANDOMIZE_1: FileNotFoundError: {file}")
        except FileExistsError:
            main.logger.error(f"RANDOMIZE_1: FileExistsError: {file}")
        except:
            main.logger.error(f"RANDOMIZE_1: ERROR: {file} in {main.os.getcwd()}")
        
    random.shuffle(randomizing_list)

    filename = 0
    for file in randomizing_list:
        try:
            main.logger.debug(f"RANDOMIZE_2: STARTING: {filename} in {file}")
            main.os.rename(str(filename), file)
            main.logger.debug(f"RANDOMIZE_2: SUCCESS: {filename} in {file}")
            filename += 1
        except FileNotFoundError:
            pass
        except FileExistsError:
            main.logger.error(f"RANDOMIZE_2: FileExistsError: {file}")
        except:
            main.logger.error(f"RANDOMIZE_2: ERROR: {file} in {main.os.getcwd()}")

def parse(path_to_file, workpath, file):
    # parses xml
    path = main.os.path.join(workpath, path_to_file, file)
    if main.os.path.exists(path):
        main.logger.debug(f"PARSE: STARTING: {file} in {path}")
        try:
            root = ET.parse(path)
            main.logger.debug(f"PARSE: SUCCESS: {file} in {path}")
            return root
        except PermissionError:
            main.logger.error(f"PARSE: PermissionError: {file} in {path}")
        except:
            main.logger.error(f"PARSE: ERROR: {file} in {path}")
    else:
        main.logger.error(f"PARSE: FileNotFoundError: {file} in {path}")

def write(parsed, file, path, workpath):
    # applies changes to xml with correct encoding
    current_dir(path, workpath)
    main.logger.debug(f"WRITE: STARTING: {file} in {path}")
    backup_file = file[0:len(file)-4] + "_backup.xml"
    main.logger.debug(f"WRITE: BACKUP_FILE: {backup_file}")
    copy(file, path, workpath, backup_file)
    full_path = main.os.path.join(workpath, path, file)
    if main.os.path.exists(full_path):
        try:
            parsed.write(full_path, encoding="windows-1251")
            main.logger.debug(f"WRITE: SUCCESS: {file} in {full_path}")
            remove(backup_file, path, workpath)
            main.logger.debug(f"WRITE: BACKUP_FILE: {backup_file}: REMOVED")
            return True
        except:
            main.logger.error(f"WRITE: ERROR: {file}")
            copy(backup_file, path, workpath, file)
            remove(backup_file, path, workpath)
            main.logger.info(f"WRITE: {file} restored from backup.")
    else:
        main.logger.error(f"WRITE: {full_path} does not exists.")


def turn_on_lua(file, variable, workpath, yaml_file):
    main.logger.debug(f"TURN_ON_LUA: STARTING: {file}:{variable}")
    try:
        lua_path = get_yaml(yaml_file, "LuaRandom", "DestPath")
        dest_path = main.os.path.join(workpath, lua_path, file)
        if dest_path:
            with open (dest_path, "r", encoding="windows-1251") as lua_script:
                old_data = lua_script.read()

            new_data = old_data.replace(f"{variable} = 0", f"{variable} = 1")

            with open (dest_path, "w", encoding="windows-1251") as lua_script:
                lua_script.write(new_data)
            main.logger.info(f"TURN_ON_LUA: SUCCESS: {file}: {variable}")
            return True
        else:
            main.logger.error(f"TURN_ON_LUA: ERROR: {dest_path} does not exists.")
    except:
        main.logger.error(f"TURN_ON_LUA: ERROR: {file}: {variable}")

def generate_color():
    # generating color for durability icon in maingameinterface
    main.logger.debug("GENERATE_COLOR: STARTING")
    random_list = ["fc93e5", "d126ac", "e180db", "c664b1", "c664c3", "df45bd"]
    hex_number = random_list[random.randint(0, len(random_list) - 1)]
    hex_number = "ff" + hex_number
    main.logger.info(f"GENERATE_COLOR: SUCCESS: {hex_number}")
    return hex_number

def show_success(message, mainwindow):
    mainwindow.addMessage(f"{loc_string('Randomizer', 'CompletionMessage')}\n{message}")
    main.logger.info(f"COMPLETED: {message}")

def show_failure(message, mainwindow):
    mainwindow.addMessage(f"{loc_string('Randomizer', 'FailureMessage')}\n{message}")
    main.logger.error(f"FAILURE: {message}")

def loc_string(module, string):
    localized_string = MESSAGES[module][string][LANGUAGE]
    return localized_string

def main_randomizing_start(mainwindow, logger, windowpath, gameversion, workpath, settings, language, messages, exe_version):

    global MESSAGES
    global LANGUAGE

    MESSAGES = messages
    LANGUAGE = language

    critical_stop = 0

    # Adding randomization settings to log
    if settings["Settings"]["DebugMode"] == True:
        main.logger.setLevel(main.logging.DEBUG)
    else:
        main.logger.setLevel(main.logging.INFO)

    log_strings_list = [["Icons", "Maps"], ["Icons", "Digits"], ["Icons", "Splashes"], 
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
    log_settings = settings["Settings"]["Checkboxes"]
            
    logger.info("Starting randomization...")
    logger.info(f"Game path: {workpath}")
    logger.info(f"Game version: {gameversion}")
    logger.info(f"Exe version: {exe_version}")
    logger.info(f"Options:")

    mainwindow.addMessage(f"{loc_string('Randomizer', 'Path')} {workpath}")
    mainwindow.addMessage(f"{loc_string('Randomizer', 'GameVersion')} {gameversion}")
    mainwindow.addMessage(f"{loc_string('Randomizer', 'ExeVersion')} {exe_version}")

    for keys in log_strings_list:
        logger.info(f"{keys[0]} : {keys[1]} = {log_settings[keys[0]][keys[1]]}")
    mainwindow.addMessage(loc_string("Randomizer", "RandomStart"))

    yaml_file = set_yaml(mainwindow, windowpath, gameversion)

    if yaml_file:
        logger.info("Creating mixing folder...")
        try:
            mix_folder_path = yaml_file["MixingDir"]
        except KeyError:
            mainwindow.showPopUp(loc_string("Randomizer", "UnableToCreateFiles"))
            logger.critical(f"Unable to read YAML configuration file. Randomization aborted.")
            mix_folder_path = False
            critical_stop = 1

        if mix_folder_path:
            mix_folder_fullpath = main.os.path.join(workpath, mix_folder_path)

            if main.os.path.exists(mix_folder_fullpath):
                logger.info("Mixing folder already exists. Removing...")
                shutil.rmtree(mix_folder_fullpath)
                logger.info("Mixing folder removed. Creating new one...")
            
            try:
                main.os.mkdir(mix_folder_fullpath)
                logger.info(f"Created mixing folder at {mix_folder_fullpath}")
            except:
                mainwindow.showPopUp(loc_string("Randomizer", "UnableToCreateFiles"))
                critical_stop = 1
    else:
        critical_stop = 1
        
    
    if critical_stop == 0:
        logger.info("Copying lua files...")
        lua_names = get_yaml(yaml_file, "LuaRandom", "Files")
        lua_dest_path = get_yaml(yaml_file, "LuaRandom", "DestPath")
        triggers_path = get_yaml(yaml_file, "LuaRandom", "TriggersDestPath")
        lua_res_path = get_yaml(yaml_file, "LuaRandom", "ResourcesPath")
        names_count = 0

        if current_dir(triggers_path, workpath): # copying triggers to scripts folder
            if copy(lua_names[3], lua_dest_path, workpath):
                if current_dir(lua_res_path, main.os.path.join(windowpath, "resources")):
                    for name in lua_names:
                        logger.info(f"Checking {name}...")
                        with open (f"{main.os.path.join(workpath, lua_dest_path, name)}", "r", encoding="windows-1251") as lua_script:
                            data = lua_script.read()
                            if "rand_guns" in data:
                                logger.info(f"No need to copy {name}. Checking for reload setting...")
                                if settings["Settings"]["RestoreLua"] == True:
                                    logger.info(f"Reload set to true. Reloading...")
                                    if copy(name, lua_dest_path, workpath):
                                        logger.info(f"Reloaded {name} successfully")
                                        if names_count == 3:
                                            mainwindow.addMessage(loc_string("Randomizer", "LuaRestored"))
                                        names_count += 1
                                    else:
                                        critical_stop = 1
                                        logger.critical(f"Unable to copy {name} to {lua_dest_path}. Randomization aborted.")
                                        mainwindow.showPopUp(loc_string("Randomizer", "LuaNotRestored"))
                                        break
                            else:
                                if copy(name, lua_dest_path, workpath):
                                    pass
                                else:
                                    critical_stop = 1
                                    logger.critical(f"Unable to copy {name} to {lua_dest_path}. Randomization aborted.")
                                    mainwindow.showPopUp(loc_string("Randomizer", "UnableToCopyFiles"))
                                    break
                else:
                    critical_stop = 1
                    logger.critical(f"{lua_res_path} is not avaliable. Randomization aborted.")
                    mainwindow.showPopUp(loc_string("Randomizer", "UnableToCopyFiles"))
            else:
                critical_stop = 1
                logger.critical(f"Unable to copy {lua_names[3]}. Randomization aborted.")
                mainwindow.showPopUp(loc_string("Randomizer", "UnableToCopyFiles"))
        else:
            critical_stop = 1
            logger.critical(f"{triggers_path} is not avaliable. Randomization aborted.")
            mainwindow.showPopUp(loc_string("Randomizer", "UnableToCopyFiles"))
    
    if critical_stop == 0:
        if copy_folder(main.os.path.join(windowpath, "resources/data/maps"), main.os.path.join(workpath, "data/maps")):
            if copy_folder(main.os.path.join(windowpath, "resources/data/profiles"), main.os.path.join(workpath, "data/profiles")):
                if gameversion == "ImprovedStoryline":
                    copy_folder(main.os.path.join(windowpath, "resources/data/maps_isl"), main.os.path.join(workpath, "data/maps"))
                if copy(lua_names[3], triggers_path, workpath):
                    mainwindow.addMessage(loc_string("Randomizer", "FilesCopied"))
                    logger.info("Necessary files successfully copied.")
                else:
                    critical_stop = 1
                    logger.critical("Unable to copy necessary files. Randomization aborted.")
                    mainwindow.showPopUp(loc_string("Randomizer", "UnableToCopyFiles"))
            else:
                critical_stop = 1
                logger.critical("Unable to copy necessary files. Randomization aborted.")
                mainwindow.showPopUp(loc_string("Randomizer", "UnableToCopyFiles"))
        else:
            critical_stop = 1
            logger.critical("Unable to copy necessary files. Randomization aborted.")
            mainwindow.showPopUp(loc_string("Randomizer", "UnableToCopyFiles"))

    if critical_stop == 0:
        # Icons: Maps
        if settings["Settings"]["Checkboxes"]["Icons"]["Maps"] == True:
            mixmap_path = get_yaml(yaml_file, "Icons", "Maps", "Path")
            mixmaps_list = get_yaml(yaml_file, "Icons", "Maps", "Files")

            if current_dir(mixmap_path, workpath):
                randomize(mixmaps_list)
                show_success("Icons : Maps", mainwindow)
            else:
                show_failure("Icons : Maps", mainwindow)
        else:
            logger.info("SKIPPED: Icons : Maps")
        
        # Icons: Digits
        if settings["Settings"]["Checkboxes"]["Icons"]["Digits"] == True:
            mixdigits_big_path = get_yaml(yaml_file, "Icons", "Digits", "Large", "Path")
            mixdigits_small_path = get_yaml(yaml_file, "Icons", "Digits", "Small", "Path")
            damageinfo_path = get_yaml(yaml_file, "Icons", "Digits", "Hp_and_fuel_bars", "Path")

            mixdigits_big_list = get_yaml(yaml_file, "Icons", "Digits", "Large", "Files")
            mixdigits_small_list = get_yaml(yaml_file, "Icons", "Digits", "Small", "Files")
            damageinfo_1_name = get_yaml(yaml_file, "Icons", "Digits", "Hp_and_fuel_bars", "Files", 0)
            damageinfo_2_name = get_yaml(yaml_file, "Icons", "Digits", "Hp_and_fuel_bars", "Files", 1)

            # Icons: Digits: Large
            if current_dir(mixdigits_big_path, workpath):
                randomize(mixdigits_big_list)
                show_success("Icons : Digits: Large", mainwindow)
            else:
                show_failure("Icons : Digits: Large", mainwindow)

            # Icons: Digits: Small
            if current_dir(mixdigits_small_path, workpath):
                randomize(mixdigits_small_list)
                show_success("Icons : Digits: Small", mainwindow)
            else:
                show_failure("Icons : Digits: Large", mainwindow)

            # Icons: Digits: Hp_and_fuel_bars
            if get_yaml(yaml_file, "Icons", "Digits", "Hp_and_fuel_bars", "Remove") == True:
                if current_dir(damageinfo_path, workpath):
                    logger.debug("Removing HP and fuel bars...")
                    damageinfo_1 = parse(damageinfo_path, workpath, damageinfo_1_name)
                    if damageinfo_1:
                        damageinfo_1_root = damageinfo_1.getroot()

                        for node in damageinfo_1_root.iter("Node"):
                            if "name" in node.attrib:
                                if any([node.attrib["name"] == "wndHpProgressBar", node.attrib["name"] == "wndFuelProgressBar", 
                                        node.attrib["name"] == "wndLowHpLamp", node.attrib["name"] == "wndLowFuelLamp"]):
                                    node.set("org", "0.000 0.000 0.000 0.000")

                        if write(damageinfo_1, damageinfo_1_name, damageinfo_path, workpath):
                            show_success("Icons : Digits: Hp_and_fuel_bars: File_0", mainwindow)
                        else:
                            show_failure("Icons : Digits: Hp_and_fuel_bars: File_0", mainwindow)
                    else:
                        show_failure("Icons : Digits: Hp_and_fuel_bars: File_0", mainwindow)
                    
                    damageinfo_2 = parse(damageinfo_path, workpath, damageinfo_2_name)
                    if damageinfo_2:
                        damageinfo_2_root = damageinfo_2.getroot()

                        for node in damageinfo_2_root.iter("Node"):
                            if "name" in node.attrib:
                                if any([node.attrib["name"] == "wndHpProgressBar", node.attrib["name"] == "wndFuelProgressBar", 
                                    node.attrib["name"] == "wndLowHpLamp", node.attrib["name"] == "wndLowFuelLamp"]):
                                    node.set("org", "0.000 0.000 0.000 0.000")

                        if write(damageinfo_2, damageinfo_2_name, damageinfo_path, workpath):
                            show_success("Icons : Digits: Hp_and_fuel_bars: File_1", mainwindow)
                        else:
                            show_failure("Icons : Digits: Hp_and_fuel_bars: File_1", mainwindow)
                    else:
                        show_failure("Icons : Digits: Hp_and_fuel_bars: File_1", mainwindow)
            else:
                logger.info("SKIPPED IN YAML: Icons : Digits: Hp_and_fuel_bars")
        else:
            logger.info("SKIPPED: Icons : Digits")
            
        # Icons: Splashes
        if settings["Settings"]["Checkboxes"]["Icons"]["Splashes"] == True:
            mixsplash_path = get_yaml(yaml_file, "Icons", "Splashes", "Path")
            mixsplash_list = get_yaml(yaml_file, "Icons", "Splashes", "Files")

            if current_dir(mixsplash_path, workpath):
                randomize(mixsplash_list)

                show_success("Icons : Splashes", mainwindow)
            else:
                show_failure("Icons : Splashes", mainwindow)
        else:
            logger.info("SKIPPED: Icons : Splashes")
        
        # Icons: DialogsBackground
        if settings["Settings"]["Checkboxes"]["Icons"]["DialogsBackground"] == True:
            mixnpcdiags_path = get_yaml(yaml_file, "Icons", "DialogsBackground", "Path")
            mixnpcdiags_list = get_yaml(yaml_file, "Icons", "DialogsBackground", "Files")

            if current_dir(mixnpcdiags_path, workpath):
                randomize(mixnpcdiags_list)

                show_success("Icons : DialogsBackground", mainwindow)
            else:
                show_failure("Icons : DialogsBackground", mainwindow)
        else:
            logger.info("SKIPPED: Icons : DialogsBackground")
        
        # Icons: Clans
        if settings["Settings"]["Checkboxes"]["Icons"]["Clans"] == True:
            mixclans_path = get_yaml(yaml_file, "Icons", "Clans", "StandaloneIcons", "Path")
            mixclans_logos_path = get_yaml(yaml_file, "Icons", "Clans", "Logos", "Path")

            mixclans_02_list = get_yaml(yaml_file, "Icons", "Clans", "StandaloneIcons", "Files_0")
            mixclans_03_list = get_yaml(yaml_file, "Icons", "Clans", "StandaloneIcons", "Files_1")
            mixclans_logos_list = get_yaml(yaml_file, "Icons", "Clans", "Logos", "Files")

            # Icons: Clans: StandaloneIcons
            if current_dir(mixclans_path, workpath):
                # Icons: Clans: StandaloneIcons: Files_0
                randomize(mixclans_02_list)
                show_success("Icons : Clans : StandaloneIcons : Files_0", mainwindow)

                # Icons: Clans: StandaloneIcons: Files_1
                randomize(mixclans_03_list)
                show_success("Icons : Clans : StandaloneIcons : Files_1", mainwindow)
            else:
                show_failure("Icons : Clans : StandaloneIcons : Files_0", mainwindow)
                show_failure("Icons : Clans : StandaloneIcons : Files_1", mainwindow)
            
            # Icons: Clans: Logos
            if current_dir(mixclans_logos_path, workpath):
                randomize(mixclans_logos_list)
                show_success("Icons : Clans : Logos", mainwindow)
            else:
                show_failure("Icons : Clans : Logos", mainwindow)

        else:
            logger.info("SKIPPED: Icons : Clans")
        
        # Icons: Interface
        if settings["Settings"]["Checkboxes"]["Icons"]["Interface"] == True:

            # Icons: Interface: BrownButtons
            mixmp_action_panel_path = get_yaml(yaml_file, "Icons", "Interface", "BrownButtons", "ActionPanel", "Path")
            mixmp_characteristicswnd_path = get_yaml(yaml_file, "Icons", "Interface", "BrownButtons", "CharacteristicWnd", "Path")
            mixmp_inventorydlg_path = get_yaml(yaml_file, "Icons", "Interface", "BrownButtons", "InventoryDlg", "Path")
            mixmp_workshopdlg_path = get_yaml(yaml_file, "Icons", "Interface", "BrownButtons", "WorkshopDlg", "Path")
            mixmp_motherpanel_path = get_yaml(yaml_file, "Icons", "Interface", "BrownButtons", "MotherPanel", "Path")

            mixmp_action_panel_list = get_yaml(yaml_file, "Icons", "Interface", "BrownButtons", "ActionPanel", "Files")
            mixmp_characteristicswnd_list = get_yaml(yaml_file, "Icons", "Interface", "BrownButtons", "CharacteristicWnd", "Files")
            mixmp_inventorydlg_list = get_yaml(yaml_file, "Icons", "Interface", "BrownButtons", "InventoryDlg", "Files")
            mixmp_workshopdlg_list = get_yaml(yaml_file, "Icons", "Interface", "BrownButtons", "WorkshopDlg", "Files")
            mixmp_motherpanel_list = get_yaml(yaml_file, "Icons", "Interface", "BrownButtons", "MotherPanel", "Files")
            files_to_mix = []

            if current_dir(mixmp_action_panel_path, workpath):
                move(mixmp_action_panel_list, mix_folder_path, workpath)

            if current_dir(mixmp_characteristicswnd_path, workpath):
                move(mixmp_characteristicswnd_list, mix_folder_path, workpath)

            if current_dir(mixmp_inventorydlg_path, workpath):
                move(mixmp_inventorydlg_list, mix_folder_path, workpath)

            if current_dir(mixmp_workshopdlg_path, workpath):
                move(mixmp_workshopdlg_list, mix_folder_path, workpath)

            if current_dir(mixmp_motherpanel_path, workpath):
                move(mixmp_motherpanel_list, mix_folder_path, workpath)

            if current_dir(mix_folder_path, workpath):
                include([mixmp_action_panel_list, mixmp_characteristicswnd_list, mixmp_inventorydlg_list, mixmp_workshopdlg_list, 
                        mixmp_motherpanel_list], files_to_mix)
                randomize(files_to_mix)

                move(mixmp_action_panel_list, mixmp_action_panel_path, workpath)
                move(mixmp_characteristicswnd_list, mixmp_characteristicswnd_path, workpath)
                move(mixmp_inventorydlg_list, mixmp_inventorydlg_path, workpath)
                move(mixmp_workshopdlg_list, mixmp_workshopdlg_path, workpath)
                move(mixmp_motherpanel_list, mixmp_motherpanel_path, workpath), workpath

                show_success("Icons : Interface : BrownButtons", mainwindow)
            else:
                show_failure("Icons : Interface : BrownButtons", mainwindow)

            # Icons: Interface: BossIcons
            mixmp_maingameinterface_path = get_yaml(yaml_file, "Icons", "Interface", "BossIcons", "MainGameInterfaceWnd", "Path")
            mixmp_bossicons_path = get_yaml(yaml_file, "Icons", "Interface", "BossIcons", "BossIndicator", "Path")

            mixmp_maingameinterface_list = get_yaml(yaml_file, "Icons", "Interface", "BossIcons", "MainGameInterfaceWnd", "Files")
            mixmp_bossicons_list = get_yaml(yaml_file, "Icons", "Interface", "BossIcons", "BossIndicator", "Files")
            files_to_mix = []

            if current_dir(mixmp_maingameinterface_path, workpath):
                move(mixmp_maingameinterface_list, mix_folder_path, workpath)

            
            if current_dir(mixmp_bossicons_path, workpath):
                move(mixmp_bossicons_list, mix_folder_path, workpath)

            if current_dir(mix_folder_path, workpath):
                include([mixmp_maingameinterface_list, mixmp_bossicons_list], files_to_mix)
                randomize(files_to_mix)

                move(mixmp_maingameinterface_list, mixmp_maingameinterface_path, workpath)
                move(mixmp_bossicons_list, mixmp_bossicons_path, workpath)

                show_success("Icons : Interface : BossIcons", mainwindow)
            else:
                show_failure("Icons : Interface : BossIcons", mainwindow)
            
            # Icons: Interface: WhiteButtons
            mixmp_questlog_path = get_yaml(yaml_file, "Icons", "Interface", "WhiteButtons", "QuestLog", "Path")
            mixmp_globalmap_path = get_yaml(yaml_file, "Icons", "Interface", "WhiteButtons", "GlobalMap", "Path")
            mixmp_localmap_path = get_yaml(yaml_file, "Icons", "Interface", "WhiteButtons", "LocalMap", "Path")

            mixmp_questlog_list = get_yaml(yaml_file, "Icons", "Interface", "WhiteButtons", "QuestLog", "Files")
            mixmp_globalmap_list = get_yaml(yaml_file, "Icons", "Interface", "WhiteButtons", "GlobalMap", "Files")
            if gameversion == "ImprovedStoryline":
                mixmp_localmap_list = get_yaml(yaml_file, "Icons", "Interface", "WhiteButtons", "LocalMap", "Files", "Group0")
                mixmp_localmap_icons_list = get_yaml(yaml_file, "Icons", "Interface", "WhiteButtons", "LocalMap", "Files", "Group1")
            else:
                mixmp_localmap_list = get_yaml(yaml_file, "Icons", "Interface", "WhiteButtons", "LocalMap", "Files")
            files_to_mix = []

            if current_dir(mixmp_questlog_path, workpath):
                move(mixmp_questlog_list, mix_folder_path, workpath)

            
            if current_dir(mixmp_globalmap_path, workpath):
                move(mixmp_globalmap_list, mix_folder_path, workpath)

            
            if current_dir(mixmp_localmap_path, workpath):
                move(mixmp_localmap_list, mix_folder_path, workpath)

                if gameversion == "ImprovedStoryline":
                    randomize(mixmp_localmap_icons_list)

                    show_success("Icons : Interface : WhiteButtons : Icons", mainwindow)
            else:
                if gameversion == "ImprovedStoryline":
                    show_failure("Icons : Interface : WhiteButtons : Icons", mainwindow)

            if current_dir(mix_folder_path, workpath):
                include([mixmp_questlog_list, mixmp_globalmap_list, mixmp_localmap_list], files_to_mix)
                randomize(files_to_mix)

                move(mixmp_questlog_list, mixmp_questlog_path, workpath)
                move(mixmp_globalmap_list, mixmp_globalmap_path, workpath)
                move(mixmp_localmap_list, mixmp_localmap_path, workpath)

                show_success("Icons : Interface : WhiteButtons", mainwindow)
            else:
                show_failure("Icons : Interface : WhiteButtons", mainwindow)
            
            # Icons: Interface: GlobalMap
            mixmp_globalmap_1_path = get_yaml(yaml_file, "Icons", "Interface", "GlobalMap", "Path")
            mixmp_globalmap_1_list = get_yaml(yaml_file, "Icons", "Interface", "GlobalMap", "Files")

            if current_dir(mixmp_globalmap_1_path, workpath):
                randomize(mixmp_globalmap_1_list)
                show_success("Icons : Interface : GlobalMap", mainwindow)
            else:
                show_failure("Icons : Interface : GlobalMap", mainwindow)
            
            # Icons: Interface: MainMenuButtons
            mixmp_mainmenu_path = get_yaml(yaml_file, "Icons", "Interface", "MainMenuButtons", "Path")
            mixmp_mainmenu_list = get_yaml(yaml_file, "Icons", "Interface", "MainMenuButtons", "Files")

            if current_dir(mixmp_mainmenu_path, workpath):
                randomize(mixmp_mainmenu_list)
                show_success("Icons : Interface : MainMenuButtons", mainwindow)
            else:
                show_failure("Icons : Interface : MainMenuButtons", mainwindow)
            
            # Icons: Interface: WeaponGroups
            mixmp_weapongroupbuttons_path = get_yaml(yaml_file, "Icons", "Interface", "WeaponGroups", "Path")
            mixmp_weapongroupbuttons_list = get_yaml(yaml_file, "Icons", "Interface", "WeaponGroups", "Files")

            if current_dir(mixmp_weapongroupbuttons_path, workpath):
                randomize(mixmp_weapongroupbuttons_list)
                show_success("Icons : Interface : WeaponGroups", mainwindow)
            else:
                show_failure("Icons : Interface : WeaponGroups", mainwindow)
            
            # Icons: Interface: WeaponSlots
            mixmp_weaponslots_path = get_yaml(yaml_file, "Icons", "Interface", "WeaponSlots", "Path")
            mixmp_weaponslots_list = get_yaml(yaml_file, "Icons", "Interface", "WeaponSlots", "Files")

            if current_dir(mixmp_weaponslots_path, workpath):
                randomize(mixmp_weaponslots_list)
                show_success("Icons : Interface : WeaponSlots", mainwindow)
            else:
                show_failure("Icons : Interface : WeaponSlots", mainwindow)
            
            # Icons: Interface: ShopIcons
            mixmp_shop_path = get_yaml(yaml_file, "Icons", "Interface", "ShopIcons", "Path")

            mixmp_shop_list_1 = get_yaml(yaml_file, "Icons", "Interface", "ShopIcons", "Files_0")
            mixmp_shop_list_2 = get_yaml(yaml_file, "Icons", "Interface", "ShopIcons", "Files_1")

            if current_dir(mixmp_shop_path, workpath):
                randomize(mixmp_shop_list_1)
                randomize(mixmp_shop_list_2)
                show_success("Icons : Interface : ShopIcons", mainwindow)
            else:
                show_failure("Icons : Interface : ShopIcons", mainwindow)
        else:
            logger.info("SKIPPED: Icons : Interface")
        
        # Icons: Radar
        if settings["Settings"]["Checkboxes"]["Icons"]["Radar"] == True:
            mixradar_localmap_path = get_yaml(yaml_file, "Icons", "Radar", "LocalMap", "Path")
            mixradar_questlog_path = get_yaml(yaml_file, "Icons", "Radar", "QuestLog", "Path")
            mixradar_path = get_yaml(yaml_file, "Icons", "Radar", "RadarWnd", "Path")

            mixradar_localmap_list = get_yaml(yaml_file, "Icons", "Radar", "LocalMap", "Files")
            mixradar_questlog_list = get_yaml(yaml_file, "Icons", "Radar", "QuestLog", "Files")
            mixradar_list = get_yaml(yaml_file, "Icons", "Radar", "RadarWnd", "Files")
            files_to_mix = []

            if current_dir(mixradar_localmap_path, workpath):
                move(mixradar_localmap_list, mix_folder_path, workpath)

            if current_dir(mixradar_questlog_path, workpath):
                move(mixradar_questlog_list, mix_folder_path, workpath)

            if current_dir(mixradar_path, workpath):
                move(mixradar_list, mix_folder_path, workpath)

            if current_dir(mix_folder_path, workpath):
                include([mixradar_localmap_list, mixradar_questlog_list, mixradar_list], files_to_mix)
                randomize(files_to_mix)

                move(mixradar_localmap_list, mixradar_localmap_path, workpath)
                move(mixradar_questlog_list, mixradar_questlog_path, workpath)
                move(mixradar_list, mixradar_path, workpath)

                show_success("Icons : Radar", mainwindow)
            else:
                show_failure("Icons : Radar", mainwindow)
        else:
            logger.info("SKIPPED: Icons : Radar")
        
        # Icons: GunsAndWares
        if settings["Settings"]["Checkboxes"]["Icons"]["GunsAndWares"] == True:
            mixwares_goods_path = get_yaml(yaml_file, "Icons", "GunsAndWares", "Goods", "Path")
            mixwares_weapon_path = get_yaml(yaml_file, "Icons", "GunsAndWares", "Weapon", "Path")
            mixwares_path = get_yaml(yaml_file, "Icons", "GunsAndWares", "Gadgets", "Path")

            if gameversion == "Steam":
                mixwares_weapon_list = get_yaml(yaml_file, "Icons", "GunsAndWares", "Weapon", "Files")
            elif gameversion == "CommunityRemaster":
                mixwares_weapon_0_list = get_yaml(yaml_file, "Icons", "GunsAndWares", "Weapon", "Files", "Group0")
                mixwares_weapon_1_list = get_yaml(yaml_file, "Icons", "GunsAndWares", "Weapon", "Files", "Group1")

            mixwares_goods_list = get_yaml(yaml_file, "Icons", "GunsAndWares", "Goods", "Files")
            mixwares_list = get_yaml(yaml_file, "Icons", "GunsAndWares", "Gadgets", "Files")
            files_to_mix = []

            if current_dir(mixwares_goods_path, workpath):
                move(mixwares_goods_list, mix_folder_path, workpath)

            if current_dir(mixwares_weapon_path, workpath):
                if gameversion == "Steam":
                    move(mixwares_weapon_list, mix_folder_path, workpath)
                elif gameversion == "CommunityRemaster":
                    move(mixwares_weapon_0_list, mix_folder_path, workpath)
                    move(mixwares_weapon_1_list, mix_folder_path, workpath)

            if current_dir(mixwares_path, workpath):
                move(mixwares_list, mix_folder_path, workpath)
            
            if current_dir(mix_folder_path, workpath):
                if gameversion == "Steam":
                    include([mixwares_goods_list, mixwares_weapon_list, mixwares_list], files_to_mix)
                elif gameversion == "CommunityRemaster":
                    include([mixwares_goods_list, mixwares_weapon_0_list, mixwares_weapon_1_list, mixwares_list], files_to_mix)

                randomize(files_to_mix)

                move(mixwares_goods_list, mixwares_goods_path, workpath)
                if gameversion == "Steam":
                    move(mixwares_weapon_list, mixwares_weapon_path, workpath)
                elif gameversion == "CommunityRemaster":
                    move(mixwares_weapon_0_list, mixwares_weapon_path, workpath)
                    move(mixwares_weapon_1_list, mixwares_weapon_path, workpath)

                move(mixwares_list, mixwares_path, workpath)

                show_success("Icons : GunsAndWares", mainwindow)
            else:
                show_failure("Icons : GunsAndWares", mainwindow)
        else:
            logger.info("SKIPPED: Icons : GunsAndWares")
        
        # Icons: CabinsAndBaskets
        if settings["Settings"]["Checkboxes"]["Icons"]["CabinsAndBaskets"] == True:
            mixcab_bug_path = get_yaml(yaml_file, "Icons", "CabinsAndBaskets", "Bug", "Path")
            mixcab_molokovoz_path = get_yaml(yaml_file, "Icons", "CabinsAndBaskets", "Molokovoz", "Path")
            mixcab_mirotvorec_path = get_yaml(yaml_file, "Icons", "CabinsAndBaskets", "Mirotvorec", "Path")
            mixcab_ural_path = get_yaml(yaml_file, "Icons", "CabinsAndBaskets", "Ural", "Path")
            mixcab_belaz_path = get_yaml(yaml_file, "Icons", "CabinsAndBaskets", "Belaz", "Path")

            mixcab_bug_list = get_yaml(yaml_file, "Icons", "CabinsAndBaskets", "Bug", "Files")
            mixcab_molokovoz_list = get_yaml(yaml_file, "Icons", "CabinsAndBaskets", "Molokovoz", "Files")
            mixcab_mirotvorec_list = get_yaml(yaml_file, "Icons", "CabinsAndBaskets", "Mirotvorec", "Files")
            mixcab_ural_list = get_yaml(yaml_file, "Icons", "CabinsAndBaskets", "Ural", "Files")
            mixcab_belaz_list = get_yaml(yaml_file, "Icons", "CabinsAndBaskets", "Belaz", "Files")
            files_to_mix = []

            if current_dir(mixcab_bug_path, workpath):
                move(mixcab_bug_list, mix_folder_path, workpath)

            if current_dir(mixcab_molokovoz_path, workpath):
                move(mixcab_molokovoz_list, mix_folder_path, workpath)

            if current_dir(mixcab_mirotvorec_path, workpath):
                move(mixcab_mirotvorec_list, mix_folder_path, workpath)

            if current_dir(mixcab_ural_path, workpath):
                move(mixcab_ural_list, mix_folder_path, workpath)

            if current_dir(mixcab_belaz_path, workpath):
                move(mixcab_belaz_list, mix_folder_path, workpath)
            
            if current_dir(mix_folder_path, workpath):
                include([mixcab_bug_list, mixcab_molokovoz_list, mixcab_mirotvorec_list, mixcab_ural_list, mixcab_belaz_list], files_to_mix)
                randomize(files_to_mix)

                move(mixcab_bug_list, mixcab_bug_path, workpath)
                move(mixcab_molokovoz_list, mixcab_molokovoz_path, workpath)
                move(mixcab_mirotvorec_list, mixcab_mirotvorec_path, workpath)
                move(mixcab_ural_list, mixcab_ural_path, workpath)
                move(mixcab_belaz_list, mixcab_belaz_path, workpath)

                show_success("Icons : CabinsAndBaskets", mainwindow)
            else:
                show_failure("Icons : CabinsAndBaskets", mainwindow)
        else:
            logger.info("SKIPPED: Icons : CabinsAndBaskets")
        
        # Icons: Smartcursor
        if settings["Settings"]["Checkboxes"]["Icons"]["Smartcursor"] == True:
            mixsmart_path = get_yaml(yaml_file, "Icons", "Smartcursor", "Path")
            if gameversion == "CommunityRemaster":
                mixsmart_copy_path = get_yaml(yaml_file, "Icons", "Smartcursor", "ToCopy")
            mixsmart_list = get_yaml(yaml_file, "Icons", "Smartcursor", "Files")

            if current_dir(mixsmart_path, workpath):
                randomize(mixsmart_list)

                if gameversion == "CommunityRemaster":
                    copy(["cross1.dds", "small_cross.dds"], mixsmart_copy_path, workpath)

                show_success("Icons : Smartcursor", mainwindow)
            else:
                show_failure("Icons : Smartcursor", mainwindow)
        else:
            logger.info("SKIPPED: Icons : Smartcursor")
        
        # Text: Names
        if settings["Settings"]["Checkboxes"]["Text"]["Names"] == True:

            # Text: Names: Affixesdiz
            affixesdiz_file = get_yaml(yaml_file, "Text", "Names", "Affixesdiz", "File")
            affixesdiz_path = get_yaml(yaml_file, "Text", "Names", "Affixesdiz", "Path")
            
            affixesdiz = parse(affixesdiz_path, workpath, affixesdiz_file)
            if affixesdiz:
                affixesdiz_root = affixesdiz.getroot()
                affixesdiz_strings = affixesdiz_root.findall("string")
                affixesdiz_values_names = []

                for value in affixesdiz_strings:
                    if "value" in value.attrib and "id" in value.attrib:
                        attrib = value.attrib["id"]
                        if attrib[(len(attrib) - 3):len(attrib)] != "diz":
                            affixesdiz_values_names.append(value.attrib["value"])

                random.shuffle(affixesdiz_values_names)

                pl = 0
                for value in affixesdiz_strings:
                    if "value" in value.attrib and "id" in value.attrib:
                        attrib = value.attrib["id"]
                        if attrib[(len(attrib) - 3):len(attrib)] != "diz":
                            value.set("value", affixesdiz_values_names[pl])
                            pl += 1

                if write(affixesdiz, affixesdiz_file, affixesdiz_path, workpath):
                    show_success("Text : Names : Affixesdiz", mainwindow)
                else:
                    show_failure("Text : Names : Affixesdiz", mainwindow)
            else:
                show_failure("Icons : Digits: Hp_and_fuel_bars: File_1", mainwindow)

            # Text: Names: Clansdiz (abbs)
            clansdiz_file = get_yaml(yaml_file, "Text", "Names", "Clansdiz", "File")
            clansdiz_path = get_yaml(yaml_file, "Text", "Names", "Clansdiz", "Path")
            clansdiz = parse(clansdiz_path, workpath, clansdiz_file)
            if clansdiz:
                clansdiz_root = clansdiz.getroot()
                clansdiz_strings = clansdiz_root.findall("string")
                all_names_list = []
                clansdiz_abbs = []

                for value in clansdiz_strings:
                    if "value" in value.attrib and "id" in value.attrib:
                        attrib = value.attrib["id"]
                        if attrib[(len(attrib) - 3):len(attrib)] == "abb":
                            clansdiz_abbs.append(value.attrib["value"])
                        elif attrib[(len(attrib) - 3):len(attrib)] != "diz":
                            all_names_list.append(value.attrib["value"])

                random.shuffle(clansdiz_abbs)

                pl = 0
                for value in clansdiz_strings:
                    if "value" in value.attrib and "id" in value.attrib:
                        attrib = value.attrib["id"]
                        if attrib[(len(attrib) - 3):len(attrib)] == "abb":
                            value.set("value", clansdiz_abbs[pl])
                            pl += 1

                if write(clansdiz, clansdiz_file, clansdiz_path, workpath):     
                    show_success("Text : Names : Clansdiz (abbs)", mainwindow)
                else:
                    show_failure("Text : Names : Clansdiz (abbs)", mainwindow)
            else:
                show_failure("Text : Names : Clansdiz (abbs)", mainwindow)

            # Text: Names: Clansdiz (names); ObjectNames; ModelNames; LevelInfo; UiBooks; Help
            maps_folders_path = get_yaml(yaml_file, "Text", "Names", "ObjectNames", "Paths")
            object_names_file = get_yaml(yaml_file, "Text", "Names", "ObjectNames", "File")

            for path in maps_folders_path:
                object_names = parse(path, workpath, object_names_file)
                if object_names:
                    object_names_root = object_names.getroot()
                    object_names_objects = object_names_root.findall("Object")

                    for FullName in object_names_objects:
                        if "FullName" in FullName.attrib:
                            if FullName.attrib["FullName"] != "" and FullName.attrib["FullName"] != "Дот" and FullName.attrib["FullName"] != "Pillbox":
                                all_names_list.append(FullName.attrib["FullName"])
            
            model_names_file = get_yaml(yaml_file, "Text", "Names", "ModelNames", "File")
            model_names_path = get_yaml(yaml_file, "Text", "Names", "ModelNames", "Path")
            model_names_tree = parse(model_names_path, workpath, model_names_file)

            if model_names_tree:
                for value in model_names_tree.findall("Item"):
                    if "value" in value.attrib:
                        all_names_list.append(value.attrib["value"])

            levelinfo_file = get_yaml(yaml_file, "Text", "Names", "LevelInfo", "File")
            levelinfo_path = get_yaml(yaml_file, "Text", "Names", "LevelInfo", "Path")
            levelinfo_tree = parse(levelinfo_path, workpath, levelinfo_file)

            if levelinfo_tree:
                for fullName in levelinfo_tree.findall("LevelInfo"):
                    if "fullName" in fullName.attrib and "name" in fullName.attrib:
                        if fullName.attrib["name"] != "mainmenu" and fullName.attrib["name"] != "t":
                            all_names_list.append(fullName.attrib["fullName"])
            
            uibooks_file = get_yaml(yaml_file, "Text", "Names", "UiBooks", "File")
            uibooks_path = get_yaml(yaml_file, "Text", "Names", "UiBooks", "Path")
            uibooks_tree = parse(uibooks_path, workpath, uibooks_file)

            if uibooks_tree:
                for value in uibooks_tree.findall("string"):
                    if "value" in value.attrib and "id" in value.attrib:
                        attrib = value.attrib["id"]
                        if attrib[(len(attrib) - 3):len(attrib)] != "diz" and value.attrib["value"] != "":
                            all_names_list.append(value.attrib["value"])
            
            help_file = get_yaml(yaml_file, "Text", "Names", "Help", "File")
            help_path = get_yaml(yaml_file, "Text", "Names", "Help", "Path")
            help_root = parse(help_path, workpath, help_file)

            if help_root:
                for value in help_root.findall("string"):
                    if "value" in value.attrib and "id" in value.attrib:
                        attrib = value.attrib["id"]
                        if attrib[(len(attrib) - 5):len(attrib)] == "title":
                            all_names_list.append(value.attrib["value"])

            random.shuffle(all_names_list)

            pl = 0
            if clansdiz:
                for value in clansdiz_strings:
                    if "value" in value.attrib and "id" in value.attrib:
                        attrib = value.attrib["id"]
                        if attrib[(len(attrib) - 3):len(attrib)] != "abb" and attrib[(len(attrib) - 3):len(attrib)] != "diz":
                            value.set("value", all_names_list[pl])
                            pl += 1
            
                if write(clansdiz, clansdiz_file, clansdiz_path, workpath):
                    show_success("Text : Names : Clansdiz (names)", mainwindow)
                else:
                    show_failure("Text : Names : Clansdiz (names)", mainwindow)
            else:
                show_failure("Text : Names : Clansdiz (names)", mainwindow)

            for path in maps_folders_path:
                object_names_tree = parse(path, workpath,  "object_names.xml")
                if object_names_tree:
                    for FullName in object_names_tree.findall("Object"):
                        if "FullName" in FullName.attrib:
                            if FullName.attrib["FullName"] != "" and FullName.attrib["FullName"] != "Дот" and FullName.attrib["FullName"] != "Pillbox":
                                FullName.set("FullName", all_names_list[pl])
                                pl += 1
                    if write(object_names_tree, object_names_file, path, workpath):
                        show_success(f"Text : Names : ObjectNames ({path[len(path)-5:len(path)-1]})", mainwindow)
                    else:
                        show_failure(f"Text : Names : ObjectNames ({path[len(path)-5:len(path)-1]})", mainwindow)
                else:
                    show_failure(f"Text : Names : ObjectNames ({path[len(path)-5:len(path)-1]})", mainwindow)

            if model_names_tree:
                for value in model_names_tree.findall("Item"):
                    if "value" in value.attrib:
                        value.set("value", all_names_list[pl])
                        pl += 1

                if write(model_names_tree, model_names_file, model_names_path, workpath):
                    show_success("Text : Names : ModelNames", mainwindow)
                else:
                    show_failure("Text : Names : ModelNames", mainwindow)
            else:
                show_failure("Text : Names : ModelNames", mainwindow)

            if levelinfo_tree:
                for fullName in levelinfo_tree.findall("LevelInfo"):
                    if "fullName" in fullName.attrib and "name" in fullName.attrib:
                        if fullName.attrib["name"] != "mainmenu" and fullName.attrib["name"] != "t":
                            fullName.set("fullName", all_names_list[pl])
                            pl += 1
            
                if write(levelinfo_tree, levelinfo_file, levelinfo_path, workpath):
                    show_success("Text : Names : LevelInfo", mainwindow)
                else:
                    show_failure("Text : Names : LevelInfo", mainwindow)
            else:
                show_failure("Text : Names : LevelInfo", mainwindow)

            if uibooks_tree:
                for value in uibooks_tree.findall("string"):
                    if "value" in value.attrib and "id" in value.attrib:
                        attrib = value.attrib["id"]
                        if attrib[(len(attrib) - 3):len(attrib)] != "diz" and value.attrib["value"] != "":
                            value.set("value", all_names_list[pl])
                            pl += 1
            
                if write(uibooks_tree, uibooks_file, uibooks_path, workpath):
                    show_success("Text : Names : UiBooks", mainwindow)
                else:
                    show_failure("Text : Names : UiBooks", mainwindow)
            else:
                show_failure("Text : Names : UiBooks", mainwindow)

            if help_root:
                for value in help_root.findall("string"):
                    if "value" in value.attrib and "id" in value.attrib:
                        attrib = value.attrib["id"]
                        if attrib[(len(attrib) - 5):len(attrib)] == "title":
                            value.set("value", all_names_list[pl])
                            pl += 1

                if write(help_root, help_file, help_path, workpath):
                    show_success("Text : Names : Help", mainwindow)
                else:
                    show_failure("Text : Names : Help", mainwindow)
            else:
                show_failure("Text : Names : Help", mainwindow)
        else:
            logger.info("SKIPPED: Text : Names")
        
        # Text: Dialogs
        if settings["Settings"]["Checkboxes"]["Text"]["Dialogs"] == True:
            
            # Text: Dialogs: DialogsGlobal
            dialogsglobal_file = get_yaml(yaml_file, "Text", "Dialogs", "DialogsGlobal", "File")
            dialogsglobal_path = get_yaml(yaml_file, "Text", "Dialogs", "DialogsGlobal", "Path")
            dialogsglobal_tree = parse(dialogsglobal_path, workpath, dialogsglobal_file)

            all_dialogs_list = []

            if dialogsglobal_tree:
                for text in dialogsglobal_tree.findall("Reply"):
                    if "text" in text.attrib:
                        all_dialogs_list.append(text.attrib["text"])
            
            # Text: Dialogs: DynamicDialogsGlobal
            dynamicdialogsglobal_file = get_yaml(yaml_file, "Text", "Dialogs", "DynamicDialogsGlobal", "File")
            dynamicdialogsglobal_path = get_yaml(yaml_file, "Text", "Dialogs", "DynamicDialogsGlobal", "Path")
            dynamicdialogsglobal_tree = parse(dynamicdialogsglobal_path, workpath, dynamicdialogsglobal_file)

            if dynamicdialogsglobal_tree:
                for text in dynamicdialogsglobal_tree.findall("Reply"):
                    if "text" in text.attrib:
                        all_dialogs_list.append(text.attrib["text"])
            
            random.shuffle(all_dialogs_list)

            pl = 0
            if dialogsglobal_tree:
                for text in dialogsglobal_tree.findall("Reply"):
                    if "text" in text.attrib:
                        text.set("text", all_dialogs_list[pl])
                    pl += 1

                if write(dialogsglobal_tree, dialogsglobal_file, dialogsglobal_path, workpath):
                    show_success("Text : Dialogs : DialogsGlobal", mainwindow)
                else:
                    show_failure("Text : Dialogs : DialogsGlobal", mainwindow)
            else:
                show_failure("Text : Dialogs : DialogsGlobal", mainwindow)

            if dynamicdialogsglobal_tree:
                for text in dynamicdialogsglobal_tree.findall("Reply"):
                    text.set("text", all_dialogs_list[pl])
                    pl += 1

                if write(dynamicdialogsglobal_tree, dynamicdialogsglobal_file, dynamicdialogsglobal_path, workpath):
                    show_success("Text : Dialogs : DynamicDialogsGlobal", mainwindow)
                else:
                    show_failure("Text : Dialogs : DynamicDialogsGlobal", mainwindow)
            else:
                show_failure("Text : Dialogs : DynamicDialogsGlobal", mainwindow)

            # Text: Dialogs: Strings
            maps_folders_path = get_yaml(yaml_file, "Text", "Dialogs", "Strings", "Paths")
            strings_file = get_yaml(yaml_file, "Text", "Dialogs", "Strings", "File")
            strings_list = []

            for path in maps_folders_path:
                strings_root = parse(path, workpath, strings_file)
                if strings_root:
                    for value in strings_root.findall("string"):
                        if "value" in value.attrib:
                            if value.attrib["value"] != "":
                                strings_list.append(value.attrib["value"])
            
            random.shuffle(strings_list)

            pl = 0
            for path in maps_folders_path:
                strings_root = parse(path, workpath, "strings.xml")
                if strings_root:
                    for value in strings_root.findall("string"):
                        if "value" in value.attrib:
                            if value.attrib["value"] != "":
                                value.set("value", strings_list[pl])
                                pl += 1

                    if write(strings_root, strings_file, path, workpath):
                        show_success(f"Text : Dialogs : Strings ({path[len(path)-5:len(path)-1]})", mainwindow)
                    else:
                        show_failure(f"Text : Dialogs : Strings ({path[len(path)-5:len(path)-1]})", mainwindow)
                else:
                    show_failure(f"Text : Dialogs : Strings ({path[len(path)-5:len(path)-1]})", mainwindow)
        else:
            logger.info("SKIPPED: Text : Dialogs")
        
        # Text: QuestInfoGlobal
        if settings["Settings"]["Checkboxes"]["Text"]["QuestInfoGlobal"] == True:
            questinfoglobal_file = get_yaml(yaml_file, "Text", "QuestInfoGlobal", "File")
            questinfoglobal_path = get_yaml(yaml_file, "Text", "QuestInfoGlobal", "Path")
            questinfoglobal_root = parse(questinfoglobal_path, workpath, questinfoglobal_file)
            questinfoglobal_briefdiz_list = []
            questinfoglobal_fulldiz_list = []

            if questinfoglobal_root:
                for briefDiz in questinfoglobal_root.findall("QuestInfo"):
                    if "briefDiz" in briefDiz.attrib:        
                        questinfoglobal_briefdiz_list.append(briefDiz.attrib["briefDiz"])

                for fullDiz in questinfoglobal_root.findall("QuestInfo"):
                    if "fullDiz" in fullDiz.attrib:            
                        questinfoglobal_fulldiz_list.append(fullDiz.attrib["fullDiz"])

                random.shuffle(questinfoglobal_briefdiz_list)
                random.shuffle(questinfoglobal_fulldiz_list)

                pl = 0
                for briefDiz in questinfoglobal_root.findall("QuestInfo"):
                    if "briefDiz" in briefDiz.attrib:        
                        briefDiz.set("briefDiz", questinfoglobal_briefdiz_list[pl])
                        pl += 1
                pl = 0
                for fullDiz in questinfoglobal_root.findall("QuestInfo"):
                    if "fullDiz" in fullDiz.attrib:            
                        fullDiz.set("fullDiz", questinfoglobal_fulldiz_list[pl])
                        pl += 1

                if write(questinfoglobal_root, questinfoglobal_file, questinfoglobal_path, workpath):
                    show_success("Text : QuestInfoGlobal", mainwindow)
                else:
                    show_failure("Text : QuestInfoGlobal", mainwindow)
            else:
                show_failure("Text : QuestInfoGlobal", mainwindow)
        else:
            logger.info("SKIPPED: Text : QuestInfoGlobal")

        # Text: BindNames
        if settings["Settings"]["Checkboxes"]["Text"]["BindNames"] == True:
            bindnames_file = get_yaml(yaml_file, "Text", "BindNames", "File")
            bindnames_path = get_yaml(yaml_file, "Text", "BindNames", "Path")
            bindnames_root = parse(bindnames_path, workpath, bindnames_file)

            bindnames_list = []

            if bindnames_root:
                for value in bindnames_root.findall("string"):
                    if "value" in value.attrib:
                        if value.attrib["value"] != "":
                            bindnames_list.append(value.attrib["value"])

                random.shuffle(bindnames_list)

                pl = 0
                for value in bindnames_root.findall("string"):
                    if "value" in value.attrib:
                        if value.attrib["value"] != "":
                            value.set("value", bindnames_list[pl])
                            pl += 1

                if write(bindnames_root, bindnames_file, bindnames_path, workpath):
                    show_success("Text : BindNames", mainwindow)
                else:
                    show_failure("Text : BindNames", mainwindow)
            else:
                show_failure("Text : BindNames", mainwindow)
        else:
            logger.info("SKIPPED: Text : BindNames")
        
        # Text: FadingMsgs
        if settings["Settings"]["Checkboxes"]["Text"]["FadingMsgs"] == True:
            fadingmsgs_file = get_yaml(yaml_file, "Text", "FadingMsgs", "FadingMsgs", "File")
            fadingmsgs_path = get_yaml(yaml_file, "Text", "FadingMsgs", "FadingMsgs", "Path")
            fadingmsgs_root = parse(fadingmsgs_path, workpath, fadingmsgs_file)

            radiosamples_file = get_yaml(yaml_file, "Text", "FadingMsgs", "RadioSamples", "File")
            radiosamples_path = get_yaml(yaml_file, "Text", "FadingMsgs", "RadioSamples", "Path")
            radiosamples_root = parse(radiosamples_path, workpath, radiosamples_file)

            fadingmsgs_list = []

            if fadingmsgs_root:
                for value in fadingmsgs_root.findall("string"):
                    if "value" in value.attrib:
                        fadingmsgs_list.append(value.attrib["value"])
            
            if radiosamples_root:
                for text in radiosamples_root.findall("Sample"):
                    if "text" in text.attrib:
                        fadingmsgs_list.append(text.attrib["text"])

            random.shuffle(fadingmsgs_list)

            pl = 0
            if fadingmsgs_root:
                for value in fadingmsgs_root.findall("string"):
                    if "value" in value.attrib:
                        value.set("value", fadingmsgs_list[pl])
                        pl += 1
                
                if write(fadingmsgs_root, fadingmsgs_file, fadingmsgs_path, workpath):
                    show_success("Text : FadingMsgs : FadingMsgs", mainwindow)
                else:
                    show_failure("Text : FadingMsgs : FadingMsgs", mainwindow)
            else:
                show_failure("Text : FadingMsgs : FadingMsgs", mainwindow)
            
            if radiosamples_root:
                for text in radiosamples_root.findall("Sample"):
                    if "text" in text.attrib:
                        text.set("text", fadingmsgs_list[pl])
                        pl += 1

                if write(radiosamples_root, radiosamples_file, radiosamples_path, workpath):
                    show_success("Text : FadingMsgs : RadioSamples", mainwindow)
                else:
                    show_failure("Text : FadingMsgs : RadioSamples", mainwindow)
            else:
                show_failure("Text : FadingMsgs : RadioSamples", mainwindow)
        else:
            logger.info("SKIPPED: Text : FadingMsgs")
        
        # Text: Interface
        if settings["Settings"]["Checkboxes"]["Text"]["Interface"] == True:
            gamestrings_file = get_yaml(yaml_file, "Text", "Interface", "GameStrings", "File")
            gamestrings_path = get_yaml(yaml_file, "Text", "Interface", "GameStrings", "Path")
            gamestrings_root = parse(gamestrings_path, workpath, gamestrings_file)

            uieditstrings_file = get_yaml(yaml_file, "Text", "Interface", "UiEditStrings", "File")
            uieditstrings_path = get_yaml(yaml_file, "Text", "Interface", "UiEditStrings", "Path")
            uieditstrings_root = parse(uieditstrings_path, workpath, uieditstrings_file)

            statistics_file = get_yaml(yaml_file, "Text", "Interface", "Statistics", "File")
            statistics_path = get_yaml(yaml_file, "Text", "Interface", "Statistics", "Path")
            statistics_root = parse(statistics_path, workpath, statistics_file)

            interface_text_list = []

            if gamestrings_root:
                for value in gamestrings_root.findall("string"):
                    if "value" in value.attrib:
                        interface_text_list.append(value.attrib["value"])

            if uieditstrings_root:
                for value in uieditstrings_root.findall("string"):
                    if "value" in value.attrib:
                        interface_text_list.append(value.attrib["value"])

            if statistics_root:
                for value in statistics_root.findall("string"):
                    if "value" in value.attrib:
                        interface_text_list.append(value.attrib["value"])

            random.shuffle(interface_text_list)

            pl = 0
            if gamestrings_root:
                for value in gamestrings_root.findall("string"):
                    if "value" in value.attrib:
                        value.set("value", interface_text_list[pl])
                        pl += 1
                
                if write(gamestrings_root, gamestrings_file, gamestrings_path, workpath):
                    show_success("Text : Interface : GameStrings", mainwindow)
                else:
                    show_failure("Text : Interface : GameStrings", mainwindow)
            else:
                show_failure("Text : Interface : GameStrings", mainwindow)

            if uieditstrings_root:
                for value in uieditstrings_root.findall("string"):
                    if "value" in value.attrib:
                        value.set("value", interface_text_list[pl])
                        pl += 1
                
                if write(uieditstrings_root, uieditstrings_file, uieditstrings_path, workpath):
                    show_success("Text : Interface : UiEditStrings", mainwindow)
                else:
                    show_failure("Text : Interface : UiEditStrings", mainwindow)
            else:
                show_failure("Text : Interface : UiEditStrings", mainwindow)

            if statistics_root:
                for value in statistics_root.findall("string"):
                    if "value" in value.attrib:
                        value.set("value", interface_text_list[pl])
                        pl += 1
                
                if write(statistics_root, statistics_file, statistics_path, workpath):
                    show_success("Text : Interface : Statistics", mainwindow)
                else:
                    show_failure("Text : Interface : Statistics", mainwindow)
            else:
                show_failure("Text : Interface : Statistics", mainwindow)
        else:
            logger.info("SKIPPED: Text : Interface")

        # Text: BooksAndHistory
        if settings["Settings"]["Checkboxes"]["Text"]["BooksAndHistory"] == True:
            uibooks_1_file = get_yaml(yaml_file, "Text", "BooksAndHistory", "Books", "File")
            uibooks_1_path = get_yaml(yaml_file, "Text", "BooksAndHistory", "Books", "Path")
            uibooks_tree  = parse(uibooks_1_path, workpath, uibooks_1_file)

            uihistory_file = get_yaml(yaml_file, "Text", "BooksAndHistory", "History", "File")
            uihistory_path = get_yaml(yaml_file, "Text", "BooksAndHistory", "History", "Path")
            uihistory_tree = parse(uihistory_path, workpath, uihistory_file)

            uibooks_diz_history_list = []

            if uibooks_tree:
                for value in uibooks_tree.findall("string"):
                    if "value" in value.attrib and "id" in value.attrib:
                        attrib = value.attrib["id"]
                        if attrib[(len(attrib) - 3):len(attrib)] == "diz" and value.attrib["value"] != "":
                            uibooks_diz_history_list.append(value.attrib["value"])
            
            if uihistory_tree:
                for value in uihistory_tree.findall("string"):
                    if "value" in value.attrib:
                        uibooks_diz_history_list.append(value.attrib["value"])
            
            random.shuffle(uibooks_diz_history_list)

            pl = 0
            if uibooks_tree:
                for value in uibooks_tree.findall("string"):
                    if "value" in value.attrib and "id" in value.attrib:
                        attrib = value.attrib["id"]
                        if attrib[(len(attrib) - 3):len(attrib)] == "diz" and value.attrib["value"] != "":
                            value.set("value", uibooks_diz_history_list[pl])
                            pl += 1
                
                if write(uibooks_tree, uibooks_1_file, uibooks_1_path, workpath):
                    show_success("Text : BooksAndHistory : UiBooks", mainwindow)
                else:
                    show_failure("Text : BooksAndHistory : UiBooks", mainwindow)
            else:
                show_failure("Text : BooksAndHistory : UiBooks", mainwindow)

            if uihistory_tree:
                for value in uihistory_tree.findall("string"):
                    if "value" in value.attrib:
                        value.set("value", uibooks_diz_history_list[pl])
                        pl += 1
                
                if write(uihistory_tree, uihistory_file, uihistory_path, workpath):
                    show_success("Text : BooksAndHistory : UiHistory", mainwindow)
                else:
                    show_failure("Text : BooksAndHistory : UiHistory", mainwindow)
            else:
                show_failure("Text : BooksAndHistory : UiHistory", mainwindow)
        else:
            logger.info("SKIPPED: Text : BooksAndHistory")
        
        # Text: Descriptions
        if settings["Settings"]["Checkboxes"]["Text"]["Descriptions"] == True:
            affixesdiz_1_file = get_yaml(yaml_file, "Text", "Descriptions", "AffixesDiz", "File")
            affixesdiz_1_path = get_yaml(yaml_file, "Text", "Descriptions", "AffixesDiz", "Path")
            affixesdiz_tree = parse(affixesdiz_1_path, workpath, affixesdiz_1_file)

            objectdiz_file = get_yaml(yaml_file, "Text", "Descriptions", "ObjectDiz", "File")
            objectdiz_path = get_yaml(yaml_file, "Text", "Descriptions", "ObjectDiz", "Path")
            objectdiz_tree = parse(objectdiz_path, workpath, objectdiz_file)

            uidescription_file = get_yaml(yaml_file, "Text", "Descriptions", "UiDescriptions", "File")
            uidescription_path = get_yaml(yaml_file, "Text", "Descriptions", "UiDescriptions", "Path")
            uidescription_tree = parse(uidescription_path, workpath, uidescription_file)

            help_1_file = get_yaml(yaml_file, "Text", "Descriptions", "Help", "File")
            help_1_path = get_yaml(yaml_file, "Text", "Descriptions", "Help", "Path")
            help_root = parse(help_1_path, workpath, help_1_file)

            clansdiz_1_file = get_yaml(yaml_file, "Text", "Descriptions", "Clansdiz", "File")
            clansdiz_1_path = get_yaml(yaml_file, "Text", "Descriptions", "Clansdiz", "Path")
            clansdiz = parse(clansdiz_1_path, workpath, clansdiz_1_file)

            all_descriptions_list = []

            if affixesdiz_tree:
                for value in affixesdiz_tree.findall("string"):
                    if "value" in value.attrib and "id" in value.attrib:
                        attrib = value.attrib["id"]
                        if attrib[(len(attrib) - 3):len(attrib)] == "diz":
                            all_descriptions_list.append(value.attrib["value"])
            
            if objectdiz_tree:
                for value in objectdiz_tree.findall("string"):
                    if "value" in value.attrib:
                        all_descriptions_list.append(value.attrib["value"])
            
            if uidescription_tree:
                for value in uidescription_tree.findall("string"):
                    if "value" in value.attrib:
                        all_descriptions_list.append(value.attrib["value"])
            
            if help_root:
                for value in help_root.findall("string"):
                    if "value" in value.attrib and "id" in value.attrib:
                        attrib = value.attrib["id"]
                        if attrib[(len(attrib) - 5):len(attrib)] != "title":
                            all_descriptions_list.append(value.attrib["value"])
            
            if clansdiz:
                for value in clansdiz.findall("string"):
                    if "value" in value.attrib and "id" in value.attrib:
                        attrib = value.attrib["id"]
                        if attrib[(len(attrib) - 3):len(attrib)] == "diz":
                            all_descriptions_list.append(value.attrib["value"])

            random.shuffle(all_descriptions_list)

            pl = 0

            if affixesdiz_tree:
                for value in affixesdiz_tree.findall("string"):
                    if "value" in value.attrib and "id" in value.attrib:
                        attrib = value.attrib["id"]
                        if attrib[(len(attrib) - 3):len(attrib)] == "diz":
                            value.set("value", all_descriptions_list[pl])
                            pl += 1
                
                if write(affixesdiz_tree, affixesdiz_1_file, affixesdiz_1_path, workpath):
                    show_success("Text : Descriptions : AffixesDiz", mainwindow)
                else:
                    show_failure("Text : Descriptions : AffixesDiz", mainwindow)
            else:
                show_failure("Text : Descriptions : AffixesDiz", mainwindow)
            
            if objectdiz_tree:
                for value in objectdiz_tree.findall("string"):
                    if "value" in value.attrib:
                        value.set("value", all_descriptions_list[pl])
                        pl += 1
                
                if write(objectdiz_tree, objectdiz_file, objectdiz_path, workpath):
                    show_success("Text : Descriptions : ObjectDiz", mainwindow)
                else:
                    show_failure("Text : Descriptions : ObjectDiz", mainwindow)
            else:
                show_failure("Text : Descriptions : ObjectDiz", mainwindow)
            
            if uidescription_tree:
                for value in uidescription_tree.findall("string"):
                    if "value" in value.attrib:
                        value.set("value", all_descriptions_list[pl])
                        pl += 1
                
                if write(uidescription_tree, uidescription_file, uidescription_path, workpath):
                    show_success("Text : Descriptions : UiDescription", mainwindow)
                else:
                    show_failure("Text : Descriptions : UiDescription", mainwindow)
            else:
                show_failure("Text : Descriptions : UiDescription", mainwindow)
            
            if help_root:
                for value in help_root.findall("string"):
                    if "value" in value.attrib and "id" in value.attrib:
                        attrib = value.attrib["id"]
                        if attrib[(len(attrib) - 5):len(attrib)] != "title":
                            value.set("value", all_descriptions_list[pl])
                            pl += 1
                
                if write(help_root, help_1_file, help_1_path, workpath):
                    show_success("Text : Descriptions : Help", mainwindow)
                else:
                    show_failure("Text : Descriptions : Help", mainwindow)
            else:
                show_failure("Text : Descriptions : Help", mainwindow)

            if clansdiz:
                for value in clansdiz.findall("string"):
                    if "value" in value.attrib and "id" in value.attrib:
                        attrib = value.attrib["id"]
                        if attrib[(len(attrib) - 3):len(attrib)] == "diz":
                            value.set("value", all_descriptions_list[pl])
                            pl += 1
                
                if write(clansdiz, clansdiz_1_file, clansdiz_1_path, workpath):
                    show_success("Text : Descriptions : ClansDiz", mainwindow)
                else:
                    show_failure("Text : Descriptions : ClansDiz", mainwindow)
            else:
                show_failure("Text : Descriptions : ClansDiz", mainwindow)
        else:
            logger.info("SKIPPED: Text : Descriptions")
        
        # Sounds: Music
        if settings["Settings"]["Checkboxes"]["Sounds"]["Music"] == True:
            mixmus_towns_path = get_yaml(yaml_file, "Sounds", "Music", "Towns", "Path")
            mixmus_cinematics_path = get_yaml(yaml_file, "Sounds", "Music", "Cinematics", "Path")
            mixmus_region1_1_path = get_yaml(yaml_file, "Sounds", "Music", "Blocks", "1-3", "Path")
            mixmus_region1_2_path = get_yaml(yaml_file, "Sounds", "Music", "Blocks", "r1m4", "Path")
            mixmus_region2_1_path = get_yaml(yaml_file, "Sounds", "Music", "Blocks", "france", "Path")
            mixmus_region2_2_path = get_yaml(yaml_file, "Sounds", "Music", "Blocks", "neutral", "Path")
            mixmus_region3_1_path = get_yaml(yaml_file, "Sounds", "Music", "Blocks", "jungle_1", "Path")
            mixmus_region3_2_path = get_yaml(yaml_file, "Sounds", "Music", "Blocks", "jungle_2", "Path")
            mixmus_region4_1_path = get_yaml(yaml_file, "Sounds", "Music", "Blocks", "desert_1", "Path")
            mixmus_region4_2_path = get_yaml(yaml_file, "Sounds", "Music", "Blocks", "desert_2", "Path")
            mixmus_music_path = get_yaml(yaml_file, "Sounds", "Music", "Music", "Path")

            mixmus_towns_list = get_yaml(yaml_file, "Sounds", "Music", "Towns", "Files")
            mixmus_cinematics_list = get_yaml(yaml_file, "Sounds", "Music", "Cinematics", "Files")
            mixmus_region1_1_list = get_yaml(yaml_file, "Sounds", "Music", "Blocks", "1-3", "Files")
            mixmus_region1_2_list = get_yaml(yaml_file, "Sounds", "Music", "Blocks", "r1m4", "Files")
            mixmus_region2_1_list = get_yaml(yaml_file, "Sounds", "Music", "Blocks", "france", "Files")
            mixmus_region2_2_list = get_yaml(yaml_file, "Sounds", "Music", "Blocks", "neutral", "Files")
            mixmus_region3_1_list = get_yaml(yaml_file, "Sounds", "Music", "Blocks", "jungle_1", "Files")
            mixmus_region3_2_list = get_yaml(yaml_file, "Sounds", "Music", "Blocks", "jungle_2", "Files")
            mixmus_region4_1_list = get_yaml(yaml_file, "Sounds", "Music", "Blocks", "desert_1", "Files")
            mixmus_region4_2_list = get_yaml(yaml_file, "Sounds", "Music", "Blocks", "desert_2", "Files")
            mixmus_music_list = get_yaml(yaml_file, "Sounds", "Music", "Music", "Files")
            files_to_mix = []

            if gameversion == "ImprovedStoryline":
                mixmus_region1_3_path = get_yaml(yaml_file, "Sounds", "Music", "Blocks", "r1m8", "Path")
                mixmus_region5_path = get_yaml(yaml_file, "Sounds", "Music", "Blocks", "winter_1", "Path")

                mixmus_region1_3_list = get_yaml(yaml_file, "Sounds", "Music", "Blocks", "r1m8", "File")
                mixmus_region5_list = get_yaml(yaml_file, "Sounds", "Music", "Blocks", "winter_1", "Files")

                if current_dir(mixmus_region1_3_path, workpath):
                    move(mixmus_region1_3_list, mix_folder_path, workpath)

                    include(mixmus_region1_3_list, files_to_mix)
                    
                if current_dir(mixmus_region5_path, workpath):
                    move(mixmus_region5_list, mix_folder_path, workpath)

                    include(mixmus_region5_list, files_to_mix)

            if current_dir(mixmus_towns_path, workpath):
                move(mixmus_towns_list, mix_folder_path, workpath)

            if current_dir(mixmus_cinematics_path, workpath):
                move(mixmus_cinematics_list, mix_folder_path, workpath)

            if current_dir(mixmus_region1_1_path, workpath):
                move(mixmus_region1_1_list, mix_folder_path, workpath)

            if current_dir(mixmus_region1_2_path, workpath):
                move(mixmus_region1_2_list, mix_folder_path, workpath)

            if current_dir(mixmus_region2_1_path, workpath):
                move(mixmus_region2_1_list, mix_folder_path, workpath)

            if current_dir(mixmus_region2_2_path, workpath):
                move(mixmus_region2_2_list, mix_folder_path, workpath)

            if current_dir(mixmus_region3_1_path, workpath):
                move(mixmus_region3_1_list, mix_folder_path, workpath)

            if current_dir(mixmus_region3_2_path, workpath):
                move(mixmus_region3_2_list, mix_folder_path, workpath)

            if current_dir(mixmus_region4_1_path, workpath):
                move(mixmus_region4_1_list, mix_folder_path, workpath)

            if current_dir(mixmus_region4_2_path, workpath):
                move(mixmus_region4_2_list, mix_folder_path, workpath)

            if current_dir(mixmus_music_path, workpath):
                move(mixmus_music_list, mix_folder_path, workpath)

            if current_dir(mix_folder_path, workpath):
                include([mixmus_towns_list, mixmus_cinematics_list, mixmus_region1_1_list, 
                         mixmus_region1_2_list, mixmus_region2_1_list, mixmus_region2_2_list, 
                         mixmus_region3_1_list, mixmus_region3_2_list, mixmus_region4_1_list, 
                         mixmus_region4_2_list, mixmus_music_list], files_to_mix)
                randomize(files_to_mix)

                move(mixmus_towns_list, mixmus_towns_path, workpath)
                move(mixmus_cinematics_list, mixmus_cinematics_path, workpath)
                move(mixmus_region1_1_list, mixmus_region1_1_path, workpath)
                move(mixmus_region1_2_list, mixmus_region1_2_path, workpath)
                move(mixmus_region2_1_list, mixmus_region2_1_path, workpath)
                move(mixmus_region2_2_list, mixmus_region2_2_path, workpath)
                move(mixmus_region3_1_list, mixmus_region3_1_path, workpath)
                move(mixmus_region3_2_list, mixmus_region3_2_path, workpath)
                move(mixmus_region4_1_list, mixmus_region4_1_path, workpath)
                move(mixmus_region4_2_list, mixmus_region4_2_path, workpath)
                move(mixmus_music_list, mixmus_music_path, workpath)

                if gameversion == "ImprovedStoryline":
                    move(mixmus_region1_3_list, mixmus_region1_3_path, workpath)
                    move(mixmus_region5_list, mixmus_region5_path, workpath)

                show_success("Sounds : Music", mainwindow)
            else:
                show_failure("Sounds : Music", mainwindow)
        else:
            logger.info("SKIPPED: Sounds : Music")
        
        # Sounds: Speech
        if settings["Settings"]["Checkboxes"]["Sounds"]["Speech"] == True:
            mixphrases_r1m1_path = get_yaml(yaml_file, "Sounds", "Speech", "r1m1", "Path")
            mixphrases_r1m2_path = get_yaml(yaml_file, "Sounds", "Speech", "r1m2", "Path")
            mixphrases_r1m3_path = get_yaml(yaml_file, "Sounds", "Speech", "r1m3", "Path")
            mixphrases_r1m4_path = get_yaml(yaml_file, "Sounds", "Speech", "r1m4", "Path")
            mixphrases_r2m1_path = get_yaml(yaml_file, "Sounds", "Speech", "r2m1", "Path")
            mixphrases_r2m2_path = get_yaml(yaml_file, "Sounds", "Speech", "r2m2", "Path")
            mixphrases_r3m1_path = get_yaml(yaml_file, "Sounds", "Speech", "r3m1", "Path")
            mixphrases_r3m2_path = get_yaml(yaml_file, "Sounds", "Speech", "r3m2", "Path")
            mixphrases_r4m1_path = get_yaml(yaml_file, "Sounds", "Speech", "r4m1", "Path")
            mixphrases_r4m2_path = get_yaml(yaml_file, "Sounds", "Speech", "r4m2", "Path")
            mixphrases_rolik_path = get_yaml(yaml_file, "Sounds", "Speech", "rolik", "Path")

            mixphrases_r1m1_list = get_yaml(yaml_file, "Sounds", "Speech", "r1m1", "Files")
            mixphrases_r1m2_list = get_yaml(yaml_file, "Sounds", "Speech", "r1m2", "Files")
            mixphrases_r1m3_list = get_yaml(yaml_file, "Sounds", "Speech", "r1m3", "Files")
            mixphrases_r1m4_list = get_yaml(yaml_file, "Sounds", "Speech", "r1m4", "Files")
            mixphrases_r2m1_list = get_yaml(yaml_file, "Sounds", "Speech", "r2m1", "Files")
            mixphrases_r2m2_list = get_yaml(yaml_file, "Sounds", "Speech", "r2m2", "Files")
            mixphrases_r3m1_list = get_yaml(yaml_file, "Sounds", "Speech", "r3m1", "Files")
            mixphrases_r3m2_list = get_yaml(yaml_file, "Sounds", "Speech", "r3m2", "Files")
            mixphrases_r4m1_list = get_yaml(yaml_file, "Sounds", "Speech", "r4m1", "Files")
            mixphrases_r4m2_list = get_yaml(yaml_file, "Sounds", "Speech", "r4m2", "Files")
            mixphrases_rolik_list = get_yaml(yaml_file, "Sounds", "Speech", "rolik", "Files")
            files_to_mix = []

            if current_dir(mixphrases_r1m1_path, workpath):
                move(mixphrases_r1m1_list, mix_folder_path, workpath)

            if current_dir(mixphrases_r1m2_path, workpath):
                move(mixphrases_r1m2_list, mix_folder_path, workpath)

            if current_dir(mixphrases_r1m3_path, workpath):
                move(mixphrases_r1m3_list, mix_folder_path, workpath)

            if current_dir(mixphrases_r1m4_path, workpath):
                move(mixphrases_r1m4_list, mix_folder_path, workpath)

            if current_dir(mixphrases_r2m1_path, workpath):
                move(mixphrases_r2m1_list, mix_folder_path, workpath)

            if current_dir(mixphrases_r2m2_path, workpath):
                move(mixphrases_r2m2_list, mix_folder_path, workpath)

            if current_dir(mixphrases_r3m1_path, workpath):
                move(mixphrases_r3m1_list, mix_folder_path, workpath)

            if current_dir(mixphrases_r3m2_path, workpath):
                move(mixphrases_r3m2_list, mix_folder_path, workpath)

            if current_dir(mixphrases_r4m1_path, workpath):
                move(mixphrases_r4m1_list, mix_folder_path, workpath)

            if current_dir(mixphrases_r4m2_path, workpath):
                move(mixphrases_r4m2_list, mix_folder_path, workpath)

            if current_dir(mixphrases_rolik_path, workpath):
                move(mixphrases_rolik_list, mix_folder_path, workpath)

            if current_dir(mix_folder_path, workpath):
                include([mixphrases_r1m1_list, mixphrases_r1m2_list, mixphrases_r1m3_list, 
                        mixphrases_r1m4_list, mixphrases_r2m1_list, mixphrases_r2m2_list, 
                        mixphrases_r3m1_list, mixphrases_r3m2_list, mixphrases_r4m1_list, 
                        mixphrases_r4m2_list, mixphrases_rolik_list], files_to_mix)
                randomize(files_to_mix)

                move(mixphrases_r1m1_list, mixphrases_r1m1_path, workpath)
                move(mixphrases_r1m2_list, mixphrases_r1m2_path, workpath)
                move(mixphrases_r1m3_list, mixphrases_r1m3_path, workpath)
                move(mixphrases_r1m4_list, mixphrases_r1m4_path, workpath)
                move(mixphrases_r2m1_list, mixphrases_r2m1_path, workpath)
                move(mixphrases_r2m2_list, mixphrases_r2m2_path, workpath)
                move(mixphrases_r3m1_list, mixphrases_r3m1_path, workpath)
                move(mixphrases_r3m2_list, mixphrases_r3m2_path, workpath)
                move(mixphrases_r4m1_list, mixphrases_r4m1_path, workpath)
                move(mixphrases_r4m2_list, mixphrases_r4m2_path, workpath)
                move(mixphrases_rolik_list, mixphrases_rolik_path, workpath)

                show_success("Sounds : Speech", mainwindow)
            else:
                show_failure("Sounds : Speech", mainwindow)
        else:
            logger.info("SKIPPED: Sounds : Speech")
        
        # Sounds: RadioSounds
        if settings["Settings"]["Checkboxes"]["Sounds"]["RadioSounds"] == True:
            mixradsamp_path = get_yaml(yaml_file, "Sounds", "RadioSounds", "Path")
            mixradsamp_list = get_yaml(yaml_file, "Sounds", "RadioSounds", "Files")

            if current_dir(mixradsamp_path, workpath):
                randomize(mixradsamp_list)
                show_success("Sounds : RadioSounds", mainwindow)
            else:
                show_failure("Sounds : RadioSounds", mainwindow)
        else:
            logger.info("SKIPPED: Sounds : RadioSounds")
        
        # Sounds: Crash
        if settings["Settings"]["Checkboxes"]["Sounds"]["Crash"] == True:
            mixcrash_path = get_yaml(yaml_file, "Sounds", "Crash", "Path")
            mixcrash_list = get_yaml(yaml_file, "Sounds", "Crash", "Files")

            if current_dir(mixcrash_path, workpath):
                randomize(mixcrash_list)
                show_success("Sounds : Crash", mainwindow)
            else:
                show_failure("Sounds : Crash", mainwindow)
        else:
            logger.info("SKIPPED: Sounds : Crash")
        
        # Sounds: Explosion
        if settings["Settings"]["Checkboxes"]["Sounds"]["Explosion"] == True:
            mixexp_path = get_yaml(yaml_file, "Sounds", "Explosion", "Path")
            mixexp_list = get_yaml(yaml_file, "Sounds", "Explosion", "Files")

            if current_dir(mixexp_path, workpath):
                randomize(mixexp_list)
                show_success("Sounds : Explosion", mainwindow)
            else:
                show_failure("Sounds : Explosion", mainwindow)
        else:
            logger.info("SKIPPED: Sounds : Explosion")

        # Sounds: Engine
        if settings["Settings"]["Checkboxes"]["Sounds"]["Engine"] == True:
            mixmot_path = get_yaml(yaml_file, "Sounds", "Engine", "Path")
            mixmot_list = get_yaml(yaml_file, "Sounds", "Engine", "Files")
            
            if current_dir(mixmot_path, workpath):
                randomize(mixmot_list)
                show_success("Sounds : Engine", mainwindow)
            else:
                show_failure("Sounds : Engine", mainwindow)
        else:
            logger.info("SKIPPED: Sounds : Engine")
        
        # Sounds: Horn
        if settings["Settings"]["Checkboxes"]["Sounds"]["Horn"] == True:
            mixhorn_path = get_yaml(yaml_file, "Sounds", "Horn", "Path")
            mixhorn_list = get_yaml(yaml_file, "Sounds", "Horn", "Files")

            if current_dir(mixhorn_path, workpath):
                randomize(mixhorn_list)
                show_success("Sounds : Horn", mainwindow)
            else:
                show_failure("Sounds : Horn", mainwindow)
        else:
            logger.info("SKIPPED: Sounds : Horn")

        # Sounds: Hit
        if settings["Settings"]["Checkboxes"]["Sounds"]["Hit"] == True:
            mixhit_events_path = get_yaml(yaml_file, "Sounds", "Hit", "Click", "Path")
            mixhit_shells_path = get_yaml(yaml_file, "Sounds", "Hit", "GunReload", "Path")
            mixhit_other_path = get_yaml(yaml_file, "Sounds", "Hit", "Other", "Path")
            mixhit_path = get_yaml(yaml_file, "Sounds", "Hit", "Hit", "Path")

            mixhit_events_list = get_yaml(yaml_file, "Sounds", "Hit", "Click", "File")
            mixhit_shells_list = get_yaml(yaml_file, "Sounds", "Hit", "GunReload", "File")
            mixhit_interface_list = get_yaml(yaml_file, "Sounds", "Hit", "Other", "Files")
            mixhit_list = get_yaml(yaml_file, "Sounds", "Hit", "Hit", "Files")
            files_to_mix = []

            if current_dir(mixhit_events_path, workpath):
                move(mixhit_events_list, mix_folder_path, workpath)

            
            if current_dir(mixhit_shells_path, workpath):
                move(mixhit_shells_list, mix_folder_path, workpath)

            
            if current_dir(mixhit_other_path, workpath):
                move(mixhit_interface_list, mix_folder_path, workpath)

            
            if current_dir(mixhit_path, workpath):
                move(mixhit_list, mix_folder_path, workpath)

            if current_dir(mix_folder_path, workpath):
                include([mixhit_events_list, mixhit_shells_list, mixhit_interface_list, 
                         mixhit_list], files_to_mix)
                randomize(files_to_mix)

                move(mixhit_events_list, mixhit_events_path, workpath)
                move(mixhit_shells_list, mixhit_shells_path, workpath)
                move(mixhit_interface_list, mixhit_other_path, workpath)
                move(mixhit_list, mixhit_path, workpath)

                show_success("Sounds : Hit", mainwindow)
            else:
                show_failure("Sounds : Hit", mainwindow)
        else:
            logger.info("SKIPPED: Sounds : Hit")
        
        # Sounds: Shooting
        if settings["Settings"]["Checkboxes"]["Sounds"]["Shooting"] == True:
            mixshoot_shooting_path = get_yaml(yaml_file, "Sounds", "Shooting", "Shooting", "Path")
            mixshoot_giantgun_path = get_yaml(yaml_file, "Sounds", "Shooting", "GiantGun", "Path")
            mixshoot_sidegun_path = get_yaml(yaml_file, "Sounds", "Shooting", "SideGun", "Path")
            mixshoot_smallgun_path = get_yaml(yaml_file, "Sounds", "Shooting", "SmallGun", "Path")
            mixshoot_special_path = get_yaml(yaml_file, "Sounds", "Shooting", "Special", "Path")
            mixshoot_path = get_yaml(yaml_file, "Sounds", "Shooting", "BigGun", "Path")

            mixshoot_shooting_list = get_yaml(yaml_file, "Sounds", "Shooting", "Shooting", "Files")
            mixshoot_giantgun_list = get_yaml(yaml_file, "Sounds", "Shooting", "GiantGun", "Files")
            mixshoot_sidegun_list = get_yaml(yaml_file, "Sounds", "Shooting", "SideGun", "Files")
            mixshoot_smallgun_list = get_yaml(yaml_file, "Sounds", "Shooting", "SmallGun", "Files")
            mixshoot_special_list = get_yaml(yaml_file, "Sounds", "Shooting", "Special", "Files")
            mixshoot_list = get_yaml(yaml_file, "Sounds", "Shooting", "BigGun", "Files")
            files_to_mix = []

            if current_dir(mixshoot_shooting_path, workpath):
                move(mixshoot_shooting_list, mix_folder_path, workpath)

            if current_dir(mixshoot_giantgun_path, workpath):
                move(mixshoot_giantgun_list, mix_folder_path, workpath)

            if current_dir(mixshoot_sidegun_path, workpath):
                move(mixshoot_sidegun_list, mix_folder_path, workpath)

            if current_dir(mixshoot_smallgun_path, workpath):
                move(mixshoot_smallgun_list, mix_folder_path, workpath)

            if current_dir(mixshoot_special_path, workpath):
                move(mixshoot_special_list, mix_folder_path, workpath)

            if current_dir(mixshoot_path, workpath):
                move(mixshoot_list, mix_folder_path, workpath)

            if current_dir(mix_folder_path, workpath):
                include([mixshoot_shooting_list, mixshoot_giantgun_list, mixshoot_sidegun_list, 
                         mixshoot_smallgun_list, mixshoot_special_list], files_to_mix)
                randomize(files_to_mix)

                move(mixshoot_shooting_list, mixshoot_shooting_path, workpath)
                move(mixshoot_giantgun_list, mixshoot_giantgun_path, workpath)
                move(mixshoot_sidegun_list, mixshoot_sidegun_path, workpath)
                move(mixshoot_smallgun_list, mixshoot_smallgun_path, workpath)
                move(mixshoot_special_list, mixshoot_special_path, workpath)
                move(mixshoot_list, mixshoot_path, workpath)

                show_success("Sounds : Shooting", mainwindow)
            else:
                show_failure("Sounds : Shooting", mainwindow)
        else:
            logger.info("SKIPPED: Sounds : Shooting")
        
        # Sounds: Other
        if settings["Settings"]["Checkboxes"]["Sounds"]["Other"] == True:
            mixemb_ambience_path = get_yaml(yaml_file, "Sounds", "Other", "Ambience", "Path")
            mixemb_cinematicsound_path = get_yaml(yaml_file, "Sounds", "Other", "CinematicSound", "Path")
            mixemb_cutscenes_path = get_yaml(yaml_file, "Sounds", "Other", "Cutscenes", "Path")
            mixemb_boat_path = get_yaml(yaml_file, "Sounds", "Other", "Boat", "Path")
            mixemb_boss01_path = get_yaml(yaml_file, "Sounds", "Other", "Boss01", "Path")
            mixemb_boss02_path = get_yaml(yaml_file, "Sounds", "Other", "Boss02", "Path")
            mixemb_boss03_path = get_yaml(yaml_file, "Sounds", "Other", "Boss03", "Path")
            mixemb_boss04_path = get_yaml(yaml_file, "Sounds", "Other", "Boss04", "Path")
            mixemb_path = get_yaml(yaml_file, "Sounds", "Other", "Boss", "Path")

            mixemb_ambience_list = get_yaml(yaml_file, "Sounds", "Other", "Ambience", "Files")
            mixemb_cinematicsound_list = get_yaml(yaml_file, "Sounds", "Other", "CinematicSound", "Files")
            mixemb_cutscenes_list = get_yaml(yaml_file, "Sounds", "Other", "Cutscenes", "Files")
            mixemb_boat_list = get_yaml(yaml_file, "Sounds", "Other", "Boat", "Files")
            mixemb_boss01_list = get_yaml(yaml_file, "Sounds", "Other", "Boss01", "Files")
            mixemb_boss02_list = get_yaml(yaml_file, "Sounds", "Other", "Boss02", "Files")
            mixemb_boss03_list = get_yaml(yaml_file, "Sounds", "Other", "Boss03", "File")
            mixemb_boss04_list = get_yaml(yaml_file, "Sounds", "Other", "Boss04", "File")
            mixemb_list = get_yaml(yaml_file, "Sounds", "Other", "Boss", "File")
            files_to_mix = []

            if current_dir(mixemb_ambience_path, workpath):
                move(mixemb_ambience_list, mix_folder_path, workpath)

            if current_dir(mixemb_cinematicsound_path, workpath):
                move(mixemb_cinematicsound_list, mix_folder_path, workpath)

            if current_dir(mixemb_cutscenes_path, workpath):
                move(mixemb_cutscenes_list, mix_folder_path, workpath)

            if current_dir(mixemb_boat_path, workpath):
                move(mixemb_boat_list, mix_folder_path, workpath)

            if current_dir(mixemb_boss01_path, workpath):
                move(mixemb_boss01_list, mix_folder_path, workpath)

            if current_dir(mixemb_boss02_path, workpath):
                move(mixemb_boss02_list, mix_folder_path, workpath)

            if current_dir(mixemb_boss03_path, workpath):
                move(mixemb_boss03_list, mix_folder_path, workpath)

            if current_dir(mixemb_boss04_path, workpath):
                move(mixemb_boss04_list, mix_folder_path, workpath)

            if current_dir(mixemb_path, workpath):
                move(mixemb_list, mix_folder_path, workpath)

            if current_dir(mix_folder_path, workpath):
                include([mixemb_ambience_list, mixemb_cinematicsound_list, mixemb_cutscenes_list, 
                         mixemb_boat_list, mixemb_boss01_list, mixemb_boss02_list, mixemb_boss03_list, 
                         mixemb_boss04_list, mixemb_list], files_to_mix)
                randomize(files_to_mix)

                move(mixemb_ambience_list, mixemb_ambience_path, workpath)
                move(mixemb_cinematicsound_list, mixemb_cinematicsound_path, workpath)
                move(mixemb_cutscenes_list, mixemb_cutscenes_path, workpath)
                move(mixemb_boat_list, mixemb_boat_path, workpath)
                move(mixemb_boss01_list, mixemb_boss01_path, workpath)
                move(mixemb_boss02_list, mixemb_boss02_path, workpath)
                move(mixemb_boss03_list, mixemb_boss03_path, workpath)
                move(mixemb_boss04_list, mixemb_boss04_path, workpath)
                move(mixemb_list, mixemb_path, workpath)

                show_success("Sounds : Other", mainwindow)
            else:
                show_failure("Sounds : Other", mainwindow)
        else:
            logger.info("SKIPPED: Sounds : Other")
        
        # Models
        animmodels_path = get_yaml(yaml_file, "Models", "Path")
        animmodels_file = get_yaml(yaml_file, "Models", "File")

        # Models: Static
        if settings["Settings"]["Checkboxes"]["Models"]["Static"] == True:
            animmodels = parse(animmodels_path, workpath, animmodels_file)
            if animmodels:
                animmodels_root = animmodels.getroot()
                animmodels_model = animmodels_root.findall("model")

                for duplicate in ["shell02", "1_riback"]:
                    a = 0
                    for id in animmodels_model:
                        if "id" in id.attrib:
                            if id.attrib["id"] == duplicate and a == 1:
                                del(id.attrib["id"])
                                del(id.attrib["file"])
                            elif id.attrib["id"] == duplicate:
                                a += 1
                
                models_0_list = get_yaml(yaml_file, "Models", "Static", "Files", "Group0")
                models_1_list = get_yaml(yaml_file, "Models", "Static", "Files", "Group1")
                models_2_list = get_yaml(yaml_file, "Models", "Static", "Files", "Group2")
                models_3_list = get_yaml(yaml_file, "Models", "Static", "Files", "Group3")
                models_4_list = get_yaml(yaml_file, "Models", "Static", "Files", "Group4")
                models_5_list = get_yaml(yaml_file, "Models", "Static", "Files", "Group5")
                models_6_list = get_yaml(yaml_file, "Models", "Static", "Files", "Group6")
                models_7_list = get_yaml(yaml_file, "Models", "Static", "Files", "Group7")
                models_8_list = get_yaml(yaml_file, "Models", "Static", "Files", "Group8")
                models_9_list = get_yaml(yaml_file, "Models", "Static", "Files", "Group9")
                models_10_list = get_yaml(yaml_file, "Models", "Static", "Files", "Group10")
                models_11_list = get_yaml(yaml_file, "Models", "Static", "Files", "Group11")

                models_lists = [models_0_list, models_1_list, models_2_list, models_3_list, 
                                models_4_list, models_5_list, models_6_list, models_7_list, 
                                models_8_list, models_9_list, models_10_list, models_11_list]

                placeholder = 0
                for models_list in models_lists:
                    for model in models_list:
                        for id in animmodels_model:
                            if "id" in id.attrib:
                                if model == id.attrib["id"]:
                                    id.set("id", "PLACEHOLDER_STATIC_" + str(placeholder))
                    placeholder += 1
                
                for models_list in models_lists:
                    random.shuffle(models_list)

                placeholder = 0
                pl = 0
                for models_list in models_lists:
                    for id in animmodels_model:
                        if "id" in id.attrib:
                            if "PLACEHOLDER_STATIC_" + str(placeholder) == id.attrib["id"]:
                                id.set("id", models_list[pl])
                                pl += 1
                    pl = 0
                    placeholder += 1
                
                if write(animmodels, animmodels_file, animmodels_path, workpath):
                    show_success("Models : Static", mainwindow)
                else:
                    show_failure("Models : Static", mainwindow)
            else:
                show_failure("Models : Static", mainwindow)
        else:
            logger.info("SKIPPED: Models : Static")
        
        # Models: Towns
        if settings["Settings"]["Checkboxes"]["Models"]["Towns"] == True:
            animmodels = parse(animmodels_path, workpath, animmodels_file)
            if animmodels:
                animmodels_root = animmodels.getroot()
                animmodels_model = animmodels_root.findall("model")

                models_towns_list = get_yaml(yaml_file, "Models", "Towns", "Files", "Towns")
                models_gates_list = get_yaml(yaml_file, "Models", "Towns", "Files", "Gates")

                a = 0
                for id in animmodels_model:
                    if "id" in id.attrib:
                        if id.attrib["id"] == "helvecia" and a == 1:
                            del(id.attrib["id"])
                            del(id.attrib["file"])
                        elif id.attrib["id"] == "helvecia":
                            a += 1
                
                placeholder = 0
                for models_list in [models_towns_list, models_gates_list]:
                    for model in models_list:
                        for id in animmodels_model:
                            if "id" in id.attrib:
                                if model == id.attrib["id"]:
                                    id.set("id", "PLACEHOLDER_TOWNS_" + str(placeholder))
                    placeholder += 1
                
                for models_list in [models_towns_list, models_gates_list]:
                    random.shuffle(models_list)
                
                placeholder = 0
                pl = 0
                for models_list in [models_towns_list, models_gates_list]:
                    for id in animmodels_model:
                        if "id" in id.attrib:
                            if "PLACEHOLDER_TOWNS_" + str(placeholder) == id.attrib["id"]:
                                id.set("id", models_list[pl])
                                pl += 1
                    pl = 0
                    placeholder += 1
                
                if write(animmodels, animmodels_file, animmodels_path, workpath):
                    show_success("Models : Towns", mainwindow)
                else:
                    show_failure("Models : Towns", mainwindow)
            else:
                show_failure("Models : Towns", mainwindow)
        else:
            logger.info("SKIPPED: Models : Towns")
        
        # Models: Guns
        if settings["Settings"]["Checkboxes"]["Models"]["Guns"] == True:
            animmodels = parse(animmodels_path, workpath, animmodels_file)
            if animmodels:
                animmodels_root = animmodels.getroot()
                animmodels_model = animmodels_root.findall("model")

                no_guns_list = get_yaml(yaml_file, "Models", "Guns", "Files", "Group0")
                guns_1_list = get_yaml(yaml_file, "Models", "Guns", "Files", "Group1")
                guns_2_list = get_yaml(yaml_file, "Models", "Guns", "Files", "Group2")

                placeholder = 0
                for gun_list in [no_guns_list, guns_1_list, guns_2_list]:
                    for model in gun_list:
                        for id in animmodels_model:
                            if "id" in id.attrib:
                                if model == id.attrib["id"]:
                                    id.set("id", "PLACEHOLDER_GUNS_" + str(placeholder))
                    placeholder += 1
                
                for gun_list in [no_guns_list, guns_1_list, guns_2_list]:
                    random.shuffle(gun_list)
                
                placeholder = 0
                pl = 0
                for gun_list in [no_guns_list, guns_1_list, guns_2_list]:
                    for id in animmodels_model:
                        if "id" in id.attrib:
                            if "PLACEHOLDER_GUNS_" + str(placeholder) == id.attrib["id"]:
                                id.set("id", gun_list[pl])
                                pl += 1
                    pl = 0
                    placeholder += 1
                
                if write(animmodels, animmodels_file, animmodels_path, workpath):
                    show_success("Models : Guns", mainwindow)
                else:
                    show_failure("Models : Guns", mainwindow)
            else:
                show_failure("Models : Guns", mainwindow)
        else:
            logger.info("SKIPPED: Models : Guns")
        
        # Models: Trees
        if settings["Settings"]["Checkboxes"]["Models"]["Trees"] == True:
            animmodels = parse(animmodels_path, workpath, animmodels_file)
            if animmodels:
                animmodels_root = animmodels.getroot()
                animmodels_model = animmodels_root.findall("model")

                mixtrees_1_list = get_yaml(yaml_file, "Models", "Trees", "Files", "Group0")
                mixtrees_2_list = get_yaml(yaml_file, "Models", "Trees", "Files", "Group1")

                placeholder = 0
                for trees_list in [mixtrees_1_list, mixtrees_2_list]:
                    for model in trees_list:
                        for id in animmodels_model:
                            if "id" in id.attrib:
                                if model == id.attrib["id"]:
                                    id.set("id", "PLACEHOLDER_TREES_" + str(placeholder))
                    placeholder += 1
                
                for trees_list in [mixtrees_1_list, mixtrees_2_list]:
                    random.shuffle(trees_list)
                
                placeholder = 0
                pl = 0
                for trees_list in [mixtrees_1_list, mixtrees_2_list]:
                    for id in animmodels_model:
                        if "id" in id.attrib:
                            if "PLACEHOLDER_TREES_" + str(placeholder) == id.attrib["id"]:
                                id.set("id", trees_list[pl])
                                pl += 1
                    pl = 0
                    placeholder += 1
                
                if write(animmodels, animmodels_file, animmodels_path, workpath):
                    show_success("Models : Trees", mainwindow)
                else:
                    show_failure("Models : Trees", mainwindow)
            else:
                show_failure("Models : Trees", mainwindow)
        else:
            logger.info("SKIPPED: Models : Trees")
        
        # Models: BarNpc
        if settings["Settings"]["Checkboxes"]["Models"]["BarNpc"] == True:
            BarNPC_Dyncs_name = get_yaml(yaml_file, "Models", "BarNpc", "DynamicScene")
            BarNPC_strings_name = get_yaml(yaml_file, "Models", "BarNpc", "Strings")
            BarNPC_paths = get_yaml(yaml_file, "Models", "BarNpc", "Paths")
            BarNPCs_dynsc_list = []
            BarNPCs_strings_list = []

            # NPC prototypes in dynamiscene.xml

            for path in BarNPC_paths:
                BarNPC_dynsc = parse(path, workpath, BarNPC_Dyncs_name)
                if BarNPC_dynsc:
                    BarNPC_dynsc_root = BarNPC_dynsc.getroot()

                    for object in BarNPC_dynsc_root.iter("Object"):
                        attr = object.attrib["Prototype"]
                        if attr == "NPC":
                            NPCview = []
                            if "skin" in object.attrib:
                                NPCview.append(object.attrib["skin"])
                            else:
                                NPCview.append("0")

                            if "cfg" in object.attrib:
                                NPCview.append(object.attrib["cfg"])
                            else:
                                NPCview.append("0")

                            NPCview.append(object.attrib["ModelName"])

                            BarNPCs_dynsc_list.append(NPCview)
                    
            random.shuffle(BarNPCs_dynsc_list)

            pl = 0
            for path in BarNPC_paths:
                BarNPC_dynsc = parse(path, workpath, BarNPC_Dyncs_name)
                if BarNPC_dynsc:
                    BarNPC_dynsc_root = BarNPC_dynsc.getroot()

                    for object in BarNPC_dynsc_root.iter("Object"):
                        attr = object.attrib["Prototype"]
                        if attr == "NPC":

                            object.set("skin", BarNPCs_dynsc_list[pl][0])

                            object.set("cfg", BarNPCs_dynsc_list[pl][1])

                            object.set("ModelName", BarNPCs_dynsc_list[pl][2])

                            pl += 1
                    
                    if write(BarNPC_dynsc, BarNPC_Dyncs_name, path, workpath):
                        show_success(f"Models : BarNpc : DynamicScene ({path[len(path)-5:len(path)-1]})", mainwindow)
                    else:
                        show_failure(f"Models : BarNpc : DynamicScene ({path[len(path)-5:len(path)-1]})", mainwindow)
            
            # NPC models in strings.xml

            for path in BarNPC_paths:
                BarNPC_strings = parse(path, workpath, BarNPC_strings_name)
                if BarNPC_strings:
                    BarNPC_strings_root = BarNPC_strings.getroot()

                    for string in BarNPC_strings_root.findall("string"):
                        if "modelName" in string.attrib:
                            NPCview = []

                            if "modelCfg" in string.attrib:
                                NPCview.append(string.attrib["modelCfg"])
                            else:
                                NPCview.append("0")

                            if "modelSkin" in string.attrib:
                                NPCview.append(string.attrib["modelSkin"])
                            else:
                                NPCview.append("0")

                            NPCview.append(string.attrib["modelName"])

                            BarNPCs_strings_list.append(NPCview)

            random.shuffle(BarNPCs_strings_list)

            pl = 0
            for path in BarNPC_paths:
                BarNPC_strings = parse(path, workpath, BarNPC_strings_name)
                if BarNPC_strings:
                    BarNPC_strings_root = BarNPC_strings.getroot()

                    for string in BarNPC_strings_root.findall("string"):
                        if "modelName" in string.attrib:
                            if BarNPCs_strings_list[pl][0] != "0":
                                string.set("modelCfg", BarNPCs_strings_list[pl][0])
                            elif "modelCfg" in string.attrib:
                                string.attrib.pop("modelCfg", None)

                            if BarNPCs_strings_list[pl][1] != "0":
                                string.set("modelSkin", BarNPCs_strings_list[pl][1])
                            elif "modelSkin" in string.attrib:
                                string.attrib.pop("modelSkin", None)

                            string.set("modelName", BarNPCs_strings_list[pl][2])

                            pl += 1
                    
                    if write(BarNPC_strings, BarNPC_strings_name, path, workpath):
                        show_success(f"Models : BarNpc : Strings ({path[len(path)-5:len(path)-1]})", mainwindow)
                    else:
                        show_failure(f"Models : BarNpc : Strings ({path[len(path)-5:len(path)-1]})", mainwindow)
        else:
            logger.info("SKIPPED: Models : BarNpc")
        
        # Models: Wheels
        if settings["Settings"]["Checkboxes"]["Models"]["Wheels"] == True:
            animmodels = parse(animmodels_path, workpath, animmodels_file)
            if animmodels:
                animmodels_root = animmodels.getroot()
                animmodels_list = get_yaml(yaml_file, "Models", "Wheels", "Files")

                for model in animmodels_list:
                    for id in animmodels_root.findall("model"):
                        if "id" in id.attrib:
                            if model in str(id.attrib["id"]):
                                id.set("id", "PLACEHOLDER_WHEELS")

                random.shuffle(animmodels_list)

                pl = 0
                for id in animmodels_root.findall("model"):
                    if "id" in id.attrib:
                        if "PLACEHOLDER_WHEELS" in id.attrib["id"]:
                            id.set("id", animmodels_list[pl])
                            pl += 1

                if write(animmodels, animmodels_file, animmodels_path, workpath):
                    show_success("Models : Wheels", mainwindow)
                else:
                    show_failure("Models : Wheels", mainwindow)
            else:
                show_failure("Models : Wheels", mainwindow)
        else:
            logger.info("SKIPPED: Models : Wheels")
        
        # Models: Humans
        if settings["Settings"]["Checkboxes"]["Models"]["Humans"] == True:
            breakableobjects_path = get_yaml(yaml_file, "Models", "Humans", "Path")
            breakableobjects_file = get_yaml(yaml_file, "Models", "Humans", "File")

            breakableobjects = parse(breakableobjects_path, workpath, breakableobjects_file)
            if breakableobjects:
                breakableobjects_root = breakableobjects.getroot()
                humans_prots_list = get_yaml(yaml_file, "Models", "Humans", "Strings", "Prototypes")
                human_models_list = get_yaml(yaml_file, "Models", "Humans", "Strings", "Models")

                random.shuffle(human_models_list)

                pl = 0
                for human in humans_prots_list:
                    for prototype in breakableobjects_root.findall("Prototype"):
                        if "ModelFile" in prototype.attrib and "Name" in prototype.attrib:
                            if prototype.attrib["Name"] == human:
                                prototype.set("ModelFile", human_models_list[pl])
                                pl += 1

                if write(breakableobjects, breakableobjects_file, breakableobjects_path, workpath):
                    show_success("Models : Humans", mainwindow)
                else:
                    show_failure("Models : Humans", mainwindow)
            else:
                show_failure("Models : Humans", mainwindow)
        else:
            logger.info("SKIPPED: Models : Humans")
        
        # Textures: Surround
        if settings["Settings"]["Checkboxes"]["Textures"]["Surround"] == True:
            mixtex_path = get_yaml(yaml_file, "Textures", "Surround", "Acient", "Path")
            mixtex_all_path = get_yaml(yaml_file, "Textures", "Surround", "All", "Path")
            mixtex_detail_path = get_yaml(yaml_file, "Textures", "Surround", "Detail", "Path")
            mixtex_factory_path = get_yaml(yaml_file, "Textures", "Surround", "Factory", "Path")
            mixtex_kladbische_path = get_yaml(yaml_file, "Textures", "Surround", "Kladbische", "Path")
            mixtex_misc_path = get_yaml(yaml_file, "Textures", "Surround", "Misc", "Path")
            mixtex_region1_path = get_yaml(yaml_file, "Textures", "Surround", "Region1", "Path")
            mixtex_region2_path = get_yaml(yaml_file, "Textures", "Surround", "Region2", "Path")
            mixtex_region3_path = get_yaml(yaml_file, "Textures", "Surround", "Region3", "Path")
            mixtex_region4_path = get_yaml(yaml_file, "Textures", "Surround", "Region4", "Path")
            mixtex_special_path = get_yaml(yaml_file, "Textures", "Surround", "Special", "Path")
            mixtex_boss02_path = get_yaml(yaml_file, "Textures", "Surround", "Boss02", "Path")
            mixtex_boss04_path = get_yaml(yaml_file, "Textures", "Surround", "Boss04", "Path")
            mixtex_submarina_path = get_yaml(yaml_file, "Textures", "Surround", "Submarina", "Path")
            mixtex_submarine_path = get_yaml(yaml_file, "Textures", "Surround", "Submarine", "Path")
            mixtex_questitems_path = get_yaml(yaml_file, "Textures", "Surround", "QuestItems", "Path")
            mixtex_grass1_path = get_yaml(yaml_file, "Textures", "Surround", "Grass1", "Path")
            mixtex_grass3_path = get_yaml(yaml_file, "Textures", "Surround", "Grass3", "Path")
            mixtex_grass4_path = get_yaml(yaml_file, "Textures", "Surround", "Grass4", "Path")
            mixtex_nature1_path = get_yaml(yaml_file, "Textures", "Surround", "Nature1", "Path")
            mixtex_nature2_path = get_yaml(yaml_file, "Textures", "Surround", "Nature2", "Path")
            mixtex_nature3_path = get_yaml(yaml_file, "Textures", "Surround", "Nature3", "Path")
            mixtex_nature4_path = get_yaml(yaml_file, "Textures", "Surround", "Nature4", "Path")
            mixtex_goods_path = get_yaml(yaml_file, "Textures", "Surround", "Goods", "Path")
            mixtex_brige_tube_path = get_yaml(yaml_file, "Textures", "Surround", "BrigeTube", "Path")
            mixtex_boss04_drone_path = get_yaml(yaml_file, "Textures", "Surround", "Boss04Drone", "Path")
            mixtex_rally_path = get_yaml(yaml_file, "Textures", "Surround", "Region4Rally", "Path")
            mixtex_nlo_path = get_yaml(yaml_file, "Textures", "Surround", "Region4NLO", "Path")
            mixtex_buildings_region2_path = get_yaml(yaml_file, "Textures", "Surround", "Region2Buildings", "Path")
            mixtex_gadgets_path = get_yaml(yaml_file, "Textures", "Surround", "Gadgets", "Path")
            mixtex_objects_path = get_yaml(yaml_file, "Textures", "Surround", "Objects", "Path")
            mixtex_masks_1_man_path = get_yaml(yaml_file, "Textures", "Surround", "Region1Man", "Path")
            mixtex_masks_1_woman_path = get_yaml(yaml_file, "Textures", "Surround", "Region1Woman", "Path")
            mixtex_masks_2_man_path = get_yaml(yaml_file, "Textures", "Surround", "Region2Man", "Path")
            mixtex_masks_2_woman_path = get_yaml(yaml_file, "Textures", "Surround", "Region2Woman", "Path")
            mixtex_masks_3_man_path = get_yaml(yaml_file, "Textures", "Surround", "Region3Man", "Path")
            mixtex_masks_4_man_path = get_yaml(yaml_file, "Textures", "Surround", "Region4Man", "Path")
            mixtex_masks_main_path = get_yaml(yaml_file, "Textures", "Surround", "MainMasks", "Path")
            mixtex_ammo_path = get_yaml(yaml_file, "Textures", "Surround", "Ammo", "Path")
            mixtex_guns_path = get_yaml(yaml_file, "Textures", "Surround", "Guns", "Path")
            mixtex_objectbox_path = get_yaml(yaml_file, "Textures", "Surround", "ObjectsBox", "Path")
            mixtex_objectconteiner_path = get_yaml(yaml_file, "Textures", "Surround", "ObjectsConteiner", "Path")
            mixtex_objectprovoda_path = get_yaml(yaml_file, "Textures", "Surround", "ObjectsProvoda", "Path")
            mixtex_boss01_path = get_yaml(yaml_file, "Textures", "Surround", "Boss01", "Path")
            mixtex_boss03_path = get_yaml(yaml_file, "Textures", "Surround", "Boss03", "Path")
            mixtex_region1benhouse_path = get_yaml(yaml_file, "Textures", "Surround", "Region1BenHouse", "Path")
            mixtex_cliffsr2_path = get_yaml(yaml_file, "Textures", "Surround", "CliffsR2", "Path")
            mixtex_forcopying_path = get_yaml(yaml_file, "Textures", "Surround", "ForCopying", "PathTo")

            mixtex_list = get_yaml(yaml_file, "Textures", "Surround", "Acient", "Files")
            mixtex_all_list = get_yaml(yaml_file, "Textures", "Surround", "All", "Files")
            mixtex_detail_list = get_yaml(yaml_file, "Textures", "Surround", "Detail", "Files")
            mixtex_factory_list = get_yaml(yaml_file, "Textures", "Surround", "Factory", "Files")
            mixtex_kladbische_list = get_yaml(yaml_file, "Textures", "Surround", "Kladbische", "Files")
            mixtex_misc_list = get_yaml(yaml_file, "Textures", "Surround", "Misc", "Files")
            mixtex_region1_list = get_yaml(yaml_file, "Textures", "Surround", "Region1", "Files")
            mixtex_region2_list = get_yaml(yaml_file, "Textures", "Surround", "Region2", "Files")
            mixtex_region3_list = get_yaml(yaml_file, "Textures", "Surround", "Region3", "Files")
            mixtex_region4_list = get_yaml(yaml_file, "Textures", "Surround", "Region4", "Files")
            mixtex_special_list = get_yaml(yaml_file, "Textures", "Surround", "Special", "Files")
            mixtex_boss02_list = get_yaml(yaml_file, "Textures", "Surround", "Boss02", "Files")
            mixtex_boss04_list = get_yaml(yaml_file, "Textures", "Surround", "Boss04", "Files")
            mixtex_submarina_list = get_yaml(yaml_file, "Textures", "Surround", "Submarina", "Files")
            mixtex_submarine_list = get_yaml(yaml_file, "Textures", "Surround", "Submarine", "Files")
            mixtex_questitems_list = get_yaml(yaml_file, "Textures", "Surround", "QuestItems", "Files")
            mixtex_grass1_list = get_yaml(yaml_file, "Textures", "Surround", "Grass1", "Files")
            mixtex_grass3_list = get_yaml(yaml_file, "Textures", "Surround", "Grass3", "Files")
            mixtex_grass4_list = get_yaml(yaml_file, "Textures", "Surround", "Grass4", "Files")
            mixtex_nature1_list = get_yaml(yaml_file, "Textures", "Surround", "Nature1", "Files")
            mixtex_nature2_list = get_yaml(yaml_file, "Textures", "Surround", "Nature2", "Files")
            mixtex_nature3_list = get_yaml(yaml_file, "Textures", "Surround", "Nature3", "Files")
            mixtex_nature4_list = get_yaml(yaml_file, "Textures", "Surround", "Nature4", "Files")
            mixtex_goods_list = get_yaml(yaml_file, "Textures", "Surround", "Goods", "Files")
            mixtex_brige_tube_list = get_yaml(yaml_file, "Textures", "Surround", "BrigeTube", "Files")
            mixtex_boss04_drone_list = get_yaml(yaml_file, "Textures", "Surround", "Boss04Drone", "Files")
            mixtex_rally_list = get_yaml(yaml_file, "Textures", "Surround", "Region4Rally", "Files")
            mixtex_nlo_list = get_yaml(yaml_file, "Textures", "Surround", "Region4NLO", "Files")
            mixtex_buildings_region2_list = get_yaml(yaml_file, "Textures", "Surround", "Region2Buildings", "Files")
            mixtex_gadgets_list = get_yaml(yaml_file, "Textures", "Surround", "Gadgets", "Files")
            mixtex_objects_list = get_yaml(yaml_file, "Textures", "Surround", "Objects", "Files")
            mixtex_masks_1_man_list = get_yaml(yaml_file, "Textures", "Surround", "Region1Man", "Files")
            mixtex_masks_1_woman_list = get_yaml(yaml_file, "Textures", "Surround", "Region1Woman", "Files")
            mixtex_masks_2_man_list = get_yaml(yaml_file, "Textures", "Surround", "Region2Man", "Files")
            mixtex_masks_2_woman_list = get_yaml(yaml_file, "Textures", "Surround", "Region2Woman", "Files")
            mixtex_masks_3_man_list = get_yaml(yaml_file, "Textures", "Surround", "Region3Man", "Files")
            mixtex_masks_4_man_list = get_yaml(yaml_file, "Textures", "Surround", "Region4Man", "Files")
            mixtex_masks_main_list = get_yaml(yaml_file, "Textures", "Surround", "MainMasks", "Files")
            mixtex_ammo_list = get_yaml(yaml_file, "Textures", "Surround", "Ammo", "Files")
            mixtex_guns_list = get_yaml(yaml_file, "Textures", "Surround", "Guns", "Files")
            mixtex_objectbox_file = get_yaml(yaml_file, "Textures", "Surround", "ObjectsBox", "File")
            mixtex_objectconteiner_file = get_yaml(yaml_file, "Textures", "Surround", "ObjectsConteiner", "File")
            mixtex_objectprovoda_file = get_yaml(yaml_file, "Textures", "Surround", "ObjectsProvoda", "File")
            mixtex_boss01_file = get_yaml(yaml_file, "Textures", "Surround", "Boss01", "File")
            mixtex_boss03_file = get_yaml(yaml_file, "Textures", "Surround", "Boss03", "File")
            mixtex_region1benhouse_file = get_yaml(yaml_file, "Textures", "Surround", "Region1BenHouse", "File")
            mixtex_cliffsr2_file = get_yaml(yaml_file, "Textures", "Surround", "CliffsR2", "File")
            mixtex_forcopying_file = get_yaml(yaml_file, "Textures", "Surround", "ForCopying", "File")
            files_to_mix = []

            if gameversion == "ImprovedStoryline":
                mixtex_nature1_path_1 = get_yaml(yaml_file, "Textures", "Surround", "Nature1", "Path_1")
                mixtex_region1loco_path = get_yaml(yaml_file, "Textures", "Surround", "Region1Loco", "Path")

                mixtex_nature1_list_1 = get_yaml(yaml_file, "Textures", "Surround", "Nature1", "Files_1")
                mixtex_region1loco_file = get_yaml(yaml_file, "Textures", "Surround", "Region1Loco", "File")

                if current_dir(mixtex_nature1_path_1, workpath):
                    rename(mixtex_nature1_list_1, "_19", need_list_changing=1)
                    move(mixtex_nature1_list_1, mix_folder_path, workpath)

                    include(mixtex_nature1_list_1, files_to_mix)
                
                if current_dir(mixtex_region1loco_path, workpath):
                    move(mixtex_region1loco_file, mix_folder_path, workpath)
                    
                    include (mixtex_region1loco_file, files_to_mix)
            
            if current_dir(mixtex_path, workpath):
                move(mixtex_list, mix_folder_path, workpath)
            
            if current_dir(mixtex_all_path, workpath):
                rename(mixtex_all_list, "_0", need_list_changing=1)
                move(mixtex_all_list, mix_folder_path, workpath)

            if current_dir(mixtex_detail_path, workpath):
                move(mixtex_detail_list, mix_folder_path, workpath)

            if current_dir(mixtex_factory_path, workpath):
                move(mixtex_factory_list, mix_folder_path, workpath)

            if current_dir(mixtex_kladbische_path, workpath):
                rename(mixtex_kladbische_list, "_1", need_list_changing=1)
                move(mixtex_kladbische_list, mix_folder_path, workpath)

            if current_dir(mixtex_misc_path, workpath):
                move(mixtex_misc_list, mix_folder_path, workpath)

            if current_dir(mixtex_region1_path, workpath):
                rename(mixtex_region1_list, "_2", need_list_changing=1)
                move(mixtex_region1_list, mix_folder_path, workpath)

            if current_dir(mixtex_region2_path, workpath):
                move(mixtex_region2_list, mix_folder_path, workpath)

            if current_dir(mixtex_region3_path, workpath):
                move(mixtex_region3_list, mix_folder_path, workpath)

            if current_dir(mixtex_region4_path, workpath):
                move(mixtex_region4_list, mix_folder_path, workpath)

            if current_dir(mixtex_special_path, workpath):
                rename(mixtex_special_list, "_3", need_list_changing=1)
                move(mixtex_special_list, mix_folder_path, workpath)

            if current_dir(mixtex_boss02_path, workpath):
                move(mixtex_boss02_list, mix_folder_path, workpath)

            if current_dir(mixtex_boss04_path, workpath):
                move(mixtex_boss04_list, mix_folder_path, workpath)

            if current_dir(mixtex_submarina_path, workpath):
                rename(mixtex_submarina_list, "_4", need_list_changing=1)
                move(mixtex_submarina_list, mix_folder_path, workpath)

            if current_dir(mixtex_submarine_path, workpath):
                rename(mixtex_submarine_list, "_5", need_list_changing=1)
                move(mixtex_submarine_list, mix_folder_path, workpath)

            if current_dir(mixtex_questitems_path, workpath):
                move(mixtex_questitems_list, mix_folder_path, workpath)

            if current_dir(mixtex_grass1_path, workpath):
                move(mixtex_grass1_list, mix_folder_path, workpath)

            if current_dir(mixtex_grass3_path, workpath):
                rename(mixtex_grass3_list, "_6", need_list_changing=1)
                move(mixtex_grass3_list, mix_folder_path, workpath)

            if current_dir(mixtex_grass4_path, workpath):
                move(mixtex_grass4_list, mix_folder_path, workpath)

            if current_dir(mixtex_nature1_path, workpath):
                move(mixtex_nature1_list, mix_folder_path, workpath)

            if current_dir(mixtex_nature2_path, workpath):
                move(mixtex_nature2_list, mix_folder_path, workpath)

            if current_dir(mixtex_nature3_path, workpath):
                move(mixtex_nature3_list, mix_folder_path, workpath)

            if current_dir(mixtex_nature4_path, workpath):
                move(mixtex_nature4_list, mix_folder_path, workpath)

            if current_dir(mixtex_goods_path, workpath):
                move(mixtex_goods_list, mix_folder_path, workpath)

            if current_dir(mixtex_brige_tube_path, workpath):
                rename(mixtex_brige_tube_list, "_7", need_list_changing=1)
                move(mixtex_brige_tube_list, mix_folder_path, workpath)

            if current_dir(mixtex_boss04_drone_path, workpath):
                rename(mixtex_boss04_drone_list, "_8", need_list_changing=1)
                move(mixtex_boss04_drone_list, mix_folder_path, workpath)

            if current_dir(mixtex_rally_path, workpath):
                move(mixtex_rally_list, mix_folder_path, workpath)

            if current_dir(mixtex_nlo_path, workpath):
                rename(mixtex_nlo_list, "_9", need_list_changing=1)
                move(mixtex_nlo_list, mix_folder_path, workpath)

            if current_dir(mixtex_buildings_region2_path, workpath):
                move(mixtex_buildings_region2_list, mix_folder_path, workpath)

            if current_dir(mixtex_gadgets_path, workpath):
                move(mixtex_gadgets_list, mix_folder_path, workpath)

            if current_dir(mixtex_objects_path, workpath):
                move(mixtex_objects_list, mix_folder_path, workpath)

            if current_dir(mixtex_masks_1_man_path, workpath):
                rename(mixtex_masks_1_man_list, "_10", need_list_changing=1)
                move(mixtex_masks_1_man_list, mix_folder_path, workpath)

            if current_dir(mixtex_masks_1_woman_path, workpath):
                rename(mixtex_masks_1_woman_list, "_11", need_list_changing=1)
                move(mixtex_masks_1_woman_list, mix_folder_path, workpath)

            if current_dir(mixtex_masks_2_man_path, workpath):
                rename(mixtex_masks_2_man_list, "_12", need_list_changing=1)
                move(mixtex_masks_2_man_list, mix_folder_path, workpath)

            if current_dir(mixtex_masks_2_woman_path, workpath):
                rename(mixtex_masks_2_woman_list, "_13", need_list_changing=1)
                move(mixtex_masks_2_woman_list, mix_folder_path, workpath)

            if current_dir(mixtex_masks_3_man_path, workpath):
                rename(mixtex_masks_3_man_list, "_14", need_list_changing=1)
                move(mixtex_masks_3_man_list, mix_folder_path, workpath)

            if current_dir(mixtex_masks_4_man_path, workpath):
                move(mixtex_masks_4_man_list, mix_folder_path, workpath)

            if current_dir(mixtex_masks_main_path, workpath):
                rename(mixtex_masks_main_list, "_15", need_list_changing=1)
                move(mixtex_masks_main_list, mix_folder_path, workpath)

            if current_dir(mixtex_ammo_path, workpath):
                move(mixtex_ammo_list, mix_folder_path, workpath)

            if current_dir(mixtex_guns_path, workpath):
                rename(mixtex_guns_list, "_16", need_list_changing=1)
                move(mixtex_guns_list, mix_folder_path, workpath)

            if current_dir(mixtex_objectbox_path, workpath):
                move(mixtex_objectbox_file, mix_folder_path, workpath)

            if current_dir(mixtex_objectconteiner_path, workpath):
                mixtex_objectconteiner_file = rename(mixtex_objectconteiner_file, "_17") 
                move(mixtex_objectconteiner_file, mix_folder_path, workpath)

            if current_dir(mixtex_objectprovoda_path, workpath):
                move(mixtex_objectprovoda_file, mix_folder_path, workpath)

            if current_dir(mixtex_boss01_path, workpath):
                mixtex_boss01_file = rename(mixtex_boss01_file, "_18")
                move(mixtex_boss01_file, mix_folder_path, workpath)

            if current_dir(mixtex_boss03_path, workpath):
                move(mixtex_boss03_file, mix_folder_path, workpath)

            if current_dir(mixtex_region1benhouse_path, workpath):
                move(mixtex_region1benhouse_file, mix_folder_path, workpath)

            if current_dir(mixtex_cliffsr2_path, workpath):
                move(mixtex_cliffsr2_file, mix_folder_path, workpath)

            if current_dir(mix_folder_path, workpath):
                include([mixtex_all_list, mixtex_detail_list, mixtex_factory_list, mixtex_kladbische_list, mixtex_misc_list, 
                         mixtex_region1_list, mixtex_region2_list, mixtex_region3_list, mixtex_region4_list, mixtex_special_list, 
                         mixtex_boss02_list, mixtex_boss04_list, mixtex_submarina_list, mixtex_submarine_list, mixtex_questitems_list, 
                         mixtex_grass1_list, mixtex_grass3_list, mixtex_grass4_list, mixtex_nature1_list, mixtex_nature2_list, 
                         mixtex_nature3_list, mixtex_nature4_list, mixtex_goods_list, mixtex_brige_tube_list, mixtex_boss04_drone_list, 
                         mixtex_rally_list, mixtex_nlo_list, mixtex_buildings_region2_list, mixtex_gadgets_list, mixtex_objects_list, 
                         mixtex_masks_1_man_list, mixtex_masks_1_woman_list, mixtex_masks_2_man_list, mixtex_masks_2_woman_list, 
                         mixtex_masks_3_man_list, mixtex_masks_4_man_list, mixtex_masks_main_list, mixtex_ammo_list, mixtex_guns_list, 
                         mixtex_list, mixtex_objectbox_file, mixtex_objectconteiner_file, mixtex_objectprovoda_file, mixtex_boss01_file, 
                         mixtex_boss03_file, mixtex_region1benhouse_file, mixtex_cliffsr2_file], files_to_mix)

                randomize(files_to_mix)

                copy(mixtex_forcopying_file, mixtex_forcopying_path, workpath)

                move(mixtex_list, mixtex_path, workpath)
                move(mixtex_all_list, mixtex_all_path, workpath)
                move(mixtex_detail_list, mixtex_detail_path, workpath)
                move(mixtex_factory_list, mixtex_factory_path, workpath)
                move(mixtex_kladbische_list, mixtex_kladbische_path, workpath)
                move(mixtex_misc_list, mixtex_misc_path, workpath)
                move(mixtex_region1_list, mixtex_region1_path, workpath)
                move(mixtex_region2_list, mixtex_region2_path, workpath)
                move(mixtex_region3_list, mixtex_region3_path, workpath)
                move(mixtex_region4_list, mixtex_region4_path, workpath)
                move(mixtex_special_list, mixtex_special_path, workpath)
                move(mixtex_boss02_list, mixtex_boss02_path, workpath)
                move(mixtex_boss04_list, mixtex_boss04_path, workpath)
                move(mixtex_submarina_list, mixtex_submarina_path, workpath)
                move(mixtex_submarine_list, mixtex_submarine_path, workpath)
                move(mixtex_questitems_list, mixtex_questitems_path, workpath)
                move(mixtex_grass1_list, mixtex_grass1_path, workpath)
                move(mixtex_grass3_list, mixtex_grass3_path, workpath)
                move(mixtex_grass4_list, mixtex_grass4_path, workpath)
                move(mixtex_nature1_list, mixtex_nature1_path, workpath)
                move(mixtex_nature2_list, mixtex_nature2_path, workpath)
                move(mixtex_nature3_list, mixtex_nature3_path, workpath)
                move(mixtex_nature4_list, mixtex_nature4_path, workpath)
                move(mixtex_goods_list, mixtex_goods_path, workpath)
                move(mixtex_brige_tube_list, mixtex_brige_tube_path, workpath)
                move(mixtex_boss04_drone_list, mixtex_boss04_drone_path, workpath)
                move(mixtex_rally_list, mixtex_rally_path, workpath)
                move(mixtex_nlo_list, mixtex_nlo_path, workpath)
                move(mixtex_buildings_region2_list, mixtex_buildings_region2_path, workpath)
                move(mixtex_gadgets_list, mixtex_gadgets_path, workpath)
                move(mixtex_objects_list, mixtex_objects_path, workpath)
                move(mixtex_masks_1_man_list, mixtex_masks_1_man_path, workpath)
                move(mixtex_masks_1_woman_list, mixtex_masks_1_woman_path, workpath)
                move(mixtex_masks_2_man_list, mixtex_masks_2_man_path, workpath)
                move(mixtex_masks_2_woman_list, mixtex_masks_2_woman_path, workpath)
                move(mixtex_masks_3_man_list, mixtex_masks_3_man_path, workpath)
                move(mixtex_masks_4_man_list, mixtex_masks_4_man_path, workpath)
                move(mixtex_masks_main_list, mixtex_masks_main_path, workpath)
                move(mixtex_ammo_list, mixtex_ammo_path, workpath)
                move(mixtex_guns_list, mixtex_guns_path, workpath)
                move(mixtex_objectbox_file, mixtex_objectbox_path, workpath)
                move(mixtex_objectconteiner_file, mixtex_objectconteiner_path, workpath)
                move(mixtex_objectprovoda_file, mixtex_objectprovoda_path, workpath)
                move(mixtex_boss01_file, mixtex_boss01_path, workpath)
                move(mixtex_boss03_file, mixtex_boss03_path, workpath)
                move(mixtex_region1benhouse_file, mixtex_region1benhouse_path, workpath)
                move(mixtex_cliffsr2_file, mixtex_cliffsr2_path, workpath)

                if gameversion == "ImprovedStoryline":
                    move(mixtex_nature1_list_1, mixtex_nature1_path_1, workpath)
                    move(mixtex_region1loco_file, mixtex_region1loco_path, workpath)

                    if current_dir(mixtex_nature1_path_1, workpath):
                        rename(mixtex_nature1_list_1, "_19", backward=1)

                if current_dir(mixtex_all_path, workpath):
                    rename(mixtex_all_list, "_0", backward=1)

                if current_dir(mixtex_kladbische_path, workpath):
                    rename(mixtex_kladbische_list, "_1", backward=1)

                if current_dir(mixtex_region1_path, workpath):
                    rename(mixtex_region1_list, "_2", backward=1)

                if current_dir(mixtex_special_path, workpath):
                    rename(mixtex_special_list, "_3", backward=1)

                if current_dir(mixtex_submarina_path, workpath):
                    rename(mixtex_submarina_list, "_4", backward=1)

                if current_dir(mixtex_submarine_path, workpath):
                    rename(mixtex_submarine_list, "_5", backward=1)

                if current_dir(mixtex_grass3_path, workpath):
                    rename(mixtex_grass3_list, "_6", backward=1)

                if current_dir(mixtex_brige_tube_path, workpath):
                    rename(mixtex_brige_tube_list, "_7", backward=1)

                if current_dir(mixtex_boss04_drone_path, workpath):
                    rename(mixtex_boss04_drone_list, "_8", backward=1)

                if current_dir(mixtex_nlo_path, workpath):
                    rename(mixtex_nlo_list, "_9", backward=1)

                if current_dir(mixtex_masks_1_man_path, workpath):
                    rename(mixtex_masks_1_man_list, "_10", backward=1)

                if current_dir(mixtex_masks_1_woman_path, workpath):
                    rename(mixtex_masks_1_woman_list, "_11", backward=1)

                if current_dir(mixtex_masks_2_man_path, workpath):
                    rename(mixtex_masks_2_man_list, "_12", backward=1)

                if current_dir(mixtex_masks_2_woman_path, workpath):
                    rename(mixtex_masks_2_woman_list, "_13", backward=1)

                if current_dir(mixtex_masks_3_man_path, workpath):
                    rename(mixtex_masks_3_man_list, "_14", backward=1)

                if current_dir(mixtex_masks_main_path, workpath):
                    rename(mixtex_masks_main_list, "_15", backward=1)

                if current_dir(mixtex_guns_path, workpath):
                    rename(mixtex_guns_list, "_16", backward=1)

                if current_dir(mixtex_objectconteiner_path, workpath):
                    rename(mixtex_objectconteiner_file, "_17", backward=1) 

                if current_dir(mixtex_boss01_path, workpath):
                    rename(mixtex_boss01_file, "_18", backward=1)

                show_success("Textures : Surround", mainwindow)
            else:
                show_failure("Textures : Surround", mainwindow)
        else:
            logger.info("SKIPPED: Textures : Surround")
        
        # Textures: Masks
        if settings["Settings"]["Checkboxes"]["Textures"]["Masks"] == True:

            # Textures: Masks: Group0
            mixhmasks_1_2_path_1 = get_yaml(yaml_file, "Textures", "Masks", "Group0", "Paths", 0)
            mixhmasks_1_2_path_2 = get_yaml(yaml_file, "Textures", "Masks", "Group0", "Paths", 1)
            mixhmasks_1_2_list = get_yaml(yaml_file, "Textures", "Masks", "Group0", "Files")
            if gameversion == "ImprovedStoryline":
                mixhmasks_1_2_list_1 = get_yaml(yaml_file, "Textures", "Masks", "Group0", "Files_1")

            if current_dir(mixhmasks_1_2_path_1, workpath):
                randomize(mixhmasks_1_2_list)

                if current_dir(mixhmasks_1_2_path_2, workpath):

                    if gameversion == "ImprovedStoryline":
                        randomize(mixhmasks_1_2_list_1)
                    else:
                        randomize(mixhmasks_1_2_list)

                    show_success("Textures : Masks : Group0", mainwindow)
                else:
                    show_failure("Textures : Masks : Group0", mainwindow)
            else:
                show_failure("Textures : Masks : Group0", mainwindow)

            # Textures: Masks: Group1
            mixhmasks_region1_path = get_yaml(yaml_file, "Textures", "Masks", "Group1", "Region1", "Path")
            mixhmasks_region2_path = get_yaml(yaml_file, "Textures", "Masks", "Group1", "Region2", "Path")
            mixhmasks_main_path = get_yaml(yaml_file, "Textures", "Masks", "Group1", "Main", "Path")
            mixhmasks_path = get_yaml(yaml_file, "Textures", "Masks", "Group1", "Masks", "Path")
            mixhmasks_copy_path = get_yaml(yaml_file, "Textures", "Masks", "Group1", "ForCopying", "PathTo")

            mixhmasks_region1_list = get_yaml(yaml_file, "Textures", "Masks", "Group1", "Region1", "Files")
            mixhmasks_region2_list = get_yaml(yaml_file, "Textures", "Masks", "Group1", "Region2", "Files")
            mixhmasks_main_file = get_yaml(yaml_file, "Textures", "Masks", "Group1", "Main", "File")
            mixhmasks_list = get_yaml(yaml_file, "Textures", "Masks", "Group1", "Masks", "Files")
            mixhmasks_copy_list = get_yaml(yaml_file, "Textures", "Masks", "Group1", "ForCopying", "Files")
            files_to_mix = []

            if current_dir(mixhmasks_region1_path, workpath):
                rename(mixhmasks_region1_list, "_0", need_list_changing=1)
                move(mixhmasks_region1_list, mix_folder_path, workpath)
            
            if current_dir(mixhmasks_region2_path, workpath):
                move(mixhmasks_region2_list, mix_folder_path, workpath)

            if current_dir(mixhmasks_main_path, workpath):
                move(mixhmasks_main_file, mix_folder_path, workpath)

            if current_dir(mixhmasks_path, workpath):
                move(mixhmasks_list, mix_folder_path, workpath)

            if current_dir(mix_folder_path, workpath):
                include([mixhmasks_region1_list, mixhmasks_region2_list, mixhmasks_main_file, mixhmasks_list], 
                        files_to_mix)
                randomize(files_to_mix)

                copy(mixhmasks_copy_list, mixhmasks_copy_path, workpath)

                move(mixhmasks_region1_list, mixhmasks_region1_path, workpath)
                move(mixhmasks_region2_list, mixhmasks_region2_path, workpath)
                move(mixhmasks_main_file, mixhmasks_main_path, workpath)
                move(mixhmasks_list, mixhmasks_path, workpath)

                if current_dir(mixhmasks_region1_path, workpath):
                    rename(mixhmasks_region1_list, "_0", backward=1)

                show_success("Textures : Masks : Group1", mainwindow)
            else:
                show_failure("Textures : Masks : Group1", mainwindow)
        else:
            logger.info("SKIPPED: Textures : Masks")
        
        # Textures: VehicleSkins
        if settings["Settings"]["Checkboxes"]["Textures"]["VehicleSkins"] == True:

            # Textures: VehicleSkins: Belaz
            belaz_skin_path = get_yaml(yaml_file, "Textures", "VehicleSkins", "Belaz", "Path")
            
            belaz_cab_1_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Belaz", "Files", "Group0")
            belaz_cab_2_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Belaz", "Files", "Group1")
            belaz_cab_3_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Belaz", "Files", "Group2")
            belaz_cab_4_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Belaz", "Files", "Group3")
            belaz_cargo_1_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Belaz", "Files", "Group4")
            belaz_cargo_2_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Belaz", "Files", "Group5")
            belaz_cargo_3_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Belaz", "Files", "Group6")
            belaz_cargo_4_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Belaz", "Files", "Group7")
            belaz_chassis_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Belaz", "Files", "Group8")
            belaz_wheel_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Belaz", "Files", "Group9")

            if current_dir(belaz_skin_path, workpath):
                for belaz_list in [belaz_cab_1_list, belaz_cab_2_list, belaz_cab_3_list, belaz_cab_4_list, 
                                   belaz_cargo_1_list, belaz_cargo_2_list, belaz_cargo_3_list, belaz_cargo_4_list, 
                                   belaz_chassis_list, belaz_wheel_list]:
                    randomize(belaz_list)
            
                show_success("Textures : VehicleSkins : Belaz", mainwindow)
            else:
                show_failure("Textures : VehicleSkins : Belaz", mainwindow)

            # Textures: VehicleSkins: Bug
            bug_skin_path = get_yaml(yaml_file, "Textures", "VehicleSkins", "Bug", "Path")

            bug_cab_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Bug", "Files", "Group0")
            bug_cargo_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Bug", "Files", "Group1")
            bug_cargo_detal_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Bug", "Files", "Group2")

            if current_dir(bug_skin_path, workpath):
                for bug_list in [bug_cab_list, bug_cargo_list, bug_cargo_detal_list]:
                    randomize(bug_list)
            
                show_success("Textures : VehicleSkins : Bug", mainwindow)
            else:
                show_failure("Textures : VehicleSkins : Bug", mainwindow)

            # Textures: VehicleSkins: Cruiser
            cruiser_skin_path = get_yaml(yaml_file, "Textures", "VehicleSkins", "Cruiser", "Path")

            cruiser_cab_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Cruiser", "Files", "Group0")
            cruiser_cab_detal_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Cruiser", "Files", "Group1")

            if current_dir(cruiser_skin_path, workpath):
                for cruiser_list in [cruiser_cab_list, cruiser_cab_detal_list]:
                    randomize(cruiser_list)
            
                show_success("Textures : VehicleSkins : Cruiser", mainwindow)
            else:
                show_failure("Textures : VehicleSkins : Cruiser", mainwindow)

            # Textures: VehicleSkins: Fighter
            fighter_skin_path = get_yaml(yaml_file, "Textures", "VehicleSkins", "Fighter", "Path")
            fighter_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Fighter", "Files")

            if current_dir(fighter_skin_path, workpath):
                randomize(fighter_list)

                show_success("Textures : VehicleSkins : Fighter", mainwindow)
            else:
                show_failure("Textures : VehicleSkins : Fighter", mainwindow)

            # Textures: VehicleSkins: Hunter
            hunter_skin_path = get_yaml(yaml_file, "Textures", "VehicleSkins", "Hunter", "Path")
            hunter_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Hunter", "Files")

            if current_dir(hunter_skin_path, workpath):
                randomize(hunter_list)

                show_success("Textures : VehicleSkins : Hunter", mainwindow)
            else:
                show_failure("Textures : VehicleSkins : Hunter", mainwindow)

            # Textures: VehicleSkins: Mirotvorec
            mirotvorec_skin_path = get_yaml(yaml_file, "Textures", "VehicleSkins", "Mirotvorec", "Path")

            mirotvorec_cab_1_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Mirotvorec", "Files", "Group0")
            mirotvorec_cab_2_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Mirotvorec", "Files", "Group1")
            mirotvorec_cargo_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Mirotvorec", "Files", "Group2")
            mirotvorec_wheel_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Mirotvorec", "Files", "Group3")

            if current_dir(mirotvorec_skin_path, workpath):
                for mirotvorec_list in [mirotvorec_cab_1_list, mirotvorec_cab_2_list, mirotvorec_cargo_list, mirotvorec_wheel_list]:
                    randomize(mirotvorec_list)
            
                show_success("Textures : VehicleSkins : Mirotvorec", mainwindow)
            else:
                show_failure("Textures : VehicleSkins : Mirotvorec", mainwindow)

            # Textures : VehicleSkins : Molokovoz
            molokovoz_skin_path = get_yaml(yaml_file, "Textures", "VehicleSkins", "Molokovoz", "Path")

            molokovoz_cab_1_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Molokovoz", "Files", "Group0")
            molokovoz_cab_2_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Molokovoz", "Files", "Group1")
            molokovoz_cargo_1_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Molokovoz", "Files", "Group2")
            molokovoz_cargo_2_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Molokovoz", "Files", "Group3")
            molokovoz_cargo_3_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Molokovoz", "Files", "Group4")
            molokovoz_wheel_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Molokovoz", "Files", "Group5")

            if current_dir(molokovoz_skin_path, workpath):
                for molokovoz_list in [molokovoz_cab_1_list, molokovoz_cab_2_list, molokovoz_cargo_1_list, 
                                       molokovoz_cargo_2_list, molokovoz_cargo_3_list, molokovoz_wheel_list]:
                    randomize(molokovoz_list)
            
                show_success("Textures : VehicleSkins : Molokovoz", mainwindow)
            else:
                show_failure("Textures : VehicleSkins : Molokovoz", mainwindow)

            # Textures : VehicleSkins : Scout
            scout_skin_path = get_yaml(yaml_file, "Textures", "VehicleSkins", "Scout", "Path")
            scout_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Scout", "Files")

            if current_dir(scout_skin_path, workpath):
                randomize(scout_list)

                show_success("Textures : VehicleSkins : Scout", mainwindow)
            else:
                show_failure("Textures : VehicleSkins : Scout", mainwindow)

            # Textures : VehicleSkins : SmallCars
            smallcars_skin_path = get_yaml(yaml_file, "Textures", "VehicleSkins", "SmallCars", "Path")

            small_car_cab_1_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "SmallCars", "Files", "Group0")
            small_car_cab_2_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "SmallCars", "Files", "Group1")

            if current_dir(smallcars_skin_path, workpath):
                for small_car_list in [small_car_cab_1_list, small_car_cab_2_list]:
                    randomize(small_car_list)

                show_success("Textures : VehicleSkins : SmallCars", mainwindow)
            else:
                show_failure("Textures : VehicleSkins : SmallCars", mainwindow)

            # Textures : VehicleSkins : Ural
            ural_skin_path = get_yaml(yaml_file, "Textures", "VehicleSkins", "Ural", "Path")

            ural_cab_1_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Ural", "Files", "Group0")
            ural_cab_2_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Ural", "Files", "Group1")
            ural_cab_3_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Ural", "Files", "Group2")
            ural_cargo_1_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Ural", "Files", "Group3")
            ural_cargo_2_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Ural", "Files", "Group4")
            ural_cargo_3_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Ural", "Files", "Group5")
            ural_cargo_4_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Ural", "Files", "Group6")
            ural_shield_1_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Ural", "Files", "Group7")
            ural_shield_2_list = get_yaml(yaml_file, "Textures", "VehicleSkins", "Ural", "Files", "Group8")

            if current_dir(ural_skin_path, workpath):
                for ural_list in [ural_cab_1_list, ural_cab_2_list, ural_cab_3_list, ural_cargo_1_list, ural_cargo_2_list, 
                                ural_cargo_3_list, ural_cargo_4_list, ural_shield_1_list, ural_shield_2_list]:
                    randomize(ural_list)

                show_success("Textures : VehicleSkins : Ural", mainwindow)
            else:
                show_failure("Textures : VehicleSkins : Ural", mainwindow)

        else:
            logger.info("SKIPPED: Textures: VehicleSkins")
        
        # Textures: Lightmaps
        if settings["Settings"]["Checkboxes"]["Textures"]["Lightmaps"] == True:
            mixlmaps_mainmenu_path = get_yaml(yaml_file, "Textures", "Lightmaps", "mainmenu", "Path")
            mixlmaps_r1m1_path = get_yaml(yaml_file, "Textures", "Lightmaps", "r1m1", "Path")
            mixlmaps_r1m2_path = get_yaml(yaml_file, "Textures", "Lightmaps", "r1m2", "Path")
            mixlmaps_r1m3_path = get_yaml(yaml_file, "Textures", "Lightmaps", "r1m3", "Path")
            mixlmaps_r1m4_path = get_yaml(yaml_file, "Textures", "Lightmaps", "r1m4", "Path")
            mixlmaps_r2m1_path = get_yaml(yaml_file, "Textures", "Lightmaps", "r2m1", "Path")
            mixlmaps_r2m2_path = get_yaml(yaml_file, "Textures", "Lightmaps", "r2m2", "Path")
            mixlmaps_r3m1_path = get_yaml(yaml_file, "Textures", "Lightmaps", "r3m1", "Path")
            mixlmaps_r3m2_path = get_yaml(yaml_file, "Textures", "Lightmaps", "r3m2", "Path")
            mixlmaps_r4m1_path = get_yaml(yaml_file, "Textures", "Lightmaps", "r4m1", "Path")
            mixlmaps_r4m2_path = get_yaml(yaml_file, "Textures", "Lightmaps", "r4m2", "Path")

            mixlmaps_mainmenu_list = get_yaml(yaml_file, "Textures", "Lightmaps", "mainmenu", "Files")
            mixlmaps_r1m1_list = get_yaml(yaml_file, "Textures", "Lightmaps", "r1m1", "Files")
            mixlmaps_r1m2_list = get_yaml(yaml_file, "Textures", "Lightmaps", "r1m2", "Files")
            mixlmaps_r1m3_list = get_yaml(yaml_file, "Textures", "Lightmaps", "r1m3", "Files")
            mixlmaps_r1m4_list = get_yaml(yaml_file, "Textures", "Lightmaps", "r1m4", "Files")
            mixlmaps_r2m1_list = get_yaml(yaml_file, "Textures", "Lightmaps", "r2m1", "Files")
            mixlmaps_r2m2_list = get_yaml(yaml_file, "Textures", "Lightmaps", "r2m2", "Files")
            mixlmaps_r3m1_list = get_yaml(yaml_file, "Textures", "Lightmaps", "r3m1", "Files")
            mixlmaps_r3m2_list = get_yaml(yaml_file, "Textures", "Lightmaps", "r3m2", "Files")
            mixlmaps_r4m1_list = get_yaml(yaml_file, "Textures", "Lightmaps", "r4m1", "Files")
            mixlmaps_r4m2_list = get_yaml(yaml_file, "Textures", "Lightmaps", "r4m2", "Files")

            if gameversion == "ImprovedStoryline":
                mixlmaps_r1m5_path = get_yaml(yaml_file, "Textures", "Lightmaps", "r1m5", "Path")
                mixlmaps_r1m6_path = get_yaml(yaml_file, "Textures", "Lightmaps", "r1m6", "Path")
                mixlmaps_r1m7_path = get_yaml(yaml_file, "Textures", "Lightmaps", "r1m7", "Path")

                mixlmaps_r1m5_list = get_yaml(yaml_file, "Textures", "Lightmaps", "r1m5", "Files")
                mixlmaps_r1m6_list = get_yaml(yaml_file, "Textures", "Lightmaps", "r1m6", "Files")
                mixlmaps_r1m7_list = get_yaml(yaml_file, "Textures", "Lightmaps", "r1m7", "Files")

            files_to_mix = []

            if current_dir(mixlmaps_mainmenu_path, workpath):
                move(mixlmaps_mainmenu_list, mix_folder_path, workpath)
            
            if current_dir(mixlmaps_r1m1_path, workpath):
                move(mixlmaps_r1m1_list, mix_folder_path, workpath)

            if current_dir(mixlmaps_r1m2_path, workpath):
                move(mixlmaps_r1m2_list, mix_folder_path, workpath)

            if current_dir(mixlmaps_r1m3_path, workpath):
                move(mixlmaps_r1m3_list, mix_folder_path, workpath)

            if current_dir(mixlmaps_r1m4_path, workpath):
                move(mixlmaps_r1m4_list, mix_folder_path, workpath)

            if current_dir(mixlmaps_r2m1_path, workpath):
                rename(mixlmaps_r2m1_list, "_0", need_list_changing=1)
                move(mixlmaps_r2m1_list, mix_folder_path, workpath)

            if current_dir(mixlmaps_r2m2_path, workpath):
                rename(mixlmaps_r2m2_list, "_1", need_list_changing=1)
                move(mixlmaps_r2m2_list, mix_folder_path, workpath)

            if current_dir(mixlmaps_r3m1_path, workpath):
                move(mixlmaps_r3m1_list, mix_folder_path, workpath)

            if current_dir(mixlmaps_r3m2_path, workpath):
                move(mixlmaps_r3m2_list, mix_folder_path, workpath)

            if current_dir(mixlmaps_r4m1_path, workpath):
                move(mixlmaps_r4m1_list, mix_folder_path, workpath)

            if current_dir(mixlmaps_r4m2_path, workpath):
                move(mixlmaps_r4m2_list, mix_folder_path, workpath)
            
            if gameversion == "ImprovedStoryline":
                if current_dir(mixlmaps_r1m5_path, workpath):
                    move(mixlmaps_r1m5_list, mix_folder_path, workpath)
                
                if current_dir(mixlmaps_r1m6_path, workpath):
                    rename(mixlmaps_r1m6_list, "_2", need_list_changing=1)
                    move(mixlmaps_r1m6_list, mix_folder_path, workpath)
                
                if current_dir(mixlmaps_r1m7_path, workpath):
                    rename(mixlmaps_r1m7_list, "_3", need_list_changing=1)
                    move(mixlmaps_r1m7_list, mix_folder_path, workpath)

            if current_dir(mix_folder_path, workpath):
                include([mixlmaps_r1m1_list, mixlmaps_r1m2_list, mixlmaps_r1m3_list, mixlmaps_r1m4_list, mixlmaps_r2m1_list, 
                         mixlmaps_r2m2_list, mixlmaps_r3m1_list, mixlmaps_r3m2_list, mixlmaps_r4m1_list, mixlmaps_r4m2_list, 
                         mixlmaps_mainmenu_list], files_to_mix)
                randomize(files_to_mix)

                move(mixlmaps_mainmenu_list, mixlmaps_mainmenu_path, workpath)
                move(mixlmaps_r1m1_list, mixlmaps_r1m1_path, workpath)
                move(mixlmaps_r1m2_list, mixlmaps_r1m2_path, workpath)
                move(mixlmaps_r1m3_list, mixlmaps_r1m3_path, workpath)
                move(mixlmaps_r1m4_list, mixlmaps_r1m4_path, workpath)
                move(mixlmaps_r2m1_list, mixlmaps_r2m1_path, workpath)
                move(mixlmaps_r2m2_list, mixlmaps_r2m2_path, workpath)
                move(mixlmaps_r3m1_list, mixlmaps_r3m1_path, workpath)
                move(mixlmaps_r3m2_list, mixlmaps_r3m2_path, workpath)
                move(mixlmaps_r4m1_list, mixlmaps_r4m1_path, workpath)
                move(mixlmaps_r4m2_list, mixlmaps_r4m2_path, workpath)

                if gameversion == "ImprovedStoryline":
                    move(mixlmaps_r1m5_list, mixlmaps_r1m5_path, workpath)
                    move(mixlmaps_r1m6_list, mixlmaps_r1m6_path, workpath)
                    move(mixlmaps_r1m7_list, mixlmaps_r1m7_path, workpath)

                    if current_dir(mixlmaps_r1m6_path, workpath):
                        rename(mixlmaps_r1m6_list, "_2", backward=1)
                    if current_dir(mixlmaps_r1m7_path, workpath):
                        rename(mixlmaps_r1m7_list, "_3", backward=1)

                if current_dir(mixlmaps_r2m1_path, workpath):
                    rename(mixlmaps_r2m1_list, "_0", backward=1)

                if current_dir(mixlmaps_r2m2_path, workpath):
                    rename(mixlmaps_r2m2_list, "_1", backward=1)
                
                show_success("Textures : Lightmaps", mainwindow)
            else:
                show_failure("Textures : Lightmaps", mainwindow)
        else:
            logger.info("SKIPPED: Textures : Lightmaps")
        
        # Textures: WeatherTex
        if settings["Settings"]["Checkboxes"]["Textures"]["WeatherTex"] == True:
            mixwtex_path = get_yaml(yaml_file, "Textures", "WeatherTex", "Path")
            mixwtex_list = get_yaml(yaml_file, "Textures", "WeatherTex", "Files")

            if current_dir(mixwtex_path, workpath):
                randomize(mixwtex_list)

                show_success("Textures : WeatherTex", mainwindow)
            else:
                show_failure("Textures : WeatherTex", mainwindow)
        else:
            logger.info("SKIPPED: Textures : WeatherTex")
        
        # Textures: Tiles
        if settings["Settings"]["Checkboxes"]["Textures"]["Tiles"] == True:
            mixtiles_region1_path = get_yaml(yaml_file, "Textures", "Tiles", "Region1", "Path")
            mixtiles_region2_path = get_yaml(yaml_file, "Textures", "Tiles", "Region2", "Path")
            mixtiles_region3_path = get_yaml(yaml_file, "Textures", "Tiles", "Region3", "Path")
            mixtiles_region4_path = get_yaml(yaml_file, "Textures", "Tiles", "Region4", "Path")

            mixtiles_region1_list = get_yaml(yaml_file, "Textures", "Tiles", "Region1", "Files")
            mixtiles_region2_list = get_yaml(yaml_file, "Textures", "Tiles", "Region2", "Files")
            mixtiles_region3_list = get_yaml(yaml_file, "Textures", "Tiles", "Region3", "Files")
            mixtiles_region4_list = get_yaml(yaml_file, "Textures", "Tiles", "Region4", "Files")
            files_to_mix = []

            if current_dir(mixtiles_region1_path, workpath):
                move(mixtiles_region1_list, mix_folder_path, workpath)

            if current_dir(mixtiles_region2_path, workpath):
                move(mixtiles_region2_list, mix_folder_path, workpath)

            if current_dir(mixtiles_region3_path, workpath):
                move(mixtiles_region3_list, mix_folder_path, workpath)

            if current_dir(mixtiles_region4_path, workpath):
                move(mixtiles_region4_list, mix_folder_path, workpath)

            if current_dir(mix_folder_path, workpath):
                include([mixtiles_region1_list, mixtiles_region2_list, mixtiles_region3_list, 
                    mixtiles_region4_list], files_to_mix)
                randomize(files_to_mix)

                move(mixtiles_region1_list, mixtiles_region1_path, workpath)
                move(mixtiles_region2_list, mixtiles_region2_path, workpath)
                move(mixtiles_region3_list, mixtiles_region3_path, workpath)
                move(mixtiles_region4_list, mixtiles_region4_path, workpath)

                show_success("Textures : Tiles", mainwindow)
            else:
                show_failure("Textures : Tiles", mainwindow)
        else:
            logger.info("SKIPPED: Textures : Tiles")
        
        # Other: Weather
        if settings["Settings"]["Checkboxes"]["Other"]["Weather"] == True:
            weather_path = get_yaml(yaml_file, "Other", "Weather", "Path")
            weather_file = get_yaml(yaml_file, "Other", "Weather", "File")
            weather_tree = parse(weather_path, workpath, weather_file)
            weather_list = []

            if weather_tree:
                for name in weather_tree.findall("WeatherItem"):
                    if "name" in name.attrib:
                        weather_list.append(name.attrib["name"])
                
                random.shuffle(weather_list)

                pl = 0
                for name in weather_tree.findall("WeatherItem"):
                    if "name" in name.attrib:
                        name.set("name", weather_list[pl])
                        pl += 1
                
                if write(weather_tree, weather_file, weather_path, workpath):
                    show_success("Other : Weather", mainwindow)
                else:
                    show_failure("Other : Weather", mainwindow)
            else:
                show_failure("Other : Weather", mainwindow)
        else:
            logger.info("SKIPPED: Other : Weather")
        
        # Other: Landscape (by ThePlain: https://github.com/ThePlain)
        if settings["Settings"]["Checkboxes"]["Other"]["Landscape"] == True:
            paths_list = get_yaml(yaml_file, "Other", "Landscape", "Paths")
            mixland_name = get_yaml(yaml_file, "Other", "Landscape", "File")
            backup_path = get_yaml(yaml_file, "Other", "Landscape", "BackupPath")
            multiple_mix = get_yaml(yaml_file, "Other", "Landscape", "PreventMultiple")
            abortLandscape = False
            displaceCount = 0

            for path in paths_list:
                if current_dir(path, workpath):
                    logger.debug(f"Trying to create landscape.txt in {path}...")
                    if "landscape.txt" in main.os.listdir():
                        if multiple_mix == False:
                            logger.debug(f"Multiple landscape randomizing is allowed.")
                        else:
                            mainwindow.addMessage(f"Other : Landscape:\n{loc_string('Randomizer', 'LandscapeProhibition')} {path}")
                            logger.warning(f"Landscape randomizing in {path} is restricted in YAML.")
                            abortLandscape = True
                    else:
                        with open("landscape.txt", "w") as log:
                            log.write(path)
                            logger.debug(f"Created landscape.txt in {path}")
                    
                    if abortLandscape == False:
                        try:
                            copy(mixland_name, backup_path, workpath, f"displace_{path[10:14]}.bin")
                            raw = None
                            logger.debug(f"Opening {mixland_name} in {path}...")

                            with open(mixland_name, "rb") as stream:
                                raw = stream.read()

                            count = int(len(raw) / 4)
                            fmt = "<" + "f" * count
                            data = list(struct.unpack(fmt, raw))
                            data = map(lambda v: v + ((random.random() - 0.5) * 3), data)

                            with open(mixland_name, "wb") as stream:
                                stream.write(struct.pack(fmt, *data))
                                displaceCount += 1
                                show_success(f"Other : Landscape ({path[10:14]})", mainwindow)
                            
                        except FileNotFoundError:
                            logger.error(f"Other : Landscape: FileNotFoundError: {mixland_name}: {path}")
                        except:
                            logger.error(f"Other : Landscape: ERROR: Path: {path}")
                            logger.debug(f"Restoring {mixland_name} from backup...")
                            if current_dir(backup_path, workpath):
                                copy(f"displace_{path[11:15]}.bin", path, workpath, mixland_name)
                                remove(f"displace_{path[11:15]}.bin", backup_path, workpath)
                                logger.debug(f"{mixland_name} successfully restored")
            
            if current_dir(backup_path, workpath):
                for path in paths_list:
                    backup_name = f"displace_{path[10:14]}.bin"
                    if backup_name in main.os.listdir():
                        remove(backup_name, backup_path, workpath)
            
            if displaceCount == 11 and gameversion == "Steam":
                show_success("Other : Landscape", mainwindow)
            elif displaceCount == 14 and gameversion == "ImprovedStoryline":
                show_success("Other : Landscape", mainwindow)
        else:
            logger.info("SKIPPED: Other : Landscape")
        
        # LuaRandom
        lua_dest_path = get_yaml(yaml_file, "LuaRandom", "DestPath")
        lua_names = get_yaml(yaml_file, "LuaRandom", "Files")
        triggers_path = get_yaml(yaml_file, "LuaRandom", "TriggersDestPath")

        if current_dir(lua_dest_path, workpath):

            # Models: Dwellers
            if settings["Settings"]["Checkboxes"]["Models"]["Dwellers"]:

                server_var_dwellers = get_yaml(yaml_file, "LuaRandom", "Variables", "Dwellers", "server.lua")

                if turn_on_lua(lua_names[0], server_var_dwellers, workpath, yaml_file):

                    show_success("Models : Dwellers", mainwindow)
                else:
                    show_failure("Models : Dwellers", mainwindow)
            else:
                logger.info("SKIPPED: Models : Dwellers")

            # Other: Prototypes
            if settings["Settings"]["Checkboxes"]["Other"]["Prototypes"]:
                server_var_prots = get_yaml(yaml_file, "LuaRandom", "Variables", "Prototypes", "server.lua")
                debug_var_prots = get_yaml(yaml_file, "LuaRandom", "Variables", "Prototypes", "debug.lua")

                if turn_on_lua(lua_names[0], server_var_prots, workpath, yaml_file):
                    if turn_on_lua(lua_names[1], debug_var_prots, workpath, yaml_file):
                            show_success("Other : Prototypes", mainwindow)
                    else:
                        show_failure("Other : Prototypes", mainwindow)
            else:
                logger.info("SKIPPED: Other : Prototypes")
            
            # Other: PlayerVehicle
            if settings["Settings"]["Checkboxes"]["Other"]["PlayerVehicle"]:
                triggers_var_prots = get_yaml(yaml_file, "LuaRandom", "Variables", "PlayerVehicle", "triggers.xml")

                if turn_on_lua(lua_names[3], triggers_var_prots, workpath, yaml_file):
                    show_success("Other : PlayerVehicle", mainwindow)
                else:
                    show_failure("Other : PlayerVehicle", mainwindow)
            
            else:
                logger.info("SKIPPED: Other : PlayerVehicle")
            
            # Other: VehicleGuns
            if settings["Settings"]["Checkboxes"]["Other"]["VehicleGuns"]:
                server_var_protguns = get_yaml(yaml_file, "LuaRandom", "Variables", "VehicleGuns", "server.lua")
                debug_var_protguns = get_yaml(yaml_file, "LuaRandom", "Variables", "VehicleGuns", "debug.lua")
                triggers_var_protguns = get_yaml(yaml_file, "LuaRandom", "Variables", "VehicleGuns", "triggers.xml")

                if turn_on_lua(lua_names[0], server_var_protguns, workpath, yaml_file):
                    if turn_on_lua(lua_names[1], debug_var_protguns, workpath, yaml_file):
                        if turn_on_lua(lua_names[3], triggers_var_protguns, workpath, yaml_file):
                            show_success("Other : VehicleGuns", mainwindow)
                        else:
                            show_failure("Other : VehicleGuns", mainwindow)
            else:
                logger.info("SKIPPED: Other : VehicleGuns")
            
            copy(lua_names[3], triggers_path, workpath)
        
        # Exe (by Seel: https://github.com/Zvetkov)
        if any([settings["Settings"]["Checkboxes"]["Exe"]["ArmorColor"], settings["Settings"]["Checkboxes"]["Exe"]["FOV"],
                settings["Settings"]["Checkboxes"]["Exe"]["Gravity"], settings["Settings"]["Checkboxes"]["Exe"]["ModelsRender"]]):
            if exe_version != "Unsupported":
                hta_name = yaml_file["Exe"]

                if current_dir("", workpath):
                    files = main.os.listdir()
                    if hta_name in files:
                        if f"{hta_name[0:len(hta_name)-4]}_backup.exe" in files:
                            logger.debug(f"Backup for {hta_name} already exists")
                        else:
                            logger.debug(f"Creating backup for {hta_name}...")
                            copy(hta_name, "", workpath, f"{hta_name[0:len(hta_name)-4]}_backup.exe")
                        
                        res = [16, 32, 64, 128, 256]
                        RAND_512 = res[random.randint(1,4)]
                        RAND_ASPECT = random.uniform(0.2, 0.95)
                        RAND_300 = float(random.randint(40, 300))
                        RAND_GRAV = float(random.randint(-20, -2))

                        ASPECT_RATIO = 16 / 9
                        TARGET_FOV_X_DEG = 90.0
                        TARGET_FOV_X_RADS = math.radians(TARGET_FOV_X_DEG)
                        TARGET_FOV_Y_RADS = 2 * math.atan(math.tan(TARGET_FOV_X_RADS / 2) * (1 / ASPECT_RATIO))
                        COEFF_FOV_X_FROM_Y = TARGET_FOV_X_RADS / TARGET_FOV_Y_RADS

                        offsets_exe = {
                            # low_fuel_threshold
                            0x124CCD: "0x009E5980",
                            }

                        models_render = {
                            0x30808B: RAND_512, # model rendering
                            0x308092: RAND_512, # same as previous
                            }

                        gravity = {
                            0x124CF1: RAND_300,
                            0x202D25: RAND_GRAV,
                            }

                        fov = {
                            # aspect
                            0x5E5A74: RAND_ASPECT, # 009E5A74
                            0x1D7CB: "0x009E5A74", # 009E5A74
                            # aspect ratio hack for Frustum Culling
                            0x3A6128: TARGET_FOV_X_RADS, # fov_x passed to CClipper::CreateScreenFrustums
                            0x5E497C: COEFF_FOV_X_FROM_Y, # hacked "aspect_ratio" coeff to calc fov_y
                            }

                        sexy_armor_color = {
                            0x11CD4F: generate_color(),
                            0x11CD62: generate_color(),
                            0x11CD75: generate_color(),
                            0x11CD88: generate_color(),
                            0x11CD9B: generate_color(),
                            0x11CDAE: generate_color(),
                            0x11CDC1: generate_color(),
                            0x11CDD4: generate_color(),
                            0x11CDE7: generate_color(),
                            0x11CE0D: generate_color(),
                            }

                        if settings["Settings"]["Checkboxes"]["Exe"]["ModelsRender"] == True:
                            offsets_exe.update(models_render)
                            logger.info(f"Exe: Res models: {RAND_512}")
                            mainwindow.addMessage(f"Exe: Res models: {RAND_512}")
                        if settings["Settings"]["Checkboxes"]["Exe"]["Gravity"] == True:
                            offsets_exe.update(gravity)
                            logger.info(f"Exe: Gravity: {RAND_GRAV}")
                            mainwindow.addMessage(f"Exe: Gravity: {RAND_GRAV}")
                        if settings["Settings"]["Checkboxes"]["Exe"]["FOV"]:
                            if gameversion == "Steam" or gameversion == "ImprovedStoryline":
                                offsets_exe.update(fov)
                                logger.info(f"Exe: FOV: {RAND_ASPECT}")
                                mainwindow.addMessage(f"Exe: FOV: {RAND_ASPECT}")
                            else:
                                mainwindow.showPopUp(loc_string("Randomizer", "FOVInavaliable"), "warning")
                        if settings["Settings"]["Checkboxes"]["Exe"]["ArmorColor"]:
                            offsets_exe.update(sexy_armor_color)

                        try:
                            with open(hta_name, "rb+") as f:
                                for offset in offsets_exe.keys():
                                    f.seek(offset)
                                    if type(offsets_exe[offset]) == int:
                                        f.write(struct.pack("i", offsets_exe[offset]))
                                    elif type(offsets_exe[offset]) == str: # hex address
                                        f.write(struct.pack("<L", int(offsets_exe[offset], base=16)))
                                    elif type(offsets_exe[offset]) == float:
                                        f.write(struct.pack("f", offsets_exe[offset]))
                                
                                show_success("Exe", mainwindow)
                        except PermissionError:
                            logger.error(f"Exe: Permission Error: {hta_name}")
                            show_failure("Exe", mainwindow)
                        except:
                            logger.error(f"Exe: ERROR: {hta_name}")
                            show_failure("Exe", mainwindow)
                    else:
                        logger.error(f"Exe: {hta_name} not found in {workpath}")
            else:
                mainwindow.addMessage(f"Exe:\n{loc_string('Randomizer', 'InvalidVersionNoRandom')}")
                logger.warning("Executable randomization is impossible due to an incorrect version of the game.")
        else:
            logger.info("SKIPPED: Exe")
            
            
        if current_dir("", workpath):
            try:
                logger.debug("Removing mixing folder...")
                shutil.rmtree(mix_folder_path)
                logger.debug("Mixing folder successfully removed")
            except:
                logger.error(f"Unable to remove {mix_folder_fullpath}")

        # Determining errors during randomization
        prev_errors = int(mainwindow.errors.text())
        new_errors = 0
        with open(main.os.path.join(windowpath, "randomizer.log"), "r") as log:
            for line in log:
                if line[0:7] == "[ERROR]":
                    new_errors += 1

        if prev_errors < new_errors:
            if prev_errors == 0:
                errors_count = new_errors
            else:
                errors_count = new_errors - prev_errors
            
            str_errors_count = str(errors_count)
        
            ending = str_errors_count[len(str_errors_count)-1]
            if language == "rus":
                if ending == "1" and str_errors_count[len(str_errors_count)-2:len(str_errors_count)] != "11":
                    mistakes = "ошибка"
                elif ending == "2" or ending == "3" or ending == "4":
                    mistakes = "ошибки"
                else:
                    mistakes = "ошибок"

                mainwindow.showPopUp(f"{loc_string('Randomizer', 'TotalMistakes1')} {errors_count} {mistakes}.\n\n{loc_string('Randomizer', 'SeeLog')}", "warning")
            elif language == "eng":
                mainwindow.showPopUp(f"{errors_count} {loc_string('Randomizer', 'TotalMistakes1')}\n\n{loc_string('Randomizer', 'SeeLog')}", "warning")
        
            mainwindow.errors.setText(str(new_errors))
            mainwindow.addMessage(loc_string("Randomizer", "RandomCompletion"))
            mainwindow.addMessage(f"{loc_string('Randomizer', 'TotalMistakes1')} {errors_count} {mistakes}.")
            logger.warning(f"{str_errors_count} errors occured while randomization.")
        else:
            mainwindow.addMessage(loc_string("Randomizer", "RandomSuccessCompletion"))
            logger.info("Randomization successfully completed.")