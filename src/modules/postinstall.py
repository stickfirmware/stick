"""
Postinstalling script for Stick firmware
"""

import os

import modules.cache as cache
import modules.nvs as nvs
import modules.os_constants as osc
from modules.printer import Levels as log_levels
from modules.printer import log
from modules.random_func_checker import check_random_extra_functions

# File list if there are no random extra func
_RANDOM_FUNC_BANLIST = [
    "p:apps/dice"
]
"""Banlist for RANDOM_EXTRA_FUNC, postinstall deletes all this files if extra func not detected"""

# Delete entire list of files
def del_it_all(list: list[str]):
    """
    Delete all files from list
    
    Note:
        Files in list need to start either with a: or p:
        p: - Python files, deletes both mpy and py version (ex. 'p:apps/dice')
        a: - All files, deletes any files, requires to provide file extension (ex. 'p:usr/config.json')
    
    Args:
        list (list[str]): Array of file paths
    """
    for file in list:
        # Flag files to delete
        deletions = []
        if file.startswith('a:'):
            deletions.append(file.replace('a:', ''))
        elif file.startswith('p:'):
            temp = file.replace('p:', '')
            deletions.append(temp + ".py")
            deletions.append(temp + ".mpy")
            
        # Delete
        for i in deletions:
            try:
                os.remove(i)
                log("Deleted: " + file, log_levels.DEBUG)
            except Exception:
                log("Failed to delete: " + file, log_levels.DEBUG)

def postinstall():
    """
    Delete all functions that are not supported on current device to save flash space
    """
    
    log("Postinstall started!")
    log("Postinstall - deleting files", log_levels.DEBUG)
    del_it_all(osc.POSTINSTALL_BLACKLIST)

    log("Postinstall - checking random extra func", log_levels.DEBUG)
    if check_random_extra_functions(): 
        log("Great! Random extra functions are enabled!", log_levels.DEBUG)
    else:
        log("Random extra func disabled :( Deleting things that depend on that", log_levels.DEBUG) 
        del_it_all(_RANDOM_FUNC_BANLIST)

    log("Postinstall - setting NVS", log_levels.DEBUG)
    n_updates = cache.get_nvs('updates')
    nvs.set_int(n_updates, "postinstall", 0)
    log("Postinstall success!")