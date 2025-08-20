import time

import modules.io_manager as io_man
import modules.os_constants as osc

import fonts.def_16x16 as f16x16
import fonts.def_8x8 as f8x8

def run():
    tft = io_man.get("tft")
    
    tft.fill(0)
    tft.text(f16x16, "Kitki30 Account", 0, 0, 65535)
    tft.text(f8x8, "Sign in to unlock:", 0, 16, 65535)
    tft.text(f8x8, "- Find My Stick", 0, 24, 65535)
    tft.text(f8x8, "- Simple games (Wordly)", 0, 32, 65535)
    tft.text(f8x8, "Completely free,", 0, 40, 65535)
    tft.text(f8x8, "with no data selling.", 0, 48, 65535)
    tft.text(f8x8, "To register or sign in:", 0, 56, 65535)
    tft.text(f8x8, "Press button B (Tab)", 0, 64, 65535)
    tft.text(f8x8, "Then connect to Wi-Fi", 0, 72, 65535)
    tft.text(f8x8, "And go to Account > Link", 0, 80, 65535)
    tft.text(f8x8, "To skip:", 0, 119, 65535)
    tft.text(f8x8, "Press button A (Enter)", 0, 127, 65535)
    
    button_a = io_man.get("button_a")
    button_b = io_man.get("button_b")
    
    while button_a.value() == 1 and button_b.value() == 1:
        time.sleep(osc.LOOP_WAIT_TIME)
        
    if button_b.value() == 0:
        import apps.settings
        apps.settings.run()