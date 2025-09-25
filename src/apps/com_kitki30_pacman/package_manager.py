import modules.menus as menus
import modules.popup as popup
import modules.oobe as oobe
from modules.oobe import get_entry
from modules.printer import log
from modules.translate import get as l_get

appsConfig = oobe.read_config()

def get_all_apps():
    results = []
    for app in appsConfig.get("apps", []):
        results.append((app["name"], app["id"]))
    return results

def app_menu(id):
    while True:
        menu = menus.menu(get_entry(id, "name"), [
            (l_get("apps.package_manager.uninstall"), 1),
            (l_get("menus.menu_close"), None)
        ])
        
        if menu == None:
            break
        if menu == 1:
            import modules.handle_apps as happs
            try:
                happs.uninstall(id)
                popup.show(l_get("apps.package_manager.success"), l_get("popups.info"))
                break
            except happs.CannotUninstallSystemApp:
                popup.show(l_get("apps.package_manager.sys_app_error"), l_get("crashes.error"))
            except happs.NoAppFolderFound:
                popup.show(l_get("apps.package_manager.folder_error"), l_get("crashes.error"))
            except Exception as e:
                log(f"An unknown error happened in Package manager!!!\nFeature: Uninstall\nApp ID: {id}\nError:\n{e}")
                raise Exception

def show_info(id):
    text = f"{l_get("apps.package_manager.popup_name")} {get_entry(id, 'name')}\n{l_get("apps.package_manager.popup_id")} {get_entry(id, 'id')}\n{l_get("apps.package_manager.popup_folder")} {get_entry(id, 'main_folder')}\n{l_get("apps.package_manager.popup_system")} {get_entry(id, 'is_system_app')}\n{l_get("apps.package_manager.popup_dependency")} {get_entry(id, 'dependency')}"
    
    popup.show(text, l_get("popups.info"))
    
    app_menu(id)

def run():
    while True:
        apps = get_all_apps()
        apps.append((l_get("menus.menu_exit"), None))
        app_select_dialog = menus.menu(l_get("apps.package_manager.name"), apps)
        
        if app_select_dialog == None:
            break
        
        show_info(app_select_dialog)