import machine

import modules.popup as popup
import modules.nvs as nvs
import modules.cache as cache

def help():
    popup.show("Available commands:\nfastrecovery - Go into recovery quickly\nhelp - Show this help message\nreboot - Reboot the device\nhardreboot - Hard reboot the device (power cycle)\ntoggledeveloper - Toggle dev apps", "Debug console")
    
def run_code(cmd):
    
    # Reboot
    if cmd == "reboot":
        machine.soft_reset()
        
    # Hard reboot
    elif cmd == "hardreboot":
        machine.reset()
        
    # Togle developer apps
    elif cmd == "toggledeveloper":
        n_settings = cache.get_nvs('settings')
        dev_settings = nvs.get_int(n_settings, "dev_apps")
        if dev_settings == 1:
            nvs.set_int(n_settings, "dev_apps", 0)
        else:
            nvs.set_int(n_settings, "dev_apps", 1)
            
    # Help
    elif cmd == "help":
        help()