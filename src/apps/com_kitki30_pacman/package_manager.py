import modules.menus as menus
import modules.popup as popup
import modules.oobe as oobe
from modules.oobe import get_entry
from modules.printer import log

appsConfig = oobe.read_config()

def get_all_apps():
    results = []
    for app in appsConfig.get("apps", []):
        results.append((app["name"], app["id"]))
    return results

def app_menu(id):
    while True:
        menu = menus.menu(get_entry(id, "name"), [
            ("Uninstall", 1),
            ("Close", None)
        ])
        
        if menu == None:
            break
        if menu == 1:
            import modules.handle_apps as happs
            try:
                happs.uninstall(id)
                popup.show("App uninstalled successfully!", "Info")
                break
            except happs.CannotUninstallSystemApp:
                popup.show("Cannot uninstall system apps!", "Error")
            except happs.NoAppFolderFound:
                popup.show("App doesn't have a folder, maybe it's a helper for some other app?", "Error")
            except Exception as e:
                log(f"An unknown error happened in Package manager!!!\nFeature: Uninstall\nApp ID: {id}\nError:\n{e}")

def show_info(id):
    text = f"Name: {get_entry(id, 'name')}\nID: {get_entry(id, 'id')}\nFolder: {get_entry(id, 'main_folder')}\nSystem app?: {get_entry(id, 'is_system_app')}\nDependency?: {get_entry(id, 'dependency')}"
    
    popup.show(text, "Package info")
    
    app_menu(id)

def run():
    while True:
        apps = get_all_apps()
        apps.append(("Exit", None))
        app_select_dialog = menus.menu("Package manager", apps)
        
        if app_select_dialog == None:
            break
        
        show_info(app_select_dialog)