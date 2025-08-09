import gc
import os
import machine

import modules.cache as cache
import modules.menus as menus
import modules.wifi_master as wmaster

def run():
        menu = []
        menu.append(("CPU freq: " + (str(machine.freq() // 1000000)) + "MHz", None))
        menu.append(("Ram free: " + (str(gc.mem_free() / 1024)) + "KB", None))
        menu.append(("Ram used: " + (str(gc.mem_alloc() / 1024)) + "KB", None))
        menu.append(("Version: " + cache.get("ver_displayname"), None))
        menu.append(("rand_extra_func: " + str(cache.get("rand_extra_func")), None))
        menu.append(("MPY Ver: " + str(os.uname().release), None))
        menu.append(("Wifi mac: " + wmaster.get_wifi_mac(), None))
        menu.append(("Close", None))
        menus.menu("Hardware info", menu)