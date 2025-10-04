"""
Stick firmware leveling service

Please don't abuse it, it's meant to be fun.
"""

# How to get xp?
# Boot system - 2 xp
# Open app - 5 xp
# Send IR signal - 3 xp

import time

import modules.nvs as nvs
import modules.cache as cache

_cooldown_timer = time.ticks_ms()
_mood_cooldown_timer = time.ticks_ms()
_COOLDOWN = 5000

_MAX_XP = 10000
_MAX_XP_PER_CALL = 10
_MAX_LEVEL = 20
_MAX_MOOD_PER_CALL = 2

n_settings = cache.get_nvs("settings")

def xp_progress(xp):
    """
    Get level for progress bar display
    
    Args:
        xp (int): Current XP
    
    Returns:
        level: Current level
        xp_in_level: XP Progress in current level
        xp_for_next_level: How much XP needed in current level to next level
        percent: Percent in float
    """
    
    # IDK Whats happening here
    ratio = xp / _MAX_XP
    float_level = ratio**0.5 * _MAX_LEVEL
    level = int(float_level)
    
    xp_start_ratio = (level / _MAX_LEVEL)**2
    xp_start = int(xp_start_ratio * _MAX_XP)
    
    next_level = min(level + 1, _MAX_LEVEL)
    xp_end_ratio = (next_level / _MAX_LEVEL)**2
    xp_end = int(xp_end_ratio * _MAX_XP)
    
    xp_in_level = xp - xp_start
    xp_for_next_level = xp_end - xp_start
    percent = xp_in_level / xp_for_next_level if xp_for_next_level else 1.0
    
    return level, xp_in_level, xp_for_next_level, percent

def get_xp():
    """
    Gets xp from Stick firmware leveling system
    
    Returns:
        int: XP from leveling system
    """
    
    return nvs.get_int(n_settings, "xp")

def add_xp(amount):
    """
    Adds xp to Stick firmware leveling system, cooldown 5s, max xp per call 10
    
    Args:
        amount (int): XP to add, max is 10
    """
    
    global _cooldown_timer
    amount = int(amount)
    
    if amount > _MAX_XP_PER_CALL:
        raise ValueError("XP amount too high!")
    
    if time.ticks_diff(time.ticks_ms(), _cooldown_timer) < _COOLDOWN:
        return
    
    _cooldown_timer = time.ticks_ms()
    
    curr_exp = nvs.get_int(n_settings, "xp")
    
    if (curr_exp + amount) > _MAX_XP:
        print("WARNING: Max XP reached!")
        return
    
    nvs.set_int(n_settings, "xp", curr_exp + amount)
    
def remove_mood(amount):
    """
    Remove mood from Stick firmware pet system, cooldown 5s, max mood per call 2
    
    Args:
        amount (int): Mood to remove, max is 2
    """
    
    global _mood_cooldown_timer
    amount = int(amount)
    
    if amount > _MAX_MOOD_PER_CALL:
        raise ValueError("Mood amount too high!")
    
    if time.ticks_diff(time.ticks_ms(), _mood_cooldown_timer) < _COOLDOWN:
        return
    
    _mood_cooldown_timer = time.ticks_ms()
    
    curr_mood = nvs.get_int(n_settings, "mood")
    
    if (curr_mood + amount) < 0:
        print("WARNING: Minimal mood reached!")
        return
    
    nvs.set_int(n_settings, "mood", curr_mood - amount)

def add_mood(amount):
    """
    Add mood to Stick firmware pet system, cooldown 5s, max mood per call 2
    
    Args:
        amount (int): Mood to add, max is 2
    """
    
    global _mood_cooldown_timer
    amount = int(amount)
    
    if amount > _MAX_MOOD_PER_CALL:
        raise ValueError("Mood amount too high!")
    
    if time.ticks_diff(time.ticks_ms(), _mood_cooldown_timer) < _COOLDOWN:
        return
    
    _mood_cooldown_timer = time.ticks_ms()
    
    curr_mood = nvs.get_int(n_settings, "mood")
    
    nvs.set_int(n_settings, "mood", curr_mood + amount)
    
def get_mood():
    """
    Gets mood from Stick firmware leveling system
    
    Returns:
        int: Mood from leveling system
    """
    
    return nvs.get_int(n_settings, "mood")