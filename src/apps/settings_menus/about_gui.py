"""
About GUI for settings
"""

import gc
import os
import time

import machine

import fonts.def_8x8 as f8x8
import modules.cache as cache
import modules.io_manager as io_man
import modules.menus as menus
import modules.open_file as open_file
import modules.os_constants as osc
from modules.translate import get as l_get


def run():
    """Show about GUI"""
    tft = io_man.get("tft")
    button_a = io_man.get("button_a")
    button_b = io_man.get("button_b")
    button_c = io_man.get("button_c")
    
    while True:
        about_menu = menus.menu(l_get("apps.settings.menu1.about"), [
            (l_get("apps.settings.about.firmware_info"), 1),
            (l_get("apps.settings.about.hardware_info"), 2),
            (l_get("menus.menu_exit"), None)
        ])
        
        if about_menu == 1:
            tft.fill(0)
            gc.collect()
            if cache.get("ver_isbeta"):
                ver_color = 65088
            else:
                ver_color = 65535
            tft.text(f8x8, f"Stick firmware {l_get("apps.settings.about.fw.version")} {cache.get("ver_displayname")}" ,0,0,ver_color)
            tft.text(f8x8, l_get("apps.settings.about.fw.by_kitki30") + " @Kitki30",0,8,ver_color)
            tft.text(f8x8, l_get("apps.settings.about.fw.apache_license"),0,16,65535)
            
            tft.text(f8x8, l_get("apps.settings.about.fw.mpy_ver").replace("%mpy_ver%", str(os.uname().release)), 0, 32, 65535)
            
            tft.text(f8x8, l_get("apps.settings.about.fw.a_exit"),0,111,65535)
            tft.text(f8x8, l_get("apps.settings.about.fw.b_credits"),0,119,65535)
            tft.text(f8x8, l_get("apps.settings.about.fw.c_license"),0,127,65535)
            while button_a.value() == 1 and button_b.value() == 1 and button_c.value() == 1:
                time.sleep(osc.DEBOUNCE_TIME)
            if button_b.value() == 0:
                open_file.open_in("com.kitki30.filereader", "/CREDITS")
            if button_c.value() == 0:
                open_file.open_in("com.kitki30.filereader", "/LICENSE")
                
        elif about_menu == 2:
            tft.fill(0)
            tft.text(f8x8, l_get("apps.settings.about.hw.hwinfo"), 0, 0, 65535)
            serial = machine.unique_id().hex().upper()
            tft.text(f8x8, osc.DEVICE_NAME, 0, 8, 64288)
            tft.text(f8x8, l_get("apps.settings.about.hw.esp_serial"), 0, 16, 65535)
            tft.text(f8x8, serial, 0, 24, 64288)
            tft.text(f8x8, l_get("menus.popup_any_btn"),0,127,65535)
            while button_a.value() == 1 and button_b.value() == 1 and button_c.value() == 1:
                time.sleep(osc.DEBOUNCE_TIME)
                
        elif about_menu is None:
            break