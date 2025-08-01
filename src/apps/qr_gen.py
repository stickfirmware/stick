import time

import modules.numpad as numpad
import modules.qr_codes as qr
import modules.os_constants as osc
import modules.io_manager as io_man

import fonts.def_8x8 as f8x8

def run():
    inp = numpad.keyboard("QR Code text")
    work = True
    tft = io_man.get_tft()
    btn_b = io_man.get_btn_b()
    btn_a = io_man.get_btn_a()
    btn_c = io_man.get_btn_c()
    didnt_scale = True
    while work == True:
        if inp != None or inp != "":
            tft.fill(0)
            size = 1
            if didnt_scale == True:
                tft.text(f8x8, "Too small? Press btn b.", 0, 127)
            else:
                size = 3
            qr.make_qr(tft, inp, 0, 0, size)
            while btn_a.value() == 1 and btn_b.value() == 1 and btn_c.value() == 1:
                time.sleep(osc.LOOP_WAIT_TIME)
            if btn_b.value() == 1 or didnt_scale == False:
                work = False
            else:
                didnt_scale = False
            while btn_a.value() == 0 or btn_b.value() == 0 or btn_c.value() == 0:
                time.sleep(osc.DEBOUNCE_TIME)