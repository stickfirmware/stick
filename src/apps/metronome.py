# Metronome app
# App ID: 1003

from machine import Pin, PWM
import time

import fonts.def_8x8 as f8x8
import fonts.def_16x32 as f16x32

import modules.buzzer as buzz
import modules.io_manager as io_man
import modules.printer as printer
import modules.menus as menus
from modules.translate import get as l_get

button_a = io_man.get('button_a')
button_b = io_man.get('button_b')
button_c = io_man.get('button_c')
tft = None

def play(bpm):
    buzzer = PWM(Pin(2), duty_u16=0, freq=500)
    delay = ((60 / bpm) * 1000)
    tft.fill(0)
    tft.text(f16x32, "BPM: " + str(bpm),0,0,24552)
    tft.text(f8x8, l_get("apps.metronome.press_a_to_exit"),0,127,65535)
    while button_a.value() == 1:
        time.sleep_ms(int(delay))
        buzz.play_sound_ms(buzzer, 400, 50)
        
    
def run():
    global button_c, button_a, button_b, tft
    button_a = io_man.get('button_a')
    button_b = io_man.get('button_b')
    button_c = io_man.get('button_c')
    tft = io_man.get('tft')
    
    bpm_max = 250
    bpm_min = 30
    bpm = 120
    
    printer.log("Going into main loop")
    
    work = True
    while work == True:
        render = menus.menu(l_get("apps.metronome.name"),
                            [("BPM: "+ str(bpm), 0), 
                             ("+", 1),
                             ("-", 2),
                             ("+10", 3),
                             ("-10", 4),
                             (l_get("apps.metronome.play"), 5),
                             (l_get("menus.menu_reset"), 6),
                             (l_get("menus.menu_close"), 7)])
        if render == 1:
            bp_temp = bpm + 1
            if bp_temp <= bpm_max:
                bpm += 1
        elif render == 2:
            bp_temp = bpm - 1
            if bp_temp >= bpm_min:
                bpm -= 1
        elif render == 3:
            bp_temp = bpm + 10
            if bp_temp <= bpm_max:
                bpm += 10
        elif render == 4:
            bp_temp = bpm - 10
            if bp_temp >= bpm_min:
                bpm -= 10
        elif render == 5:
            play(bpm)
        elif render == 6:
            bpm = 120
        elif render == None or render == 7:
            work = False