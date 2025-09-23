import machine

import modules.popup as popup

def help():
    popup.show("Available commands:\nfastrecovery - Go into recovery quickly\nhelp - Show this help message\nreboot - Reboot the device\nhardreboot - Hard reboot the device (power cycle)", "Debug console")
    
def run_code(cmd):
    if cmd == "reboot":
        machine.soft_reset()
    elif cmd == "hardreboot":
        machine.reset()
    elif cmd == "help":
        help()