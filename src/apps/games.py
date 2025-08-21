import gc

from modules.decache import decache
import modules.menus as menus
import modules.os_constants as osc
import modules.powersaving as ps

def run():    
    menu_apps = [("Minesweeper", 1)]
    menu_apps.append(("Close", None))

    menu1 = menus.menu("Menu", menu_apps)
    if menu1 == 1:
        import apps.minesweeper as a_ms
        a_ms.run()
        del a_ms
        decache('apps.minesweeper')
    gc.collect()
    ps.set_freq(osc.BASE_FREQ)