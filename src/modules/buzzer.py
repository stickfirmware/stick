# Buzzer script

import time

duty = 0.5

def set_volume(volume):
    global duty
    duty = volume

def play_sound(buzzer, freq, duration):
    buzzer.duty_u16(int(65536*duty))
    buzzer.freq(freq)
    time.sleep(duration)
    buzzer.duty_u16(int(65536*0))
    
def play_sound_ms(buzzer, freq, duration):
    play_sound(buzzer, freq, (duration / 1000))
    
def startup_sound(buzzer):
    play_sound(buzzer, 440, 0.1)
    play_sound(buzzer, 494, 0.1)
    play_sound(buzzer, 523, 0.1)
    play_sound(buzzer, 494, 0.1)
    play_sound(buzzer, 523, 0.1)
    play_sound(buzzer, 587, 0.1)
    play_sound(buzzer, 659, 0.1)