import time
import machine
import esp32

import fonts.def_8x8 as f8x8

import modules.os_constants as osc
import modules.io_manager as io_man
import modules.nvs as nvs
import modules.menus as menus
    
tft = io_man.get('tft')

def dummyMsg():
    tft.fill(0)
    tft.text(f8x8, "Dummy mode",0,0,65535)
    tft.text(f8x8, "Locks your device to clock!",0,8,65535)
    tft.text(f8x8, "To unlock press button A+B",0,24,65535)
    tft.text(f8x8, "at once for around 1 second.",0,32,65535)
    tft.text(f8x8, "This will stay even after",0,48,65535)
    tft.text(f8x8, "reboots! You need to unlock",0,56,65535)
    tft.text(f8x8, "it first with button combo!",0,64,65535)
    time.sleep(5)

def run():
    global tft
    tft = io_man.get('tft')

    n_locks = esp32.NVS("locks")
    work = True
    while work == True:
        if nvs.get_int(n_locks, "dummy") == 0:
            lockmen = menus.menu("Lock menu", [("Dummy mode", 1), ("Dummy mode with PIN", 2), ("Cancel", 13)])
            if lockmen == 1:
                machine.freq(osc.BASE_FREQ)
                nvs.set_int(n_locks, "dummy", 1)
                dummyMsg()
            if lockmen == 2:
                machine.freq(osc.BASE_FREQ)
                import modules.numpad as npad
                pin = npad.numpad("Enter PIN", 6, True)
                if pin == None or pin == "":
                    tft.fill(0)
                    tft.text(f8x8, "Set PIN first",0,0,65535)
                    time.sleep(1)
                    return
                if len(pin) < 4:
                    tft.fill(0)
                    tft.text(f8x8, "PIN too short",0,0,65535)
                    time.sleep(1)
                    return
                nvs.set_int(n_locks, "dummy", 2)
                nvs.set_string(n_locks, "pin", str(pin))
                dummyMsg()
            else:
                machine.freq(osc.BASE_FREQ)
            work = False
        elif nvs.get_int(n_locks, "dummy") == 1:
            lockmen = menus.menu("Lock menu", [("Disable dummy mode", 1), ("Cancel", 13)])
            if lockmen == 1:
                machine.freq(osc.BASE_FREQ)
                nvs.set_int(n_locks, "dummy", 0)
                tft.fill(0)
                tft.text(f8x8, "Disabled dummy mode!",0,0,65535)
                if nvs.get_string(n_locks, "pin") != "":
                    nvs.set_string(n_locks, "pin", "")
                time.sleep(2)
                work = False
            else:
                machine.freq(osc.BASE_FREQ)
                work = False
                if nvs.get_string(n_locks, "pin") != "":
                    nvs.set_int(n_locks, "dummy", 2)
        elif nvs.get_int(n_locks, "dummy") == 2:
            import modules.numpad as npad
            pin = npad.numpad("Enter PIN", 6, True)
            if pin == nvs.get_string(n_locks, "pin"):
                nvs.set_int(n_locks, "dummy", 1)
            else:
                tft.fill(0)
                tft.text(f8x8, "Invalid PIN!",0,0,65535)
                work = False
