# Score keeper app
# App ID: 1001

import modules.io_manager as io_man
import modules.printer as printer
import modules.menus as menus
import modules.nvs as nvs
import esp32
import machine
import modules.os_constants as osc

button_a = io_man.get_btn_a()
button_b = io_man.get_btn_b()
button_c = io_man.get_btn_c()
tft = io_man.get_tft()

def run():
    global button_c, button_a, button_b, tft
    button_a = io_man.get_btn_a()
    button_b = io_man.get_btn_b()
    button_c = io_man.get_btn_c()
    tft = io_man.get_tft()
    
    machine.freq(osc.ULTRA_FREQ)
    
    app_storage = esp32.NVS("apps_1001")
    
    printer.log("Going into main loop")
    
    team_1 = 0
    team_2 = 0
    
    t1_nvs = nvs.get_int(app_storage, "team1")
    t2_nvs = nvs.get_int(app_storage, "team2")
    if t1_nvs != None:
        team_1 = t1_nvs
    else:
        nvs.set_int(app_storage, "team1", 0)
    if t2_nvs != None:
        team_2 = t2_nvs
    else:
        nvs.set_int(app_storage, "team2", 0)
    
    work = True
    while work == True:
        render = menus.menu("Scorekeeper", [("Team 1: " + str(team_1), 1), ("Team 2: " + str(team_2), 2), ("Reset", 3), ("Close", 4)])
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
        
