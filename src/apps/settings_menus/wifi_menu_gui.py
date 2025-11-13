"""
Main menu for all the wifi settings
"""

import apps.settings as settings
import modules.menus as menus
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
            settings.run_gui("apps.settings_menus.wifi_setup_gui")
            
        # Wi-Fi connection
        elif rendr == 2:
            settings.run_gui("apps.settings_menus.wifi_connect_gui")

        # Wi-Fi status
        elif rendr == 5:
            settings.run_gui("apps.settings_menus.wifi_status_gui")
            
        else:
            break