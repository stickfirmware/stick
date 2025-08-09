import random
import time

import fonts.def_16x32 as f16x32
import fonts.def_8x8 as f8x8

import modules.os_constants as osc
import modules.st7789 as st
import modules.text_utils as text_utils
import modules.io_manager as io_man

def random_int(tft):
    random.seed(None)
    text = str(random.randint(1,6))
    x = text_utils.center_x(text, 16)
    y = text_utils.center_y(text, 32)
    tft.text(f16x32, text, x, y, st.WHITE)

def run():
    tft = io_man.get('tft')
    button_a = io_man.get('button_a')
    button_c = io_man.get('button_c')

    tft.fill(0)
    tft.text(f8x8, "Roll again? Press btn A", 0, 0, st.WHITE)

    random_int(tft)

    while True:
        if button_c.value() == 0:
            break
        if button_a.value() == 0:
            while button_a.value() == 0:
                time.sleep(osc.DEBOUNCE_TIME)
            random_int(tft)
            
        time.sleep(osc.LOOP_WAIT_TIME)