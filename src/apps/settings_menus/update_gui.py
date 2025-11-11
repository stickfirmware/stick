"""
Update menu
"""

import modules.menus as menus
import modules.popup as popup
import version
from modules.translate import get as l_get


def run():
    sys_ver_format = version.version_to_str(version.get_parsed_version(), True)
    popup.show(f"Welcome to Stick firmware updater!\nCurrent system version: {sys_ver_format}", "Updater")
    
    while True:
        menu2 = menus.menu("Updater",
                            [("System update", 1),
                             ("Info", 2),
                            (l_get("menus.menu_close"), 13)])
        
        # Update
        if menu2 == 1:
            import modules.update_os as update
            update.update_interactive()
            break
        
        # Info
        elif menu2 == 2:
            popup.show("This updater will update your stick firmware with update package you provide. Get the update package from official github. Updates are made to save ram, so you can't update directly from 2.3.0 to 2.3.2, to update you will need to do 2.3.1 first then 2.3.2", "Info")
        
        else:
            break