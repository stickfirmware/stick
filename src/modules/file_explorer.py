import sys
import time
import os
import gc

import fonts.def_8x8 as f8x8
import fonts.def_16x32 as f16x32

import modules.menus as menus
import modules.open_file as open_file   
import modules.io_manager as io_man

button_a = io_man.get_btn_a()
button_b = io_man.get_btn_b()
button_c = io_man.get_btn_c()
tft = io_man.get_tft()
    
clipboard = ""
        
sd_present = False

freespace_flash = 0
freespace_sd = 0

# Refresh io
def load_io():
    global button_c, button_a, button_b, tft
    button_a = io_man.get_btn_a()
    button_b = io_man.get_btn_b()
    button_c = io_man.get_btn_c()
    tft = io_man.get_tft()

def is_file(path):
    if os.stat(path)[0] & 0x4000:
        return False
    else:
        return True

def path_join(*args):
    parts = [s.strip("/") for s in args if s != "/"]
    return "/" + "/".join(parts) if parts else "/"


def parent_path(path):
    if path == "/" or path == "":
        return "/"
    if path.endswith("/") and path != "/":
        path = path[:-1]
    last_slash = path.rfind("/")
    if last_slash == 0:
        return "/"
    elif last_slash > 0:
        return path[:last_slash]
    else:
        return "/"

def browser(path):
    load_io()
    try:
        files = os.listdir(path)
    except OSError:
        return
    
    files_menu = []
    index = 1
    files_menu.append(("../", 0))
    for i in files:
        if is_file(path_join(path, i)) == True:
            files_menu.append(("      " + str(i), index))
        else:
            files_menu.append(("<DIR> " + str(i), index))
        index += 1
    chunks = [path[i:i+28] for i in range(0, len(path), 28)]
    last_chunk = chunks[-1] if chunks else ""
    render = menus.menu(last_chunk, files_menu)
    
    if render == None:
        return
    elif render == 0:
        return
    else:
        return path_join(path, files[render - 1])
    
def fileMenu(file):
    global clipboard
    render = menus.menu(str(file), [("Open in...", 4), ("Delete", 2), ("Properties", 1), ("Exit", 13)])
    if render == 4:
        open_file.openMenu(file)
    elif render == 1:
        if "temp" not in os.listdir("/"):
            os.mkdir("/temp")
        stat = os.stat(file)
        tm = time.localtime(stat[8])
        with open("/temp/fileprop.txt", "w") as f:
            f.write(str(file) + "\n")
            f.write("File size: {} B\n".format(stat[6]))
            f.write("Last modified: {} {}, {} at {:02}:{:02}:{:02}\n".format(
                ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][tm[1]-1],
                tm[2], tm[0], tm[3], tm[4], tm[5]
            ))

        comd = __import__("helpers.run_in_reader")
        parts = "helpers.run_in_reader".split(".")
        for part in parts[1:]:
            comd = getattr(comd, part)
        comd.open_file("/temp/fileprop.txt")
        if "helpers/run_in_reader" in sys.modules:
            del sys.modules["helpers/run_in_reader"]
    elif render == 2:
        if menus.menu("Delete?", [("Yes", 1), ("No", None)]) == 1:
            try:
                os.remove(file)
            except Exception as e:
                print(e)
                menus.menu("Error deleting file!", [("Close", 1)])
            return
        
def detect():
    global sd_present
    global freespace_flash
    global freespace_sd
    os.sync()
    os.chdir("/")
    
    # Check for SD Card
    listdir = os.listdir()
    if "sd" in listdir:
        sd_present = True
        stat = os.statvfs("/sd")
        freespace_sd = stat[0] * stat[3]
    
    # Check free space on flash
    stat = os.statvfs("/")
    freespace_flash = stat[0] * stat[3]

def rmdir_recursive(path):
    for file in os.listdir(path):
        full_path = path_join(path, file)
        if is_file(full_path):
            os.remove(full_path)
        else:
            rmdir_recursive(full_path)
    os.rmdir(path)
    
def explorerLoop(startingpath, disablemenu = False):
    currpath = startingpath
    work = True
    while work == True:
        browse = browser(currpath)
        if browse == None:
            if disablemenu:
                if currpath == "/":
                    work = False
                else:
                    currpath = parent_path(currpath)
            else:
                folder_exit_menu = menus.menu("Menu", [("Go back", None), ("Create folder", 1)])
                if folder_exit_menu == None:
                    if currpath == "/":
                        work = False
                    else:
                        currpath = parent_path(currpath)
                elif folder_exit_menu == 1:
                    import modules.numpad as keyboard
                    folder_create_name = keyboard.keyboard("Enter folder name", 200)
                    from modules.decache import decache
                    decache("modules.numpad")
                    if folder_create_name != "" and folder_create_name != None:
                        try:
                            os.mkdir(path_join(currpath, folder_create_name))
                        except:
                            menus.menu("Couldn't make folder!", [("OK", None)])
                    else:
                        menus.menu("Invalid name!", [("OK", 1)])
        else:
            if is_file(browse):
                if disablemenu == False:
                    fileMenu(browse)
                else:
                    return browse
            else:
                if disablemenu:
                    currpath = browse
                else:
                    folder_enter_menu = menus.menu("Folder menu", [("Change dir", 1), ("Delete", 2)])
                    if folder_enter_menu == 1:
                        currpath = browse
                    elif folder_enter_menu == 2:
                        if menus.menu("Remove folder?", [("Yes", 1), ("No", None)]) == 1:
                            try:
                                rmdir_recursive(path_join(currpath, browse))
                            except:
                                menus.menu("Couldn't remove folder!", [("OK", None)])
    
def run(fileselectmode=False, startingselectpath="/"):
    load_io()
    tft.fill(0)
    tft.text(f16x32, "File Explorer",0,0,1984)
    tft.text(f8x8, "Loading...",0,32,65535)
    work = True
    detect()
    if fileselectmode == True:
        work = False
        return explorerLoop(startingselectpath, True)
    while work == True:
        if sd_present == True:
            render = menus.menu("File explorer", [("Built-in Flash (/)", 1), ("SD Card (/sd)", 2), ("Exit", 13)])
        else:
            render = menus.menu("File explorer", [("Built-in Flash (/)", 1), ("Exit", 13)])
        try:
            if render == 13:
                work = False
            elif render == 2:
                explorerLoop("/sd")
            elif render == 1:
                explorerLoop("/")
            else:
                work = False
        except Exception as e:
            print("Oops!\nSomething wrong has happened in File Explorer\nLogs:\n"+str(e))
            tft.fill(0)
            gc.collect()
            tft.text(f16x32, "Oops!",0,0,2015)
            tft.text(f8x8, "Something wrong has happened!",0,32,65535)
            tft.text(f8x8, "Please try again!",0,40,65535)
            time.sleep(3)
            work = False
