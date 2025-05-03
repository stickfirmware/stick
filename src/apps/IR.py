from machine import Pin
import machine
import modules.IR.db_nec as db_nec
import modules.IR.db_sony as db_sony
import modules.IR.db_panasonic as db_pana
import modules.IR.nec as nec
import modules.IR.sony as sony
import modules.IR.panasonic as pana
import modules.menus as menus
import fonts.def_8x8 as f8x8
import modules.nvs as nvs
import esp32

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

def send(necc, sonyc, panac):
    tft.text(f8x8, "Sending nec...",0,0,65535)
    nec.send_array(necc)
    tft.text(f8x8, "Sending sony...",0,8,65535)
    sony.send_array(sonyc)
    tft.text(f8x8, "Sending panasonic...",0,16,65535)
    sony.send_array(panac)
    work = True
    while work == True:
        render = menus.menu("Repeat?", [("Yes", 1), ("No", 2)])
        if render == 1:
            tft.text(f8x8, "Sending nec...",0,0,65535)
            nec.send_array(necc)
            tft.text(f8x8, "Sending sony...",0,8,65535)
            sony.send_array(sonyc)
            tft.text(f8x8, "Sending panasonic...",0,16,65535)
            sony.send_array(panac)
        else:
            work = False

def run():
    global ir_pin
    work = True
    nec.set_ir(ir_pin)
    sony.set_ir(ir_pin)
    machine.freq(240000000)
    while work == True:
        render = menus.menu("IR Remote", [("ON/OFF", 1), ("VOL+", 2), ("VOL-", 3), ("Mute", 4), ("CHANNEL+ / NEXT", 5), ("CHANNEL- / PREV", 6), ("FREEZE", 7), ("Change IR pin", 8), ("Close", 9)])
        if render == 1:
            send(db_nec.power, db_sony.power, db_pana.power)
        elif render == 2:
            send(db_nec.vol_up, db_sony.vol_up, db_pana.vol_up)
        elif render == 3:
            send(db_nec.vol_down, db_sony.vol_down, db_pana.vol_down)
        elif render == 4:
            send(db_nec.mute, db_sony.mute, db_pana.mute)
        elif render == 5:
            send(db_nec.prog_up, db_sony.prog_up, db_pana.prog_up)
        elif render == 6:
            send(db_nec.prog_down, db_sony.prog_down, db_pana.prog_down)
        elif render == 7:
            send(db_nec.freeze, db_sony.freeze, db_pana.freeze)
        elif render == 8:
            render = menus.menu("Change IR pin", [("GPIO19 (Default)", 19), ("GPIO26", 26), ("GPIO25/36", 25), ("GPIO0", 0), ("Cancel", 99)])
            if render != 99:
                nvs.set_int(n_settings, "irPin", render)
            ir_pin = machine.PWM(machine.Pin(nvs.get_int(n_settings, "irPin"), machine.Pin.OUT), duty = 0)
        else:
            work = False
    machine.freq(80000000)