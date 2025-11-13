"""
Power menu settings GUI
"""

import apps.settings as settings
import modules.menus as menus
from modules.translate import get as l_get


def run():
    """Power menu settings GUI"""
    
    while True:
        power_menu = menus.menu(l_get("apps.settings.power.title"), [
            (l_get("apps.settings.power.pwr_saving"), 1),
            (l_get("apps.settings.power.shutdown_mode"), 2),
            ("Performance mode", 3),
            (l_get("menus.menu_close"), None)
        ])
        
        # Power saving settings
        if power_menu == 1:
            settings.run_gui("apps.settings_menus.power_saver_gui")
        
        # Shutdown mode settings
        elif power_menu == 2:
            settings.run_gui("apps.settings_menus.shutdown_mode_gui")

        # Performance mode
        elif power_menu == 3:
            settings.run_gui("apps.settings_menus.performance_enabler_gui")

        else:
            break