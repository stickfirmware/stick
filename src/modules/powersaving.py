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
performance_mode = False

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

# Toggle performance mode
def toggle_performance():
    global performance_mode
    if performance_mode:
        performance_mode = False
    else:
        performance_mode = True
    return performance_mode

# Boost freq for some cpu intensive tasks, then make it normal for power saving
def boost_clock():
    """
    Boosts clock depending on battery and allow_boosts state
    """
    if performance_mode:
        set_freq(osc.ULTRA_FREQ)
        return
    if allow_boosts:
        voltage = bcheck.voltage(2)  # Use lower sample mode to prevent lag
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

    Note:
        Performance mode will still keep clock at ULTRA_FREQ
    """
    global performance_mode
    if performance_mode:
        voltage = bcheck.voltage(2) # Use lower sample mode to prevent lag
        if voltage <= 3.7: # Auto disable performance mode on low battery
            performance_mode = False
        else:
            set_freq(osc.ULTRA_FREQ)
            return
    if machine.freq() != osc.SLOW_FREQ:
        set_freq(osc.BASE_FREQ)
        return