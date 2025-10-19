"""
Context menu helper for Stick firmware
"""

import gc
import sys

import modules.io_manager as io_man
import modules.menus as menus
import modules.oobe as oobe
from modules.printer import Levels as log_levels
from modules.printer import log
from modules.translate import get as l_get

button_a = io_man.get('button_a')
button_b = io_man.get('button_b')
button_c = io_man.get('button_c')
tft = None

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
    
def get_supported_apps(apps_config: dict, filename: str) -> list[tuple]:
    """
    Get supported apps menu
    
    Args:
        apps_config (dict): JSON dict of apps config
        filename (str): Filename to open
    
    Returns:
        list[tuple]: List to display in menus.menu
    """
    
    log("Getting supported apps from config", log_levels.DEBUG)
    menu = []
    for i, app in enumerate(apps_config["apps"]):
        for pattern in app.get("handleExtensions", []):
            if matches_pattern(filename, pattern):
                log(f"Found supported app {app['name']} for pattern {pattern}", log_levels.DEBUG)
                menu.append((app["name"], i))
                break
    menu.append((l_get("menus.menu_exit"), None))
    return menu

def open_in(id: str, file: str, ram_clean: bool = True):
    """
    Open file in app with package id you provided
    
    Args:
        id (str): Package ID to open file in
        filename (str): Filename to open
    """
    
    log(f"Opening file {file} in app with ID: {id}")
    
    # Read OOBE config, get app, and format import path
    log("Reading OOBE config", log_levels.DEBUG)
    appsConfig = oobe.read_config() # Its cached, so it wont double read (If run with openMenu)
    app = appsConfig["apps"][id]
    modpath = app["file"]
    parts = modpath.split(".")
    
    # Import module
    log("Importing app...", log_levels.DEBUG)
    gc.collect() # Collect before import again
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
        
    # Collect before running app
    gc.collect()
        
    # Open app
    log("Running app open_file...", log_levels.DEBUG)
    if hasattr(comd, "open_file"):
        comd.open_file(file)

    # Delete from path (To keep ram, can be overwritten with ram_clean = False)
    if modpath in sys.modules and ram_clean:
        del sys.modules[modpath]
        gc.collect()
    
def open_menu(file: str):
    """
    Open file open context menu (GUI)
    
    Args:
        filename (str): Filename to open
    """
    appsConfig = oobe.read_config()
    supportedAppsMenu = get_supported_apps(appsConfig, file)
    selected_index = menus.menu(l_get("apps.file_explorer.open_in"), supportedAppsMenu)
    if selected_index is not None:
        app_index = selected_index
        open_in(app_index, file)  

def openMenu(file: str):
    """Old func name for open_menu, to not break compatibility"""
    log("openMenu is deprecated, use open_menu instead", log_levels.WARNING)
    return open_menu(file)