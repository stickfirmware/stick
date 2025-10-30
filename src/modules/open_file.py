"""
Helper to open files in apps
"""

import gc
import sys

import modules.io_manager as io_man
import modules.menus as menus
import modules.oobe as oobe
from modules.printer import Levels as log_levels
from modules.printer import log
from modules.translate import get as l_get

# Check if filename matches pattern
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
    
def get_supported_apps(apps_config: dict, filename: str, use_legacy: bool = True) -> list[tuple]:
    """
    Get supported apps menu
    
    Args:
        apps_config (dict): JSON dict of apps config
        filename (str): Filename to open
        use_legacy (bool): If true it will append app index, if false it will append app ID (Default is True)
    
    Returns:
        list[tuple]: List to display in menus.menu
    """
    
    log("Getting supported apps from config", log_levels.DEBUG)
    menu = []
    for i, app in enumerate(apps_config["apps"]):
        for pattern in app.get("handleExtensions", []):
            if matches_pattern(filename, pattern):
                log(f"Found supported app {app['name']} for pattern {pattern}", log_levels.DEBUG)
                if use_legacy:
                    menu.append((app["name"], i))
                else:
                    menu.append((app["name"], app["id"]))
                break
    menu.append((l_get("menus.menu_exit"), None))
    return menu
        
def open_in(app_id: str, filename: str, ram_clean: bool = True):
    """
    Open file in app with package id you provided
    
    Args:
        id (str): Package ID to open file in
        filename (str): Filename to open
        ram_clean (bool, optional): Remoes the app with decache if True (Default)
    """
    log(f"Opening file {filename} in app ID: {app_id}")
    apps_config = oobe.read_config()
    
    # Find app by ID
    app = None

    for a in apps_config["apps"]:
        if a["id"] == app_id:
            app = a
            break
        
    if not app:
        log(f"App with ID {app_id} not found!", log_levels.WARNING)
        return

    modpath = app["file"]

    # Import the thing
    log("Importing app...", log_levels.DEBUG)
    gc.collect()
    module = __import__(modpath)
    for part in modpath.split(".")[1:]:
        module = getattr(module, part)

    # Iopen file
    log("Opening file...")
    gc.collect()
    if hasattr(module, "open_file"):
        module.open_file(filename)

    if ram_clean and modpath in sys.modules:
        del sys.modules[modpath]
        gc.collect()
    
def open_menu(file: str):
    appsConfig = oobe.read_config()
    supportedAppsMenu = get_supported_apps(appsConfig, file)
    selected_index = menus.menu(l_get("apps.file_explorer.open_in"), supportedAppsMenu)
    if selected_index is not None:
        app_index = selected_index
        open_in(app_index, file)  
        
def open_menu(filename: str):
    """
    Open file open context menu (GUI)
    
    Args:
        filename (str): Filename to open
    """
    # Read config and get supported apps
    apps_config = oobe.read_config()
    supported_apps_menu = get_supported_apps(apps_config, filename, False)
    
    # Request user input and open
    selected_id = menus.menu(l_get("apps.file_explorer.open_in"), supported_apps_menu)
    if selected_id is not None:
        open_in(selected_id, filename)

def openMenu(file: str):
    """Old func name for open_menu, to not break compatibility"""
    log("openMenu is deprecated, use open_menu instead", log_levels.WARNING)
    return open_menu(file)