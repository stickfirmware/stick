import gc

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
    import modules.oobe as oobe
    appsConfig = oobe.read_config()
    
    results = []
    for app in appsConfig.get("apps", []):
        if not app.get("hidden", False) and not app.get("dependency", False) and app.get("file"):
            results.append((app["name"], app["id"]))
    return results

def run():    
    menu_apps = search_apps()
    menu_apps.extend([(l_get("apps.games.name"), 1),
                    (l_get("apps.others.name"), 2),
                    (l_get("apps.settings.name"), 3)])
    if dev_settings == 1:
        menu_apps.append(("Developer apps", 99))
    menu_apps.append((l_get("menus.menu_close"), None))

    menu1 = menus.menu(l_get("menus.app_menu_title"), menu_apps)
    if menu1 == 3:
        import apps.settings as a_se
        a_se.run()
        del a_se
        decache('apps.settings')
    elif menu1 == 2:
        import apps.others as a_ot
        a_ot.run()
        del a_ot
        decache('apps.others')
    elif menu1 == 1:
        import apps.games as a_g
        a_g.run()
        del a_g
        decache('apps.games')
    elif menu1 == 99:
        import apps.dev_apps.dev_menu as d_dev
        d_dev.run()
        del d_dev
        decache('apps.dev_apps.dev_menu')
    elif menu1 != None:
        import modules.open_app as open_app
        open_app.run(menu1)
    gc.collect()
    ps.set_freq(osc.BASE_FREQ)