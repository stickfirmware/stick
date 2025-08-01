import esp32

import modules.nvs as nvs
from modules.decache import decache

print("Init IO manager")
import modules.io_manager as io_man
if io_man.get_tft() != None:
    tft = io_man.get_tft()
else:
    import modules.tft_init as tft_init
    tft = tft_init.init_tft()
import modules.button_init as btn_init
buttons = btn_init.init_buttons()
button_a = buttons[0]
button_b = buttons[1]
button_c = buttons[2]
io_man.set_btn_a(button_a)
io_man.set_btn_b(button_b)
io_man.set_btn_c(button_c)
io_man.set_tft(tft)

import machine
import modules.menus as menus
import os

def reset_nvs():
    import scripts.reset_nvs

def remove_upd():
    try:
        os.remove("/update.py")
    except:
        print("Update.py deletion error")
def clear_temp():
    try:
        os.rmdir("/temp")
    except:
        print("/temp deletion error")
        
while True:
    render = menus.menu("Recovery menu", [("Reset NVS configuration", 1), ("Delete update.py", 2), ("Clear /temp/", 3), ("File explorer", 5), ("Toggle dev apps", 6), ("Reboot", 13)])
    if render == 1:
        render1 = menus.menu("Destroy nvs?", [("No", 1), ("Yes", 2)])
        if render1 == 2:
            reset_nvs()
    elif render == 2:
        remove_upd()
    elif render == 3:
        clear_temp()
    elif render == 5:
        import modules.file_explorer as a_fe
        a_fe.run()
        decache('modules.file_explorer')
        del a_fe
    elif render == 6:
        n_settings = esp32.NVS("settings")
        dev_settings = nvs.get_int(n_settings, "dev_apps")
        if dev_settings == 1:
            nvs.set_int(n_settings, "dev_apps", 0)
        else:
            nvs.set_int(n_settings, "dev_apps", 1)
    elif render == 13:
        machine.reset()