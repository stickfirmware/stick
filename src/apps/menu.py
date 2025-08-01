import modules.io_manager as io_man
from modules.decache import decache
import modules.menus as menus
import modules.os_constants as osc
import esp32
import modules.nvs as nvs
import machine
import gc

n_settings = esp32.NVS("settings")

dev_settings = nvs.get_int(n_settings, "dev_apps")
if dev_settings == None:
    dev_settings = 0

button_a = None
button_b = None
button_c = None
tft = None

def run():
    global button_c, button_a, button_b, tft
    button_a = io_man.get_btn_a()
    button_b = io_man.get_btn_b()
    button_c = io_man.get_btn_c()
    tft = io_man.get_tft()
    
    menu_apps = [("IR Remote", 1), ("Music Player", 6), ("File explorer", 7), ("Flashlight", 8), ("Others", 4), ("Settings", 3)]
    if dev_settings == 1:
        menu_apps.append(("Developer apps", 99))
    menu_apps.append(("Close", 13))

    menu1 = menus.menu("Menu", menu_apps)
    if menu1 == 3:
        import apps.settings as a_se
        a_se.run()
        del a_se
        decache('apps.settings')
    elif menu1 == 4:
        import apps.others as a_ot
        a_ot.run()
        del a_ot
        decache('apps.others')
    elif menu1 == 1:
        import apps.IR as a_ir
        a_ir.run()
        a_ir.exit()
        del a_ir
        decache('apps.IR')
    elif menu1 == 6:
        import apps.player as a_pl
        a_pl.run()
        del a_pl
        decache('apps.player')
    elif menu1 == 7:
        import modules.file_explorer as a_fe
        a_fe.run()
        del a_fe
        decache('modules.file_explorer')
    elif menu1 == 8:
        import apps.flashlight as a_fl
        a_fl.run()
        del a_fl
        decache('apps.flashlight')
    elif menu1 == 99:
        import apps.dev_apps.dev_menu as d_dev
        d_dev.run()
        del d_dev
        decache('apps.dev_apps.dev_menu')
    gc.collect()
    machine.freq(osc.BASE_FREQ)