# SHHHH! SUPER SECRET THINGS HERE! I'M WARNING YOU!

import time

import modules.io_manager as io_man
import modules.crash_handler as c_handler
import modules.os_constants as osc

import fonts.def_16x32 as f16x32
import fonts.def_8x8 as f8x8

def trigger(code):
    tft = io_man.get('tft')
    button_b = io_man.get('button_b')
    button_c = io_man.get('button_c')
    clicker = io_man.get('clicker_btn')

    # Button holder
    if code == 1:
        tft.fill(0)
        tft.text(f8x8, "WHY?", 0,0,65535)
        time.sleep(0.5)
        tft.text(f8x8, "WHY?", 40,0,65535)
        time.sleep(0.5)
        tft.text(f8x8, "RELEASE TEH BUTTON!", 80,0,65535)
        time.sleep(0.5)
        tft.text(f16x32, "N", 0,8,63552)
        time.sleep(0.5)
        tft.text(f16x32, "O", 16,8,63552)
        time.sleep(0.5)
        tft.text(f16x32, "W", 32,8,63552)
        time.sleep(0.5)
        tft.text(f16x32, "!", 48,8,63552)
        time.sleep(0.1)
        tft.text(f16x32, "!", 64,8,63552)
        time.sleep(0.1)
        tft.text(f16x32, "!", 72,8,63552)
        time.sleep(0.5)
        if button_b.value() == 0:
            c_handler.crash_screen(tft, 2, "YOU WANTED IT!!!\nLeave teh button alone, please, I'm begging you!", True, True, 1)
    # Clicker
    elif code == 2 and clicker is not None:
        tft.fill(0)
        work = True
        update_counter = True
        clicks = 0
        while work:
            time.sleep(osc.LOOP_WAIT_TIME)
            if update_counter:
                update_counter = False
                tft.text(f16x32, str(clicks), 0,0,63552)
            if clicker.value() == 0:
                update_counter = True
                clicks += 1
                while clicker.value() == 0:
                    time.sleep(osc.DEBOUNCE_TIME)
            if button_c.value() == 0:
                work = False
                while button_c.value() == 0:
                    time.sleep(osc.DEBOUNCE_TIME)

