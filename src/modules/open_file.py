import sys as nisysa

import modules.menus as menus
import modules.json as json
import modules.io_manager as io_man

button_a = io_man.get('button_a')
button_b = io_man.get('button_b')
button_c = io_man.get('button_c')
tft = io_man.get('tft')

def matchesPattern(filename, pattern):
    if pattern == "*":
        return True
    elif pattern == "*.*":
        return "." in filename
    elif pattern.startswith("*."):
        ext = pattern[2:]
        return filename.lower().endswith("." + ext.lower())
    return False
    
def getSupportedApps(appsConfig, filename):
    menu = []
    for i, app in enumerate(appsConfig["apps"]):
        for pattern in app.get("handleExtensions", []):
            if matchesPattern(filename, pattern):
                menu.append((app["name"], i))
                break
    menu.append(("Exit", None))
    return menu
    
def openMenu(file):
    import apps.oobe as oobe
    appsConfig = oobe.read_config()
    supportedAppsMenu = getSupportedApps(appsConfig, file)
    selected_index = menus.menu("Open in", supportedAppsMenu)
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
