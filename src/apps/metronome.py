# Metronome app
# App ID: 1003

import fonts.def_8x8 as f8x8
import fonts.def_16x32 as f16x32

from machine import Pin, PWM
import modules.io_manager as io_man
import modules.osconstants as osc

button_a = io_man.get_btn_a()
button_b = io_man.get_btn_b()
button_c = io_man.get_btn_c()
tft = io_man.get_tft()

def play(bpm):
    import time
    print("Buzz tone")
    import modules.buzzer as buzz
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
    button_a = io_man.get_btn_a()
    button_b = io_man.get_btn_b()
    button_c = io_man.get_btn_c()
    tft = io_man.get_tft()
    
    import modules.menus as menus
    if osc.HAS_BUZZER == False:
        menus.menu("You don't have buzzer!", [("OK", None)])
        return
    import machine
    
    machine.freq(240000000)
    
    bpm_max = 250
    bpm_min = 30
    bpm = 120
    
    print("Going into main loop")
    
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