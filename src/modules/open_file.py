"""
Context menu helper for Stick firmware
"""

import sys as nisysa

import modules.io_manager as io_man
import modules.menus as menus
from modules.translate import get as l_get

button_a = io_man.get('button_a')
button_b = io_man.get('button_b')
button_c = io_man.get('button_c')
tft = None

def matches_pattern(filename: str, pattern: str) -> bool:
    """
    Check if filename matches pattern
    
    Args:
        filename (str): Filename to check
        pattern (str): Pattern
    
    Returns:
        bool: True if matches, False if not
    """
    if pattern == "*":
        return True
    elif pattern == "*.*":
        return "." in filename
    elif pattern.startswith("*."):
        ext = pattern[2:]
        return filename.lower().endswith("." + ext.lower())
    return False
    
def get_supported_apps(apps_config: dict, filename: str) -> list[tuple]:
    """
    Get supported apps menu
    
    Args:
        apps_config (dict): JSON dict of apps config
        filename (str): Filename to open
    
    Returns:
        list[tuple]: List to display in menus.menu
    """
    menu = []
    for i, app in enumerate(apps_config["apps"]):
        for pattern in app.get("handleExtensions", []):
            if matches_pattern(filename, pattern):
                menu.append((app["name"], i))
                break
    menu.append((l_get("menus.menu_exit"), None))
    return menu
    
def openMenu(file: str):
    """
    Open file open context menu
    
    Args:
        filename (str): Filename to open
    """
    import modules.oobe as oobe
    appsConfig = oobe.read_config()
    supportedAppsMenu = get_supported_apps(appsConfig, file)
    selected_index = menus.menu(l_get("apps.file_explorer.open_in"), supportedAppsMenu)
    if selected_index is not None:
        app_index = selected_index
        app = appsConfig["apps"][app_index]
        modpath = app["file"]
        parts = modpath.split(".")
        comd = __import__(modpath)
        for part in parts[1:]:
            comd = getattr(comd, part)
        # Support for legacy apps
        if hasattr(comd, "set_btf"):
            button_a = io_man.get('button_a')
            button_b = io_man.get('button_b')
            button_c = io_man.get('button_c')
            tft = io_man.get('tft')
            comd.set_btf(button_a, button_b, button_c, tft)
        if hasattr(comd, "open_file"):
            comd.open_file(file)

        if modpath in nisysa.modules:
            del nisysa.modules[modpath]
