"""
Shutdown mode settings GUI
"""

import time

import fonts.def_8x8 as f8x8
import modules.cache as cache
import modules.io_manager as io_man
import modules.menus as menus
import modules.nvs as nvs
import modules.popup as popup
from modules.translate import get as l_get


def run():
    """Shutdown mode settings GUI"""
    tft = io_man.get("tft")
    n_settings = cache.get_nvs("settings")
    
    work1 = True
    while work1:
        menu3 = menus.menu(l_get("apps.settings.power.shutdown_mode_title"),[
            (l_get("apps.settings.power.shutdown_modes.deep_sleep"), 1),
            (l_get("apps.settings.power.shutdown_modes.legacy"), 2),
            (l_get("apps.settings.power.get_current"), 3),
            (l_get("apps.settings.power.shutdown_what_is_this"), 4),
            (l_get("menus.menu_close"), 13)
        ])
        
        # Change values
        if menu3 == 1:
            nvs.set_int(n_settings, "shutdown_mode", 2) # Deep sleep
        elif menu3 == 2:
            nvs.set_int(n_settings, "shutdown_mode", 1) # Legacy
            
        # Show current
        elif menu3 == 3:
            name = "N/A"
            curr_val = nvs.get_int(n_settings, "shutdown_mode")
            if curr_val == 1:
                name = l_get("apps.settings.power.shutdown_modes.legacy")
            elif curr_val == 2:
                name = l_get("apps.settings.power.shutdown_modes.deep_sleep")
            tft.text(f8x8, name, 0, 0, 65535)
            time.sleep(3)
            
        # What is this popup
        elif menu3 == 4:
            popup.show(l_get("apps.settings.power.shutdown_what_this_popup"), l_get("popups.info"))
        else:
            work1 = False 