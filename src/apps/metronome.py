# Metronome app
# App ID: 1003

from machine import Pin, PWM
import time

import fonts.def_8x8 as f8x8
import fonts.def_16x32 as f16x32

import modules.buzzer as buzz
import modules.io_manager as io_man
import modules.os_constants as osc
import modules.printer as printer
import modules.menus as menus

button_a = io_man.get('button_a')
button_b = io_man.get('button_b')
button_c = io_man.get('button_c')
tft = io_man.get('tft')

def play(bpm):
    buzzer = PWM(Pin(2), duty_u16=0, freq=500)
    delay = ((60 / bpm) * 1000)
    tft.fill(0)
    tft.text(f16x32, "BPM: " + str(bpm),0,0,24552)
    tft.text(f8x8, "Press button A to exit!",0,127,65535)
    while button_a.value() == 1:
        time.sleep_ms(int(delay))
        buzz.play_sound_ms(buzzer, 400, 50)
        
    
def run():
    global button_c, button_a, button_b, tft
    button_a = io_man.get('button_a')
    button_b = io_man.get('button_b')
    button_c = io_man.get('button_c')
    tft = io_man.get('tft')
    
    if osc.HAS_BUZZER == False:
        menus.menu("You don't have buzzer!", [("OK", None)])
        return
    
    bpm_max = 250
    bpm_min = 30
    bpm = 120
    
    printer.log("Going into main loop")
    
    work = True
    while work == True:
        render = menus.menu("Metronome", [("BPM: "+ str(bpm), 0), ("+", 1), ("-", 2), ("+10", 3), ("-10", 4), ("Play", 5), ("Reset", 6), ("Close", 7)])
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