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

def run():
    _LOAD_IO()
    n_settings = cache.get_nvs('settings')
    n_updates = cache.get_nvs('updates')
    
    work = True
    while work:
        # Main menu
        menu1 = menus.menu(l_get("apps.settings.name"),
                           [(l_get("apps.clock.name"), 0),
                            (l_get("apps.settings.menu1.lcd"), 1),
                            (l_get("apps.settings.menu1.power"), 50),
                            (l_get("apps.settings.menu1.neopixel"), 5),
                            (l_get("apps.settings.menu1.sound"), 2),
                            (l_get("apps.settings.menu1.wifi"), 3),
                            (l_get("apps.settings.menu1.sdcard"), 7),
                            (l_get("apps.settings.menu1.language"), 11),
                            (l_get("apps.settings.menu1.about"), 8),
                            (l_get("apps.settings.menu1.factory"), 9),
                            (l_get("apps.settings.menu1.backups"), 10),
                            (l_get("apps.settings.menu1.show_guides_again"), 12),
                            (l_get("menus.menu_close"), None)]) # ("Account", 10),
        
        # Power settings
        if menu1 == 50:
            import apps.settings_menus.power_menu_gui as pm_gui
            pm_gui.run()
            decache("apps.settings_menus.power_menu_gui")
            del pm_gui
                
        # Show guides again
        elif menu1 == 12:
            n_guides = cache.get_nvs("guides")
            nvs.set_int(n_guides, 'quick_start', 0)
            nvs.set_int(n_guides, 'account_popup', 0)
            popup.show(l_get("apps.settings.guides.reboot_notify"), l_get("popups.info"))
            
        # Clock
        elif menu1 == 0:
            import apps.settings_menus.clock_gui as c_gui
            c_gui.run()
            decache("apps.settings_menus.clock_gui")
            del c_gui
                
        # Langs
        elif menu1 == 11:
            import apps.settings_menus.language_gui as l_gui
            l_gui.run()
            decache("apps.settings_menus.language_gui")
            del l_gui
            
        # LCD / st7789 settings
        elif menu1 == 1:
            import apps.settings_menus.lcd_settings as l_gui
            l_gui.run()
            decache("apps.settings_menus.lcd_settings")
            del l_gui
                        
        # Sound settings
        elif menu1 == 2:
            import apps.settings_menus.sound_gui as s_gui
            s_gui.run()
            decache("apps.settings_menus.sound_gui")
        
        # Neopixel settings
        elif menu1 == 5:
            if not osc.HAS_NEOPIXEL:
                popup.show(l_get("apps.settings.neopixel.no_neo_popup"), l_get("popups.info"))
                continue
            
            import apps.settings_menus.neopixel_gui as np_gui
            np_gui.run()
            decache("apps.settings_menus.neopixel_gui")
            del np_gui
                    
        # Wi-Fi settings
        elif menu1 == 3:
            import apps.settings_menus.wifi_menu_gui as wm_gui
            wm_gui.run()
            decache("apps.settings_menus.wifi_menu_gui")
            del wm_gui
                
        # SD Card settings
        elif menu1 == 7:
            # SD Slot check
            if not osc.HAS_SD_SLOT or nvs.get_int(n_settings, "sd_overwrite") == 1:
                popup.show(l_get("apps.settings.sd.no_slot_detected_popup"), l_get("crashes.error"), 10)
                continue
            
            import apps.settings_menus.sd_gui as s_gui
            s_gui.run()
            decache("apps.settings_menus.sd_gui")
            del s_gui
        
        # About screen
        elif menu1 == 8:
            import apps.settings_menus.about_gui as a_gui
            a_gui.run()
            decache("apps.settings_menus.about_gui")
            del a_gui
                
        # Factory
        elif menu1 == 9:
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
        
        # Backups
        elif menu1 == 10:
            import apps.settings_menus.backups_gui as b_gui
            b_gui.run()
            decache("apps.settings_menus.backups_gui")
            del b_gui
            
        else:
            work = False
            
        
    gc.collect()
    ps.set_freq(osc.BASE_FREQ)