import json
import os
import time

import machine

import fonts.def_8x8 as f8x8
import modules.cache as cache
import modules.io_manager as io_man
import modules.IR.recv as recv
import modules.menus as menus
import modules.nvs as nvs
import modules.os_constants as osc
import modules.powersaving as ps
import modules.printer as printer
from modules.printer import Levels as log_levels
from modules.translate import get as l_get

button_a = io_man.get('button_a')
button_b = io_man.get('button_b')
button_c = io_man.get('button_c')
tft = None

n_settings = cache.get_nvs('settings')
pin_nvs = nvs.get_int(n_settings, "irPin")
if pin_nvs is None or pin_nvs not in osc.IR_ALLOWED_PINS:
    nvs.set_int(n_settings, "irPin", osc.IR_PIN)
    pin_nvs = osc.IR_PIN
printer.log("IR pin from NVS:" + repr(pin_nvs))
ir_pin = machine.PWM(machine.Pin(pin_nvs, machine.Pin.OUT), duty=0)
io_man.set('IR', ir_pin)

def run():
    global button_c, button_a, button_b, tft
    button_a = io_man.get('button_a')
    button_b = io_man.get('button_b')
    button_c = io_man.get('button_c')
    tft = io_man.get('tft')
    ps.set_freq(osc.BASE_FREQ)
    global ir_pin
    work = True
    while work:
        render = menus.menu(l_get("apps.ir_remote.name"), 
                             [(l_get("apps.ir_remote.menu.change_pin"), 8),
                             (l_get("apps.ir_remote.menu.receive"), 9),
                             (l_get("menus.menu_close"), 10)])
        # Change pin
        if render == 8:
            render_pins = []
            for pin in osc.IR_ALLOWED_PINS:
                render_pins.append(("GPIO"+str(pin), pin))
            render = menus.menu(l_get("apps.ir_remote.menu.change_pin"), render_pins)
            if render != 99 and render is not None:
                nvs.set_int(n_settings, "irPin", render)
            ir_pin = machine.PWM(machine.Pin(nvs.get_int(n_settings, "irPin"), machine.Pin.OUT), duty = 0)
            io_man.set('IR', ir_pin)
        elif render == 9:
            if not osc.ALLOW_IR_RECORD:
                printer.log("Device doesn't have support for recording IR signals, showing menu.", log_levels.WARNING)
                menus.menu(l_get("apps.ir_remote.menu.receive_no_support"), [(l_get("menus.menu_close"), 1)])
                continue
            works = True
            updat = True
            if "usr" not in os.listdir("/"):
                os.mkdir("/usr")
            if "ir" not in os.listdir("/usr/"):
                os.mkdir("/usr/ir")
            while works:
                time.sleep(osc.LOOP_WAIT_TIME)
                if updat:
                    tft.fill(0)
                    # Show receiver mode pinout
                    tft.text(f8x8, l_get("apps.ir_remote.receiver_mode.title"),0,0,65535)
                    tft.text(f8x8, l_get("apps.ir_remote.receiver_mode.pinout"),0,10,65535)
                    tft.text(f8x8, "GND - Recv GND / -",0,18,54937)
                    tft.text(f8x8, "3v3 (" + l_get("apps.ir_remote.receiver_mode.pinout_5v") + ") - VCC",0,26,63648)
                    tft.text(f8x8, "G26 - OUT / S",0,34,65535)
                    tft.text(f8x8, l_get("apps.ir_remote.receiver_mode.save_info"),0,48,65535)
                    tft.text(f8x8, l_get("apps.ir_remote.receiver_mode.a_to_continue"),0,56,65535)
                    tft.text(f8x8, l_get("apps.ir_remote.receiver_mode.c_to_exit"),0,64,65535)
                    updat = False
                if button_c.value() == 0:
                    works = False
                    continue
                if button_a.value() == 1:
                    continue
                tft.fill(0)
                tft.text(f8x8, l_get("apps.ir_remote.receiver_mode.scan_to_copy"),0,0,65535)
                tft.text(f8x8, l_get("apps.ir_remote.receiver_mode.timeout"),0,8,65535)
                ir_data = recv.record_ir(15000)
                if ir_data is not None and ir_data != []:
                    date = str(time.time())
                    filename = f"/usr/ir/{date}.ir"
                    with open(filename, 'w') as f:
                        json.dump(ir_data, f)
                    tft.text(f8x8, l_get("apps.ir_remote.receiver_mode.saved_as") + filename,0,16,65535)
                else:
                    tft.fill(0)
                    tft.text(f8x8, l_get("apps.ir_remote.receiver_mode.timeout_no_signal"), 0, 16, 63488)
                time.sleep(2)
                updat = True
            
        else:
            work = False
    ps.set_freq(osc.BASE_FREQ)