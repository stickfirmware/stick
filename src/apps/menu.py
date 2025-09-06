import gc

import modules.io_manager as io_man
from modules.decache import decache
import modules.menus as menus
import modules.os_constants as osc
import modules.nvs as nvs
import modules.powersaving as ps
import modules.cache as cache
from modules.translate import get as l_get

n_settings = cache.get_nvs('settings')

dev_settings = nvs.get_int(n_settings, "dev_apps")
if dev_settings == None:
    dev_settings = 0
    
def search_apps():
    import apps.oobe as oobe
    appsConfig = oobe.read_config()
    
    results = []
    for app in appsConfig.get("apps", []):
        if not app.get("hidden", False) and not app.get("dependency", False) and app.get("file"):
            results.append((app["name"], app["id"]))
    return results

def run():    
    menu_apps = [(l_get("apps.ir_remote.name"), 1),
                 (l_get("apps.file_explorer.name"), 7),
                 (l_get("apps.flashlight.name"), 8),
                 (l_get("apps.games.name"), 5),
                 (l_get("apps.others.name"), 4),
                 (l_get("apps.custom_apps.name"), 10),
                 (l_get("apps.settings.name"), 3)]
    if dev_settings == 1:
        menu_apps.append(("Developer apps", 99))
    menu_apps.append((l_get("menus.menu_close"), 13))

    menu1 = menus.menu(l_get("menus.app_menu_title"), menu_apps)
    if menu1 == 3:
        import apps.settings as a_se
        a_se.run()
        del a_se
        decache('apps.settings')
    elif menu1 == 4:
        import apps.others as a_ot
        a_ot.run()
        del a_ot
        decache('apps.others')
    elif menu1 == 1:
        import apps.IR as a_ir
        a_ir.run()
        del a_ir
        decache('apps.IR')
    elif menu1 == 7:
        import modules.file_explorer as a_fe
        a_fe.run()
        del a_fe
        decache('modules.file_explorer')
    elif menu1 == 8:
        import apps.flashlight as a_fl
        a_fl.run()
        del a_fl
        decache('apps.flashlight')
    elif menu1 == 5:
        import apps.games as a_g
        a_g.run()
        del a_g
        decache('apps.games')
    elif menu1 == 10:
        menu_selections = search_apps()
        menu_selections.append((l_get("menus.menu_close"), None))
        c_apps_menu = menus.menu(l_get("apps.custom_apps.name"), menu_selections)
        if c_apps_menu is not None:
            import modules.open_app as open_app
            open_app.run(c_apps_menu)
    elif menu1 == 99:
        import apps.dev_apps.dev_menu as d_dev
        d_dev.run()
        del d_dev
        decache('apps.dev_apps.dev_menu')
    gc.collect()
    ps.set_freq(osc.BASE_FREQ)