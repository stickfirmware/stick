import os
import esp32

from modules.printer import log
import modules.os_constants as osc
import modules.nvs as nvs

def postinstall():
    log("Postinstall - deleting files")
    for file in osc.POSTINSTALL_BLACKLIST:
        try:
            os.remove(file)
            log("Deleted: " + file)
        except:
            log("Failed to delete: " + file)
    log("Postinstall - setting NVS")
    n_updates = esp32.NVS("updates")
    nvs.set_int(n_updates, "postinstall", 0)