import sys as nisysa
import modules.menus as menus
import modules.json as json

button_a = None
button_b = None
button_c = None
tft = None

def set_btf(bta, btb, btc, ttft):
    global button_a
    global button_b
    global button_c
    global tft
    
    button_a = bta
    button_b = btb
    button_c = btc
    tft = ttft

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
    appsConfig = json.read("/usr/config/apps.json")
    supportedAppsMenu = getSupportedApps(appsConfig, file)
    selected_index = menus.menu("Open in", supportedAppsMenu)
    if selected_index is not None:
        print(supportedAppsMenu)
        app_index = selected_index
        app = appsConfig["apps"][app_index]
        print(app)
        modpath = app["file"]
        parts = modpath.split(".")
        comd = __import__(modpath)
        for part in parts[1:]:
            comd = getattr(comd, part)
        if hasattr(comd, "set_btf"):
            comd.set_btf(button_a, button_b, button_c, tft)
        if hasattr(comd, "openFile"):
            comd.openFile(file)

        if modpath in nisysa.modules:
            del nisysa.modules[modpath]
