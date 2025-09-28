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
_COOLDOWN = 5000

_MAX_XP = 10000
_MAX_XP_PER_CALL = 10
_MAX_LEVEL = 20

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
    # Normalizacja do 0..1
    ratio = xp / _MAX_XP
    # Obliczamy "realny" poziom w float
    float_level = ratio**0.5 * _MAX_LEVEL
    level = int(float_level)
    
    # XP start dla tego levelu
    xp_start_ratio = (level / _MAX_LEVEL)**2
    xp_start = int(xp_start_ratio * _MAX_XP)
    
    # XP next level
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