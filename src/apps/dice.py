import random
import time

import fonts.def_16x32 as f16x32
import fonts.def_8x8 as f8x8

import modules.os_constants as osc
from modules.translate import get as l_get
import modules.text_utils as text_utils
import modules.io_manager as io_man
import modules.cache as cache
import modules.seed_random as s_random

def random_int(tft):
    text = str(random.randint(1,6))
    x = text_utils.center_x(text, 16)
    y = text_utils.center_y(32)
    tft.text(f16x32, text, x, y, random.randint(60000, 65535))

def run():
    tft = io_man.get('tft')
    button_a = io_man.get('button_a')
    button_c = io_man.get('button_c')
    
    if not cache.get('random_seeded'):
        s_random.seed()

    tft.fill(0)
    tft.text(f8x8, l_get("apps.dice.roll_again"), 0, 0, 65535)

    random_int(tft)

    while True:
        if button_c.value() == 0:
            break
        if button_a.value() == 0:
            while button_a.value() == 0:
                time.sleep(osc.DEBOUNCE_TIME)
            random_int(tft)
            
        time.sleep(osc.LOOP_WAIT_TIME)