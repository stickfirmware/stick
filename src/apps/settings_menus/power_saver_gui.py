"""
Power saving settings GUI
"""

import time

import modules.cache as cache
import modules.menus as menus
import modules.nvs as nvs
from modules.translate import get as l_get


def run():
    """Power saver settings GUI"""
    n_settings = cache.get_nvs("settings")
    
    work1 = True
    while work1:
        menu3 = menus.menu(l_get("apps.settings.power.pwr_saving_title"),
                            [(l_get("apps.settings.current") + ": " + str(nvs.get_int(n_settings, "allowsaving")), 1),
                            (l_get("menus.enable"), 2),
                            (l_get("menus.disable"), 3), 
                            (l_get("menus.menu_close"), 13)])
        if menu3 == 1:
            time.sleep(0.02)
        elif menu3 == 2:
            nvs.set_int(n_settings, "allowsaving", 1)
        elif menu3 == 3:
            nvs.set_int(n_settings, "allowsaving", 0)
        else:
            work1 = False 