# Score keeper app
# App ID: 1001

import esp32

import modules.io_manager as io_man
import modules.printer as printer
import modules.menus as menus
import modules.nvs as nvs
from modules.translate import get as l_get

button_a = io_man.get('button_a')
button_b = io_man.get('button_b')
button_c = io_man.get('button_c')
tft = None

def run():
    global button_c, button_a, button_b, tft
    button_a = io_man.get('button_a')
    button_b = io_man.get('button_b')
    button_c = io_man.get('button_c')
    tft = io_man.get('tft')
    
    app_storage = esp32.NVS("apps_1001")
    
    printer.log("Going into main loop")
    
    team_1 = 0
    team_2 = 0
    
    t1_nvs = nvs.get_int(app_storage, "team1")
    t2_nvs = nvs.get_int(app_storage, "team2")
    if t1_nvs is not None:
        team_1 = t1_nvs
    else:
        nvs.set_int(app_storage, "team1", 0)
    if t2_nvs is not None:
        team_2 = t2_nvs
    else:
        nvs.set_int(app_storage, "team2", 0)
    
    work = True
    while work:
        render = menus.menu(l_get("apps.scorekeeper.name"), 
                            [(l_get("apps.scorekeeper.team") + " 1: " + str(team_1), 1),
                             (l_get("apps.scorekeeper.team") + " 2: " + str(team_2), 2),
                             (l_get("menus.menu_reset"), 3),
                             (l_get("menus.menu_close"), 4)])
        if render == 1:
            team_1 += 1
        elif render == 2:
            team_2 += 1
        elif render == 3:
            team_1 = 0
            team_2 = 0
        else:
            work = False
    
    nvs.set_int(app_storage, "team1", team_1)
    nvs.set_int(app_storage, "team2", team_2)
        
