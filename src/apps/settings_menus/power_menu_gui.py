"""
Power menu settings GUI
"""

import modules.menus as menus
from modules.decache import decache
from modules.translate import get as l_get


def run():
    """Power menu settings GUI"""
    power_menu = menus.menu(l_get("apps.settings.power.title"), [
        (l_get("apps.settings.power.pwr_saving"), 1),
        (l_get("apps.settings.power.shutdown_mode"), 2),
        (l_get("menus.menu_close"), None)
    ])
    
    # Power saving settings
    if power_menu == 1:
        import apps.settings_menus.power_saver_gui as ps_gui
        ps_gui.run()
        decache("apps.settings_menus.power_saver_gui")
        del ps_gui
    
    # Shutdown mode settings
    elif power_menu == 2:
        import apps.settings_menus.shutdown_mode_gui as sm_gui
        sm_gui.run()
        decache("apps.settings_menus.shutdown_mode_gui")
        del sm_gui