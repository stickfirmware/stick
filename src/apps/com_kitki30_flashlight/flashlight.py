import time

import modules.io_manager as io_man
import modules.os_constants as osc
import modules.nvs as nvs
import modules.cache as cache

n_settings = cache.get_nvs('settings')

def run():
    button_a = io_man.get('button_a')
    button_b = io_man.get('button_b')
    button_c = io_man.get('button_c')
    tft = io_man.get('tft')
    
    tft.set_backlight(1.0)
    tft.fill(65535)
    
    if osc.HAS_NEOPIXEL:
        import modules.neopixel_anims as np_anims
        np_anims.static(255, 255, 255)
    
    while button_a.value() == 1 and button_b.value() == 1 and button_c.value() == 1:
        time.sleep(osc.DEBOUNCE_TIME)
    tft.set_backlight(nvs.get_float(n_settings, "backlight"))