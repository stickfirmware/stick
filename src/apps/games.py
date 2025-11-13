import gc

import modules.menus as menus
import modules.powersaving as ps
from modules.decache import decache
from modules.translate import get as l_get


def run():
    menu_apps = [(l_get("apps.minesweeper.name"), 1)]
    menu_apps.append((l_get("menus.menu_close"), None))

    menu1 = menus.menu(l_get("apps.games.name"), menu_apps)
    if menu1 == 1:
        import apps.minesweeper as a_ms
        a_ms.run()
        del a_ms
        decache('apps.minesweeper')
    gc.collect()
    ps.loop()