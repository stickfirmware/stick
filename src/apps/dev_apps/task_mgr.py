import gc
import modules.menus as menus

def run():
        menu = []
        menu.append("Ram free: "(str(gc.mem_free() / 1024) + "KB", None))
        menu.append("Ram used: "(str(gc.mem_alloc() / 1024) + "KB", None))
        menu.append(("Close", None))
        menus.menu("Hardware info", menu)