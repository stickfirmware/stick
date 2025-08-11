import time

import modules.numpad as numpad
import modules.qr_codes as qr
import modules.os_constants as osc
import modules.io_manager as io_man
import modules.menus as menus

def run():
    inp = None
    work = True
    tft = io_man.get('tft')
    btn_b = io_man.get('button_b')
    btn_a = io_man.get('button_a')
    btn_c = io_man.get('button_c')
    allow_input = True
    size = 1

    while work == True:
        if inp != None and inp != "":
            # Render qr
            qr.make_qr(tft, inp, 0, 0, size, True)

            while btn_a.value() == 1 and btn_b.value() == 1 and btn_c.value() == 1:
                time.sleep(osc.LOOP_WAIT_TIME)

            if btn_a.value() == 0:
                menu = menus.menu("QR Menu", [("Size", 1), ("Change input", 2), ("Exit", 3)])
                if menu == 2:
                    inp = None
                    allow_input = True
                elif menu == 1:
                    qr_size_menu = menus.menu("Size menu", [("Size +1", 1), ("Size -1", 2), ("Exit", 3)])
                    if qr_size_menu == 1:
                        size += 1
                    elif qr_size_menu == 2:
                        size -= 1
                else:
                    work = False
        else:
            if allow_input == True:
                inp = numpad.keyboard("QR Code text")
                allow_input = False
                size = 1
            else:
                work = False