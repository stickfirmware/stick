"""
Neopixel GUI for settings
"""

import modules.cache as cache
import modules.menus as menus
import modules.nvs as nvs
import modules.os_constants as osc
import modules.popup as popup
from modules.translate import get as l_get


def run():
    """Neopixel settings GUI"""
    n_settings = cache.get_nvs("settings")
    
    import modules.neopixel_anims as np_anims
    
    while True:
        np_menu =  menus.menu(l_get("apps.settings.neopixel.title"),
                                [(l_get("apps.settings.neopixel.enable"), 0), 
                                (l_get("apps.settings.neopixel.anim_style"), 1),
                                (l_get("apps.settings.neopixel.notice_menu"), 2),
                                (l_get("menus.menu_close"), None)])
        if np_menu == 0:
            enable = menus.menu(l_get("apps.settings.neopixel.enable_ask"),
                                [(l_get("menus.yes"), 1),
                                    (l_get("menus.no"), 0)])
            if enable is not None:
                nvs.set_int(n_settings, 'neo_enabled', enable)
            np_anims.refresh_counters() # Refresh cache
                
        elif np_menu == 1:
            anim_style_selector = menus.menu(l_get("apps.settings.neopixel.anim_style"), 
                                                [(l_get("apps.settings.neopixel.static"), 1),
                                                (l_get("apps.settings.neopixel.rainbow"), 2),
                                                (l_get("menus.menu_close"), None)])
            if anim_style_selector == 1:
                nvs.set_int(n_settings, "neo_anim_style", 1)
                color_change_ask = menus.menu(l_get("apps.settings.neopixel.also_change_colors"),
                                                [(l_get("menus.yes"), 1),
                                                (l_get("menus.no"), None)])
                if color_change_ask == 1:
                    import modules.numpad as keypad
                    r = keypad.numpad("R color, 0-255", 3)
                    g = keypad.numpad("G color, 0-255", 3)
                    b = keypad.numpad("B color, 0-255", 3)
                    if r > 255:
                        r = 255
                    if g > 255:
                        g = 255
                    if b > 255:
                        b = 255
                    nvs.set_int(n_settings, "neo_R", r)
                    nvs.set_int(n_settings, "neo_G", g)
                    nvs.set_int(n_settings, "neo_B", b)
                
            elif anim_style_selector == 2:
                nvs.set_int(n_settings, "neo_anim_style", 2)
            np_anims.refresh_counters() # Refresh cache
        
        elif np_menu == 2:
            popup.show(
                l_get("apps.settings.neopixel.notice").replace("%backlight", str(osc.NEOPIXEL_BACKLIGHT_THRESHOLD)).replace("%ledtype", str(osc.NEOPIXEL_TYPE)),
                l_get("apps.settings.neopixel.notice_menu"))
        
        else:
            break