# Buzzer script

import time
import asyncio

import modules.os_constants as osc

duty = 0.5

def set_volume(volume):
    global duty
    if volume >= 1:
        duty = 1
    else:
        duty = volume

def play_sound(buzzer, freq, duration):
    if osc.HAS_BUZZER:
        buzzer.duty_u16(int(65536*duty))
        buzzer.freq(freq)
        time.sleep(duration)
        buzzer.duty_u16(int(65536*0))
    
def play_sound_ms(buzzer, freq, duration):
    play_sound(buzzer, freq, (duration / 1000))
    
async def play_sound_async(buzzer, freq, duration):
    if osc.HAS_BUZZER:
        buzzer.duty_u16(int(65536*duty))
        buzzer.freq(freq)
        await asyncio.sleep(duration)
        buzzer.duty_u16(int(65536*0))
    
async def play_sound_ms_async(buzzer, freq, duration):
    await play_sound(buzzer, freq, (duration / 1000))
    
def startup_sound(buzzer):
    sounds = [440, 494, 523, 494, 523, 494, 523, 587, 659]
    for freq in sounds:
        play_sound(buzzer, freq, 0.1)