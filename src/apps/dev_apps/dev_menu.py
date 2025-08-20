import gc
import os

import modules.io_manager as io_man
from modules.decache import decache
import modules.menus as menus
import modules.crash_handler as c_handler
import modules.os_constants as osc
import modules.powersaving as ps

button_a = None
button_b = None
button_c = None
tft = None

def run():
    global button_c, button_a, button_b, tft
    button_a = io_man.get('button_a')
    button_b = io_man.get('button_b')
    button_c = io_man.get('button_c')
    tft = io_man.get('tft')
    
    menu_apps = [("Grove I2C scan", 1), ("Hardware info", 2), ("Trigger crash", 3), ("SD Activator (Experimental)", 3), ("Close", None)]

    menu1 = menus.menu("Menu", menu_apps)
    if menu1 == 1:
        import apps.dev_apps.iic_scan as i2c_scan
        i2c_scan.run()
        del i2c_scan
        decache('apps.dev_apps.iic_scan')
    elif menu1 == 2:
        import apps.dev_apps.task_mgr as taskmgr
        taskmgr.run()
        del taskmgr
        decache('apps.dev_apps.task_mgr')
    elif menu1 == 3:
        os.sync()
        c_handler.crash_screen(tft, 1, "User triggered test crash from menu", True, True, 1)
    elif menu1 == 4:
        import apps.dev_apps.sd_activator as sd_act
        sd_act.run()
        del sd_act
        decache('apps.dev_apps.sd_activator')
    gc.collect()
    ps.set_freq(osc.BASE_FREQ)