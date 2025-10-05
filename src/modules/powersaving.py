"""
Stick firmware power saving helper
"""

import time

import machine

import modules.battery_check as bcheck
import modules.os_constants as osc

cooldown = 50 # ms
last_clock_change = time.ticks_ms() # Just to not abuse the voltage regulator

allow_boosts = True

# Set boost state
def boost_allowing_state(allow: bool) -> bool:
    """
    Change clock boosting state

    Args:
        allow (bool): True if you want to allow clock boosting, False if no

    Returns:
        bool: Current state of allow_boosts
    """
    global allow_boosts
    allow_boosts = allow
    return allow_boosts

# Boost freq for some cpu intensive tasks, then make it normal for power saving
def boost_clock():
    """
    Boosts clock depending on battery and allow_boosts state
    """
    if allow_boosts:
        voltage = bcheck.voltage(2)
        if voltage >= 3.7:
            set_freq(osc.ULTRA_FREQ)
        else:
            set_freq(osc.FAST_FREQ)

# Set freq
def set_freq(freq: int):
    """
    Set MCU frequency in Hz

    Args:
        freq (int): MCU frequency in Hz

    Returns:
        bool: True if success, False if failed/cooldown
    """
    global last_clock_change
    now = time.ticks_ms()
    if time.ticks_diff(now, last_clock_change) >= cooldown and machine.freq() != freq:
        machine.freq(freq)
        last_clock_change = now

# Saver function for loops (Should be called every 1-2s to save power)
def loop():
    """
    Slow down MCU clock to save power, make sure to call it every 1-2s so it is not always highest one possible
    """
    if machine.freq() != osc.SLOW_FREQ:
        set_freq(osc.BASE_FREQ)