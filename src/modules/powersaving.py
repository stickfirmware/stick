import machine
import time

import modules.os_constants as osc

cooldown = 50 # ms
last_clock_change = time.ticks_ms() # Just to not abuse the voltage regulator

allow_boosts = True

# Set boost state
def boost_allowing_state(allow):
    global allow_boosts
    allow_boosts = allow
    return allow_boosts

# Boost freq for some cpu intensive tasks, then make it normal for power saving
def boost_clock():
    if allow_boosts == True:
        set_freq(osc.ULTRA_FREQ)

# Set freq
def set_freq(freq):
    global last_clock_change
    if time.ticks_diff(time.ticks_ms(), last_clock_change) >= cooldown and machine.freq() != freq:
        machine.freq(freq)
        last_clock_change = time.ticks_ms()

# Saver function for loops (Should be called every 1-2s to save power)
def loop():
    if machine.freq() != osc.SLOW_FREQ:
        set_freq(osc.BASE_FREQ)