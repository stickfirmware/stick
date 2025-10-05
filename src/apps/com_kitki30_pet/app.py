import os
import time

import apps.com_kitki30_pet.pet_scanner as pscan
import fonts.def_8x8 as f8x8
import modules.button_combos as btnc
import modules.files as files
import modules.io_manager as io_man
import modules.json as json
import modules.menus as menus
import modules.os_constants as osc
import modules.saving_prompt as save_prompt
import modules.popup as popup
import modules.xp_leveling as xp_levels
from modules.translate import get as l_get

_PET_PATH = "/apps/com_kitki30_pet/pets"
_CONFIG_PATH = "/usr/config/"

def pet_list_gui():
    pets = pscan.get_list(_PET_PATH)
    if len(pets) == 0:
        popup.show(l_get("apps.pet.no_pets", "crashes.error"))
        return None
    return pets

def make_config():
    if "pet_config.json" in os.listdir(_CONFIG_PATH):
        return json.read(files.path_join(_CONFIG_PATH, "pet_config.json"))
    else:
        pets = pet_list_gui()
        if pets is None: 
            return
        save_prompt.show_saving_prompt()
        json.write(files.path_join(_CONFIG_PATH, "pet_config.json"), {"pet_name": pets[0][0], "pet_path": pets[0][2]})
        return json.read(files.path_join(_CONFIG_PATH, "pet_config.json"))
    
def replace_pet_lines(line):
    xp = xp_levels.xp_progress(xp_levels.get_xp())
    
    mood = "Unknown"
    mood_points = xp_levels.get_mood()
    
    if mood_points >= 80:
        mood = l_get("apps.pet.mood.happy")
    elif mood_points >= 50:
        mood = l_get("apps.pet.mood.neutral")
    else:
        mood = l_get("apps.pet.mood.sad")
    
    return line.replace("%mood%", mood).replace("%level%", str(xp[0])).replace("%curr%", str(xp[1])).replace("%need%", str(xp[2])) 

def run():
    tft = io_man.get('tft')

    tft.fill(0)
    
    # Scan for pets
    tft.text(f8x8, l_get("apps.pet.scan_pets"), 0, 0, 65535)
    
    pets = pet_list_gui()
    if pets is None:
        return

    # Make or load config
    tft.text(f8x8, l_get("apps.pet.load_conf"), 0, 8, 65535)
    
    config = make_config()
    
    # Give mood to pet
    xp_levels.add_mood(3)

    # Display pet
    data = None
    with open(files.path_join(config["pet_path"],"pet_en.txt"), "r") as f:
        data = f.read().splitlines()
        
    tft.fill(0)
    y = 0
    
    for line in data:
        tft.text(f8x8, replace_pet_lines(line), 0, y, 65535)
        y += 8
        
    while not btnc.any_btn(["a", "b", "c"]):
        time.sleep(osc.LOOP_WAIT_TIME)
        
    menu = menus.menu(l_get("apps.pet.pet_menu"), [(l_get("menus.menu_exit"), None), (l_get("apps.pet.change_pet"), 1)])
    
    # Change pet
    if menu == 1:
        change_menu = []
        
        change_menu.append((f"{l_get("apps.pet.current")} {config["pet_name"]}", None))
        
        for pet in pets:
            change_menu.append((pet[0], pet))
            
        pet_select = menus.menu(l_get("apps.pet.change_pet"), change_menu)
        
        if pet_select is None:
            return
        
        save_prompt.show_saving_prompt()
        json.write(files.path_join(_CONFIG_PATH, "pet_config.json"), {"pet_name": pet_select[0], "pet_path": pet_select[2]})
        return run()