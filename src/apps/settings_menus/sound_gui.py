"""
Sound settings
"""

import time

import modules.cache as cache
import modules.menus as menus
import modules.nvs as nvs
from modules.translate import get as l_get


def run():
    # Get NVS namespace
    n_settings = cache.get_nvs("settings")
    
    while True:
        menu2 = menus.menu(l_get("apps.settings.buzzer_menu.buzzer_title"),
                            [(l_get("apps.settings.buzzer_menu.volume"), 1), 
                            (l_get("menus.menu_close"), 13)])
        
        # Volume settings
        if menu2 == 1:
            while True:
                menu3 = menus.menu(l_get("apps.settings.buzzer_menu.volume_title"),
                                    [(l_get("apps.settings.current") + ": " + str(round(nvs.get_float(n_settings, "volume"), 1)), 1),
                                    ("+", 2),
                                    ("-", 3),
                                    (l_get("menus.menu_close"), 13)])
                if menu3 == 1:
                    time.sleep(0.02)
                elif menu3 == 2:
                    if round(nvs.get_float(n_settings, "volume"), 1) != 0.8:
                        nvs.set_float(n_settings, "volume", (nvs.get_float(n_settings, "volume") + 0.1))
                elif menu3 == 3:
                    if round(nvs.get_float(n_settings, "volume"), 1) != 0.1:
                        nvs.set_float(n_settings, "volume", (nvs.get_float(n_settings, "volume") - 0.1))
                else:
                    break
        
        else:
            break