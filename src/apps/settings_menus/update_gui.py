"""
Update menu
"""

import modules.menus as menus
import modules.popup as popup
import version
from modules.translate import get as l_get


def run():
    sys_ver_format = version.version_to_str(version.get_parsed_version(), True)
    popup.show(l_get("apps.settings.update.updater_gui.welcomer").replace("%sys_ver%", sys_ver_format), l_get("apps.settings.update.updater_gui.name"))
    
    while True:
        menu2 = menus.menu(l_get("apps.settings.update.updater_gui.name"),
                            [(l_get("apps.settings.update.updater_gui.system_update"), 1),
                             (l_get("apps.settings.update.updater_gui.info"), 2),
                            (l_get("menus.menu_close"), 13)])
        
        # Update
        if menu2 == 1:
            import modules.update_os as update
            update.update_interactive()
            break
        
        # Info
        elif menu2 == 2:
            popup.show(l_get("apps.settings.update.updater_gui.info_popup"), l_get("popups.info"))
        
        else:
            break