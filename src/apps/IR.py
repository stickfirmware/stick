from machine import Pin
import machine
import time
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
import esp32
import os
import json

button_a = None
button_b = None
button_c = None
tft = None

def set_btf(bta, btb, btc, ttft):
    global button_a
    global button_b
    global button_c
    global tft
    
    button_a = bta
    button_b = btb
    button_c = btc
    tft = ttft

n_settings = esp32.NVS("settings")
if nvs.get_int(n_settings, "irPin") == None:
    nvs.set_int(n_settings, "irPin", 19)
ir_pin = machine.PWM(machine.Pin(nvs.get_int(n_settings, "irPin"), machine.Pin.OUT), duty = 0)

def send(necc, sonyc, panac, samsac, gcc):
    tft.text(f8x8, "Sending nec...",0,0,65535)
    nec.send_array(necc)
    time.sleep(0.1)
    tft.text(f8x8, "Sending sony...",0,8,65535)
    sony.send_array(sonyc)
    time.sleep(0.1)
    tft.text(f8x8, "Sending samsung...",0,16,65535)
    samsa.send_array(samsac)
    time.sleep(0.1)
    tft.text(f8x8, "Sending panasonic...",0,24,65535)
    pana.send_array(panac)
    time.sleep(0.1)
    tft.text(f8x8, "Sending GC...",0,32,65535)
    gc_send.send_array(gcc)
    work = True
    while work == True:
        render = menus.menu("Repeat?", [("Yes", 1), ("No", 2)])
        if render == 1:
            tft.text(f8x8, "Sending nec...",0,0,65535)
            nec.send_array(necc)
            time.sleep(0.3)
            tft.text(f8x8, "Sending sony...",0,8,65535)
            sony.send_array(sonyc)
            time.sleep(0.3)
            tft.text(f8x8, "Sending samsung...",0,16,65535)
            samsa.send_array(samsac)
            time.sleep(0.3)
            tft.text(f8x8, "Sending panasonic...",0,24,65535)
            pana.send_array(panac)
            time.sleep(0.1)
            tft.text(f8x8, "Sending GC...",0,32,65535)
            gc_send.send_array(gcc)
        else:
            work = False

def run():
    global ir_pin
    work = True
    nec.set_ir(ir_pin)
    sony.set_ir(ir_pin)
    pana.set_ir(ir_pin)
    samsa.set_ir(ir_pin)
    gc_send.set_ir(ir_pin)
    machine.freq(240000000)
    while work == True:
        render = menus.menu("IR Remote", [("Devices menu", 0), ("ON/OFF", 1), ("VOL+", 2), ("VOL-", 3), ("Mute", 4), ("CHANNEL+ / NEXT", 5), ("CHANNEL- / PREV", 6), ("FREEZE", 7), ("Change IR pin", 8), ("Receive", 9), ("Close", 10)])
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
        elif render == 8:
            render = menus.menu("Change IR pin", [("GPIO19 (Default)", 19), ("GPIO26", 26), ("GPIO0", 0), ("GPIO32", 32), ("GPIO33", 33), ("Cancel", 99)])
            if render != 99 and render != None:
                nvs.set_int(n_settings, "irPin", render)
            ir_pin = machine.PWM(machine.Pin(nvs.get_int(n_settings, "irPin"), machine.Pin.OUT), duty = 0)
        elif render == 9:
            works = True
            updat = True
            if "usr" not in os.listdir("/"):
                os.mkdir("/usr")
            if "ir" not in os.listdir("/usr/"):
                os.mkdir("/usr/ir")
            while works == True:
                time.sleep(0.02)
                if updat == True:
                    tft.fill(0)
                    tft.text(f8x8, "Receiver mode!",0,0,65535)
                    tft.text(f8x8, "Receiver pinout:",0,10,65535)
                    tft.text(f8x8, "GND - Recv GND / -",0,18,54937)
                    tft.text(f8x8, "3v3 (Or 5v if supported) - VCC",0,26,63648)
                    tft.text(f8x8, "G26 - OUT / S",0,34,65535)
                    tft.text(f8x8, "Everything is saved to /usr/ir",0,48,65535)
                    tft.text(f8x8, "Press button A to continue,",0,56,65535)
                    tft.text(f8x8, "button C to exit!",0,64,65535)
                    updat = False
                if button_c.value() == 0:
                    works = False
                    continue
                if button_a.value() == 1:
                    continue
                tft.fill(0)
                tft.text(f8x8, "Scan IR to copy!",0,0,65535)
                tft.text(f8x8, "Timeout: 15s",0,8,65535)
                ir_data = recv.record_ir(15000)
                if ir_data is not None and ir_data != []:
                    date = str(time.time())
                    filename = f"/usr/ir/{date}.ir"
                    with open(filename, 'w') as f:
                        json.dump(ir_data, f)
                    tft.text(f8x8, "Saved as: " + filename,0,16,65535)
                else:
                    tft.fill(0)
                    tft.text(f8x8, "Timeout. No signal.", 0, 16, 63488)
                time.sleep(2)
                updat = True
            
        else:
            work = False
    machine.freq(80000000)