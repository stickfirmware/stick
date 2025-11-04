"""
Language GUI for settings
"""

import machine

import modules.cache as cache
import modules.menus as menus
import modules.nvs as nvs
import modules.popup as popup
import modules.translate as translate
from modules.translate import get as l_get


def run():
    """Language settings GUI"""
    n_settings = cache.get_nvs("settings")
    
    while True:
        # Get old language
        lang_old = nvs.get_string(n_settings, "lang")
        
        # Make menu out of available languages
        translations = []
        for i in translate.main_file["langs"]:
            translations.append((translate.main_file[i]["name"], i))
        translations.append((l_get("menus.menu_close"), None))
        
        # Ask user for translation selection
        ts_menu = menus.menu(l_get("apps.settings.lang_menu.title"), translations)
        
        # Change version
        if ts_menu is not None:
            if translate.load(ts_menu):
                import version
                if l_get("lang_info.version")[0] < version.get_version("lang_ver")[0] or l_get("lang_info.version")[1] < version.get_version("lang_ver")[1]:
                    popup.show("The language pack is older than system pack version and can not work properly. Expect errors or untranslated menus.", "Info", 60)
                nvs.set_string(n_settings, "lang", ts_menu)
                reboot_confirm = menus.menu(l_get("apps.settings.lang_menu.reboot"),
                                            [(l_get("menus.yes"), 1),
                                                (l_get("menus.no"), None)])
                if reboot_confirm == 1: 
                    machine.soft_reset()
            else:
                popup.show("Translation loading error.", "Error", 10)
                translate.load(lang_old)
        
        else:
            break