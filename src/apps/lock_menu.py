import time

import fonts.def_8x8 as f8x8

import modules.os_constants as osc
import modules.io_manager as io_man
import modules.nvs as nvs
import modules.powersaving as ps
import modules.menus as menus
import modules.cache as cache
import modules.hashing as hashing
from modules.translate import get as l_get

tft = io_man.get('tft')

def dummyMsg():
    tft.fill(0)
    tft.text(f8x8, l_get("lock_menu.dummy_info_1"),0,0,65535)
    tft.text(f8x8, l_get("lock_menu.dummy_info_2"),0,8,65535)
    tft.text(f8x8, l_get("lock_menu.dummy_info_3"),0,24,65535)
    tft.text(f8x8, l_get("lock_menu.dummy_info_4"),0,32,65535)
    tft.text(f8x8, l_get("lock_menu.dummy_info_5"),0,48,65535)
    tft.text(f8x8, l_get("lock_menu.dummy_info_6"),0,56,65535)
    tft.text(f8x8, l_get("lock_menu.dummy_info_7"),0,64,65535)
    time.sleep(5)

def run():
    global tft
    tft = io_man.get('tft')

    n_locks = cache.get_nvs('locks')
    work = True
    while work == True:
        if nvs.get_int(n_locks, "dummy") == 0:
            lockmen = menus.menu(l_get("lock_menu.name"), 
                                 [(l_get("lock_menu.dummy_mode"), 1),
                                  (l_get("lock_menu.dummy_with_pin"), 2),
                                  (l_get("menus.menu_close"), 13)])
            if lockmen == 1:
                ps.set_freq(osc.BASE_FREQ)
                nvs.set_int(n_locks, "dummy", 1)
                dummyMsg()
            if lockmen == 2:
                ps.set_freq(osc.BASE_FREQ)
                import modules.numpad as npad
                pin = npad.numpad(l_get("lock_menu.enter_pin"), 6, True)
                if pin == None or pin == "":
                    tft.fill(0)
                    tft.text(f8x8, l_get("lock_menu.set_pin_first"),0,0,65535)
                    time.sleep(1)
                    return
                if len(pin) < 4:
                    tft.fill(0)
                    tft.text(f8x8, l_get("lock_menu.pin_too_short"),0,0,65535)
                    time.sleep(1)
                    return
                nvs.set_int(n_locks, "dummy", 2)
                tft.fill(0)
                tft.text(f8x8, l_get("lock_menu.making_sure_1"),0,0,65535)
                tft.text(f8x8, l_get("lock_menu.making_sure_2"),0,8,65535)
                tft.text(f8x8, l_get("lock_menu.making_sure_3"),0,16,65535)
                pin_hash, salt = hashing.hash_pin(pin, 5000)
                nvs.set_string(n_locks, "pin", str(pin_hash))
                nvs.set_string(n_locks, "salt", salt)
                dummyMsg()
            else:
                ps.set_freq(osc.BASE_FREQ)
            work = False
        elif nvs.get_int(n_locks, "dummy") == 1:
            lockmen = menus.menu(l_get("lock_menu.name"), 
                                 [(l_get("lock_menu.disable_dummy"), 1),
                                  (l_get("menus.menu_close"), 13)])
            if lockmen == 1:
                ps.set_freq(osc.BASE_FREQ)
                nvs.set_int(n_locks, "dummy", 0)
                tft.fill(0)
                tft.text(f8x8, l_get("lock_menu.disabled"),0,0,65535)
                if nvs.get_string(n_locks, "pin") != "":
                    nvs.set_string(n_locks, "pin", "")
                    nvs.set_string(n_locks, "salt", "")
                time.sleep(2)
                work = False
            else:
                ps.set_freq(osc.BASE_FREQ)
                work = False
                if nvs.get_string(n_locks, "pin") != "":
                    nvs.set_int(n_locks, "dummy", 2)
        elif nvs.get_int(n_locks, "dummy") == 2:
            import modules.numpad as npad
            pin = npad.numpad(l_get("lock_menu.enter_pin"), 6, True)
            tft.fill(0)
            tft.text(f8x8, l_get("lock_menu.verify_hash_1"),0,0,65535)
            tft.text(f8x8, l_get("lock_menu.verify_hash_2"),0,8,65535)
            if hashing.verify_pin(pin, nvs.get_string(n_locks, "salt"), nvs.get_string(n_locks, "pin"), 5000):
                nvs.set_int(n_locks, "dummy", 1)
            else:
                tft.fill(0)
                tft.text(f8x8, l_get("lock_menu.invalid_pin"),0,0,65535)
                work = False
