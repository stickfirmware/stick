from machine import Pin
import machine
import time
import os
import json

import modules.io_manager as io_man
import modules.printer as printer
import modules.os_constants as osc
import modules.IR.db_nec as db_nec
import modules.IR.db_sony as db_sony
import modules.IR.db_panasonic as db_pana
import modules.IR.db_samsung as db_samsa
import modules.IR.db_gc as db_gc
import modules.IR.nec as nec
import modules.IR.sony as sony
import modules.IR.panasonic as pana
import modules.IR.samsung as samsa
import modules.IR.gc_send as gc_send
import modules.IR.recv as recv
import modules.menus as menus
import fonts.def_8x8 as f8x8
import modules.nvs as nvs
import modules.powersaving as ps
import modules.cache as cache
from modules.translate import get as l_get

button_a = io_man.get('button_a')
button_b = io_man.get('button_b')
button_c = io_man.get('button_c')
tft = io_man.get('tft')

n_settings = cache.get_nvs('settings')
pin_nvs = nvs.get_int(n_settings, "irPin")
if pin_nvs is None or pin_nvs not in osc.IR_ALLOWED_PINS:
    nvs.set_int(n_settings, "irPin", osc.IR_PIN)
    pin_nvs = osc.IR_PIN
printer.log("IR pin from NVS:" + repr(pin_nvs))
ir_pin = machine.PWM(machine.Pin(pin_nvs, machine.Pin.OUT), duty=0)
io_man.set('IR', ir_pin)

def send(necc, sonyc, panac, samsac, gcc):
    ps.boost_freq()
    sending_text = l_get("apps.ir_remote.sending")
    tft.text(f8x8, f"{sending_text} nec...",0,0,65535)
    nec.send_array(necc)
    time.sleep(osc.IR_SENDING_WAIT_TIME)
    tft.text(f8x8, f"{sending_text} sony...",0,8,65535)
    sony.send_array(sonyc)
    time.sleep(osc.IR_SENDING_WAIT_TIME)
    tft.text(f8x8, f"{sending_text} samsung...",0,16,65535)
    samsa.send_array(samsac)
    time.sleep(osc.IR_SENDING_WAIT_TIME)
    tft.text(f8x8, f"{sending_text} panasonic...",0,24,65535)
    pana.send_array(panac)
    time.sleep(osc.IR_SENDING_WAIT_TIME)
    tft.text(f8x8, f"{sending_text} GC...",0,32,65535)
    gc_send.send_array(gcc)
    render = menus.menu(l_get("apps.ir_remote.menu.repeat"), [(l_get("menus.yes"), 1), (l_get("menus.no"), 2)])
    ps.set_freq(osc.BASE_FREQ)
    if render == 1:
        send(necc, sonyc, panac, samsac, gcc)
    else:
        work = False

def run():
    global button_c, button_a, button_b, tft
    button_a = io_man.get('button_a')
    button_b = io_man.get('button_b')
    button_c = io_man.get('button_c')
    tft = io_man.get('tft')
    ps.set_freq(osc.BASE_FREQ)
    global ir_pin
    work = True
    while work == True:
        render = menus.menu(l_get("apps.ir_remote.name"), 
                            [(l_get("apps.ir_remote.buttons.power"), 1),
                             (l_get("apps.ir_remote.buttons.vol_up"), 2),
                             (l_get("apps.ir_remote.buttons.vol_down"), 3),
                             (l_get("apps.ir_remote.buttons.mute"), 4),
                             (l_get("apps.ir_remote.buttons.chan_next"), 5),
                             (l_get("apps.ir_remote.buttons.chan_prev"), 6),
                             (l_get("apps.ir_remote.buttons.freeze"), 7),
                             (l_get("apps.ir_remote.menu.change_pin"), 8),
                             (l_get("apps.ir_remote.menu.receive"), 9),
                             (l_get("menus.menu_close"), 10)])
        if render == 1:
            send(db_nec.power, db_sony.power, db_pana.power, db_samsa.power, db_gc.power)
        elif render == 2:
            send(db_nec.vol_up, db_sony.vol_up, db_pana.vol_up, db_samsa.vol_up, db_gc.vol_up)
        elif render == 3:
            send(db_nec.vol_down, db_sony.vol_down, db_pana.vol_down, db_samsa.vol_down, db_gc.vol_down)
        elif render == 4:
            send(db_nec.mute, db_sony.mute, db_pana.mute, db_samsa.mute, db_gc.mute)
        elif render == 5:
            send(db_nec.prog_up, db_sony.prog_up, db_pana.prog_up, db_samsa.prog_up, db_gc.prog_up)
        elif render == 6:
            send(db_nec.prog_down, db_sony.prog_down, db_pana.prog_down, db_samsa.prog_down, db_gc.prog_down)
        elif render == 7:
            send(db_nec.freeze, db_sony.freeze, db_pana.freeze, db_samsa.freeze, db_gc.freeze)
        # Change pin
        elif render == 8:
            render_pins = []
            for pin in osc.IR_ALLOWED_PINS:
                render_pins.append(("GPIO"+str(pin), pin))
            render = menus.menu(l_get("apps.ir_remote.menu.change_pin"), render_pins)
            if render != 99 and render != None:
                nvs.set_int(n_settings, "irPin", render)
            ir_pin = machine.PWM(machine.Pin(nvs.get_int(n_settings, "irPin"), machine.Pin.OUT), duty = 0)
            io_man.set('IR', ir_pin)
        elif render == 9:
            if osc.ALLOW_IR_RECORD == False:
                menus.menu(l_get("apps.ir_remote.menu.receive_no_support"), [(l_get("menus.menu_close"), 1)])
                continue
            works = True
            updat = True
            if "usr" not in os.listdir("/"):
                os.mkdir("/usr")
            if "ir" not in os.listdir("/usr/"):
                os.mkdir("/usr/ir")
            while works == True:
                time.sleep(osc.LOOP_WAIT_TIME)
                if updat == True:
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