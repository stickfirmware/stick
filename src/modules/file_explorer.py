import sys
import time
import os

import fonts.def_8x8 as f8x8
import fonts.def_16x32 as f16x32

import modules.menus as menus
import modules.open_file as open_file   
import modules.io_manager as io_man
import modules.popup as popup
from modules.files import is_file, rmdir_recursive, parent_path, path_join
from modules.translate import get as l_get

button_a = io_man.get('button_a')
button_b = io_man.get('button_b')
button_c = io_man.get('button_c')
tft = None

file_banlist = [
    '/main.py',
    '/mainos.py',
    '/version.py',
    '/modules',
    '/apps',
    '/helpers',
    '/fonts',
    '/bitmaps',
    '/scripts',
    '/recovery',
    '/guides'
]
    
clipboard = ""
        
sd_present = False

freespace_flash = 0
freespace_sd = 0

# Refresh io
def _LOAD_IO():
    global button_c, button_a, button_b, tft
    button_a = io_man.get('button_a')
    button_b = io_man.get('button_b')
    button_c = io_man.get('button_c')
    tft = io_man.get('tft')

def browser(path):
    _LOAD_IO()
    try:
        files = os.listdir(path)
    except OSError:
        return
    
    files_menu = []
    index = 1
    files_menu.append(("../", 0))
    for i in files:
        if is_file(path_join(path, i)):
            files_menu.append(("  " + str(i), index))
        else:
            files_menu.append(("D " + str(i), index))
        index += 1
    chunks = [path[i:i+28] for i in range(0, len(path), 28)]
    last_chunk = chunks[-1] if chunks else ""
    render = menus.menu(last_chunk, files_menu)
    
    if render is None:
        return
    elif render == 0:
        return
    else:
        return path_join(path, files[render - 1])
    
def fileMenu(file):
    global clipboard
    if file.endswith(".mpy") or file in file_banlist:
        confirmation = menus.menu(l_get("apps.file_explorer.modify_may_harm"), 
                                  [(l_get("apps.file_explorer.dont_open"), None),
                                   (l_get("apps.file_explorer.open_anyway"), 1)])
        if confirmation is None:
            return
    render = menus.menu(str(file), 
                        [(l_get("apps.file_explorer.open_in"), 4),
                         (l_get("apps.file_explorer.delete"), 2),
                         (l_get("apps.file_explorer.properties"), 1),
                         (l_get("menus.menu_exit"), 13)])
    if render == 4:
        open_file.openMenu(file)
    elif render == 1:
        if "temp" not in os.listdir("/"):
            os.mkdir("/temp")
        stat = os.stat(file)
        tm = time.localtime(stat[8])
        with open("/temp/fileprop.txt", "w") as f:
            f.write(str(file) + "\n")
            f.write("{} {} B\n".format(l_get("apps.file_explorer.file_size"), stat[6]))
            f.write("{} {} {}, {} at {:02}:{:02}:{:02}\n".format(l_get("apps.file_explorer.last_modified"),
                l_get("apps.file_explorer.months_of_the_year")[tm[1]-1],
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
        if menus.menu(l_get("apps.file_explorer.delete_confirmation"), 
                      [l_get("menus.yes"), 
                       (l_get("menus.no"), None)]) == 1:
            try:
                os.remove(file)
            except Exception as e:
                print(e)
                menus.menu(l_get("apps.file_explorer.error_deleting"), [(l_get("menus.menu_close"), 1)])
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
    
def explorerLoop(startingpath, disablemenu = False):
    currpath = startingpath
    work = True
    while work:
        browse = browser(currpath)
        if browse is None:
            if disablemenu:
                if currpath == "/":
                    work = False
                else:
                    currpath = parent_path(currpath)
            else:
                folder_exit_menu = menus.menu(l_get("apps.file_explorer.folder_menu"),
                                              [(l_get("menus.menu_go_back"), None),
                                               (l_get("apps.file_explorer.create_folder"), 1)])
                if folder_exit_menu is None:
                    if currpath == "/":
                        work = False
                    else:
                        currpath = parent_path(currpath)
                elif folder_exit_menu == 1:
                    import modules.numpad as keyboard
                    folder_create_name = keyboard.keyboard(l_get("apps.file_explorer.enter_folder_name"), 200)
                    from modules.decache import decache
                    decache("modules.numpad")
                    if folder_create_name != "" and folder_create_name is not None:
                        try:
                            os.mkdir(path_join(currpath, folder_create_name))
                        except OSError:
                            popup.show(l_get("apps.file_explorer.could_not_make_folder"), l_get("crashes.error"), 10)
                    else:
                        popup.show(l_get("apps.file_explorer.invalid_name"), l_get("crashes.error"), 10)
        else:
            if is_file(browse):
                if not disablemenu:
                    fileMenu(browse)
                else:
                    return browse
            else:
                if disablemenu:
                    currpath = browse
                else:
                    if browse in file_banlist:
                        confirmation = menus.menu(l_get("apps.file_explorer.modify_may_harm"), 
                                  [(l_get("apps.file_explorer.dont_open"), None),
                                   (l_get("apps.file_explorer.open_anyway"), 1)])
                        if confirmation != 1:
                            continue
                    folder_enter_menu = menus.menu(l_get("apps.file_explorer.folder_menu"),
                                                   [(l_get("apps.file_explorer.change_dir"), 1), 
                                                    (l_get("apps.file_explorer.delete"), 2)])
                    if folder_enter_menu == 1:
                        currpath = browse
                    elif folder_enter_menu == 2:
                        if menus.menu(l_get("apps.file_explorer.delete_confirmation"), 
                                [l_get("menus.yes"), 
                                (l_get("menus.no"), None)]) == 1:
                            try:
                                rmdir_recursive(path_join(currpath, browse))
                            except OSError:
                                popup.show(l_get("apps.file_explorer.error_deleting"), "Error", 10)
    
def run(fileselectmode=False, startingselectpath="/"):
    _LOAD_IO()
    tft.fill(0)
    tft.text(f16x32, l_get("apps.file_explorer.name_big"),0,0,1984)
    tft.text(f8x8, l_get("apps.file_explorer.loading"),0,32,65535)
    work = True
    detect()
    if fileselectmode:
        work = False
        return explorerLoop(startingselectpath, True)
    while work:
        if sd_present:
            render = menus.menu(l_get("apps.file_explorer.name"), 
                                [(l_get("apps.file_explorer.built-in_flash") + " (/)", 1),
                                 (l_get("apps.file_explorer.sd_card") + " (/sd)", 2),
                                 (l_get("menus.menu_exit"), 13)])
        else:
            render = menus.menu(l_get("apps.file_explorer.name"), 
                                [(l_get("apps.file_explorer.built-in_flash") + " (/)", 1),
                                 (l_get("menus.menu_exit"), 13)])
        if render == 13:
            work = False
        elif render == 2:
            explorerLoop("/sd")
        elif render == 1:
            explorerLoop("/")
        else:
            work = False