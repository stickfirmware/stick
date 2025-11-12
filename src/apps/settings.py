import gc

import machine

import modules.cache as cache
import modules.io_manager as io_man
import modules.menus as menus
import modules.nvs as nvs
import modules.os_constants as osc
import modules.popup as popup
import modules.powersaving as ps
from modules.decache import decache
from modules.translate import get as l_get

tft = None

# Refresh io
def _LOAD_IO():
    global tft
    tft = io_man.get('tft')
    
def run_gui(path: str):
    """
    Helper to run all the GUIs
    
    Args:
        path: module path to the gui
    """
    parts = path.split('.')
    mod = __import__(path)
    for part in parts[1:]:
        mod = getattr(mod, part)
    mod.run()
    decache(path)
    del mod

def run():
    _LOAD_IO()
    n_settings = cache.get_nvs('settings')
    n_updates = cache.get_nvs('updates')
    
    work = True
    while work:
        # Main menu
        menu1 = menus.menu(l_get("apps.settings.name"),
                           [(l_get("apps.clock.name"), "apps.settings_menus.clock_gui"),
                            (l_get("apps.settings.menu1.lcd"), "apps.settings_menus.lcd_settings"),
                            (l_get("apps.settings.menu1.power"), "apps.settings_menus.power_menu_gui"),
                            (l_get("apps.settings.menu1.neopixel"), 2),
                            (l_get("apps.settings.menu1.sound"), "apps.settings_menus.sound_gui"),
                            (l_get("apps.settings.menu1.wifi"), "apps.settings_menus.wifi_menu_gui"),
                            (l_get("apps.settings.menu1.sdcard"), 3),
                            (l_get("apps.settings.menu1.language"), "apps.settings_menus.language_gui"),
                            (l_get("apps.settings.menu1.about"), "apps.settings_menus.about_gui"),
                            (l_get("apps.settings.menu1.factory"), 4),
                            (l_get("apps.settings.menu1.backups"), "apps.settings_menus.backups_gui"),
                            (l_get("apps.settings.menu1.show_guides_again"), 1),
                            (l_get("apps.settings.menu1.updates"), "apps.settings_menus.update_gui"),
                            (l_get("menus.menu_close"), None)]) # ("Account", 10),
                
        # Show guides again
        if menu1 == 1:
            n_guides = cache.get_nvs("guides")
            nvs.set_int(n_guides, 'quick_start', 0)
            nvs.set_int(n_guides, 'account_popup', 0)
            popup.show(l_get("apps.settings.guides.reboot_notify"), l_get("popups.info"))
        
        # Neopixel settings
        elif menu1 == 2:
            if not osc.HAS_NEOPIXEL:
                popup.show(l_get("apps.settings.neopixel.no_neo_popup"), l_get("popups.info"))
                continue
            
            run_gui("apps.settings_menus.neopixel_gui")
                
        # SD Card settings
        elif menu1 == 3:
            # SD Slot check
            if not osc.HAS_SD_SLOT or nvs.get_int(n_settings, "sd_overwrite") == 1:
                popup.show(l_get("apps.settings.sd.no_slot_detected_popup"), l_get("crashes.error"), 10)
                continue
            
            run_gui("apps.settings_menus.sd_gui")
                
        # Factory
        elif menu1 == 4:
            confirm_reset = menus.menu(l_get("apps.settings.factory.reset_all"),
                                       [(l_get("menus.no"), None),
                                        (l_get("menus.yes"), 1)])
            if confirm_reset == 1:
                confirm_reset = menus.menu(l_get("apps.settings.factory.it_removes_all"),
                                           [(l_get("menus.menu_cancel"), 2),
                                            (l_get("apps.settings.factory.confirm"), 1)])
                if confirm_reset == 1:
                    nvs.set_int(n_updates, "factory", 1) # Set NVS bootloader entry
                    machine.soft_reset() # Reboot
                    
        # Run others if not None
        elif menu1:
            run_gui(menu1)
            
        else:
            work = False
            
        
    gc.collect()
    ps.loop()