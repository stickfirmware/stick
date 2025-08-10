import os

from modules.random_func_checker import check_random_extra_functions
from modules.printer import log
import modules.os_constants as osc
import modules.nvs as nvs
import modules.cache as cache

_RANDOM_FUNC_BANLIST = [
    "/apps/dice.py"
]

def del_it_all(list):
    for file in list:
        try:
            os.remove(file)
            log("Deleted: " + file)
        except:
            log("Failed to delete: " + file)

def postinstall():
    log("Postinstall - deleting files")
    del_it_all(osc.POSTINSTALL_BLACKLIST)

    log("Postinstall - checking random extra func")
    if check_random_extra_functions(): 
        log("Great! Random extra functions are enabled!")
    else:
        log("Random extra func disabled :( Deleting things that depend on that") 
        del_it_all(_RANDOM_FUNC_BANLIST)

    log("Postinstall - setting NVS")
    n_updates = cache.get_nvs('updates')
    nvs.set_int(n_updates, "postinstall", 0)