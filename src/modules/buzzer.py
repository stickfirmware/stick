# Buzzer script

import time

duty = 0.5

def set_volume(volume):
    duty = volume

def play_sound(buzzer, freq, duration):
    buzzer.duty_u16(int(65536*duty))
    buzzer.freq(freq)
    time.sleep(duration)
    buzzer.duty_u16(int(65536*0))