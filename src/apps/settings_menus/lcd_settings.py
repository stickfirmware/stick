"""
LCD settings GUI
"""

import time

import modules.cache as cache
import modules.os_constants as osc
import modules.io_manager as io_man
import modules.menus as menus
import modules.nvs as nvs
import modules.popup as popup
from modules.translate import get as l_get

def run():
    """LCD settings GUI"""
    menu2 = menus.menu(l_get("apps.settings.lcd_menu.title"),
            [(l_get("apps.settings.lcd_menu.backlight"), 1),
            (l_get("apps.settings.lcd_menu.autorotate"), 2),
            (l_get("menus.menu_close"), 13)])
    
    # Get TFT & NVS namespace
    tft = io_man.get('tft')
    n_settings = cache.get_nvs('settings')
    
    # Backlight settings
    if menu2 == 1:
        work1 = True
        while work1:
            menu3 = menus.menu(l_get("apps.settings.lcd_menu.backlight_title"),
                                [(l_get("apps.settings.current") + ": " + str(round(nvs.get_float(n_settings, "backlight"), 1)), 1),
                                ("+", 2),
                                ("-", 3),
                                (l_get("menus.menu_close"), 13)])
            if menu3 == 1:
                time.sleep(0.02)
            elif menu3 == 2:
                if round(nvs.get_float(n_settings, "backlight"), 1) != 1.0:
                    nvs.set_float(n_settings, "backlight", (nvs.get_float(n_settings, "backlight") + 0.1))
            elif menu3 == 3:
                if round(nvs.get_float(n_settings, "backlight"), 1) > osc.LCD_MIN_BL:
                    nvs.set_float(n_settings, "backlight", (nvs.get_float(n_settings, "backlight") - 0.1))
            else:
                work1 = False
            tft.set_backlight(nvs.get_float(n_settings, "backlight"))
        
    # Autorotate settings       
    elif menu2 == 2:
        work1 = True
        if not osc.HAS_IMU:
            work1 = False
            popup.show(l_get("apps.settings.lcd_menu.imu_error_popup"), l_get("crashes.error"), 10)
        while work1:
            menu3 = menus.menu(l_get("apps.settings.lcd_menu.autorotate_title"),
                                [(l_get("apps.settings.current") + ": " + str(nvs.get_int(n_settings, "autorotate")), 1),
                                (l_get("menus.enable"), 2),
                                (l_get("menus.disable"), 3), 
                                (l_get("menus.menu_close"), 13)])
            if menu3 == 1:
                time.sleep(0.02)
            elif menu3 == 2:
                nvs.set_int(n_settings, "autorotate", 1)
            elif menu3 == 3:
                nvs.set_int(n_settings, "autorotate", 0)
            else:
                work1 = False