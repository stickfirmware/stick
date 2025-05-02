from machine import Pin
import machine
import modules.IR.db_nec as db_nec
import modules.IR.nec as nec
import modules.menus as menus
import fonts.def_8x8 as f8x8

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

ir_pin = machine.PWM(machine.Pin(19, machine.Pin.OUT), duty = 0)

def send(codes):
    tft.text(f8x8, "Sending...",0,0,65535)
    nec.send_array(codes)
    work = True
    while work == True:
        render = menus.menu("Repeat?", [("Yes", 1), ("No", 2)])
        if render == 1:
            tft.text(f8x8, "Sending...",0,0,65535)
            nec.send_array(codes)
        else:
            work = False

def run():
    work = True
    nec.set_ir(ir_pin)
    machine.freq(240000000)
    while work == True:
        render = menus.menu("IR Remote", [("ON/OFF", 1), ("VOL+", 2), ("VOL-", 3), ("Mute", 4), ("CHANNEL+", 5), ("CHANNEL-", 6), ("FREEZE", 7), ("Close", 8)])
        if render == 1:
            send(db_nec.power)
        elif render == 2:
            send(db_nec.vol_up)
        elif render == 3:
            send(db_nec.vol_down)
        elif render == 4:
            send(db_nec.mute)
        elif render == 5:
            send(db_nec.prog_up)
        elif render == 6:
            send(db_nec.prog_down)
        elif render == 7:
            send(db_nec.freeze)
        else:
            work = False
    machine.freq(80000000)