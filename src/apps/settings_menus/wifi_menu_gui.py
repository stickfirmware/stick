"""
Main menu for all the wifi settings
"""

import modules.menus as menus
from modules.decache import decache
from modules.translate import get as l_get


def run():
    while True:
        rendr =  menus.menu(l_get("apps.settings.wifi.title"), 
                            [(l_get("apps.settings.wifi.setup_ap"), 1),
                                (l_get("apps.settings.wifi.connection"), 2),
                                (l_get("apps.settings.wifi.status"), 5),
                                (l_get("menus.menu_close"), 13)])
        
        # Wi-Fi AP setup
        if rendr == 1:
            import apps.settings_menus.wifi_setup_gui as ws_gui
            ws_gui.run()
            decache("apps.settings_menus.wifi_setup_gui")
            del ws_gui
            
        # Wi-Fi connection
        elif rendr == 2:
            import apps.settings_menus.wifi_connect_gui as wc_gui
            wc_gui.run()
            decache("apps.settings_menus.wifi_connect_gui")
            del wc_gui

        # Wi-Fi status
        elif rendr == 5:
            import apps.settings_menus.wifi_status_gui as w_gui
            w_gui.run()
            decache("apps.settings_menus.wifi_status_gui")
            del w_gui
            
        else:
            break