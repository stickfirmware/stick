"""
First boot checker for Stick firmware
"""
import modules.nvs as nvs
import modules.cache as cache
import modules.printer as printer
from modules.printer import Levels as log_levels

def check():
    """
    Makes configs and user folders
    """
    n_boot = cache.get_nvs("boot")
    if nvs.get_int(n_boot, "firstBoot") is None:
        printer.log("Devices first boot, configuring NVS.")
    
        # Boot config
        printer.log("Configuring 'boot' NVS", log_levels.DEBUG)
        nvs.set_int(n_boot, "firstBoot", 1)
        printer.log("boot:firstBoot:1", log_levels.DEBUG)
        
        import modules.oobe as oobe
        oobe.createUserFolder()
        oobe.createConfig()