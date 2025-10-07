"""
Helper for Stick firmware to set default vars in NVS
"""

import modules.cache as cache
import modules.nvs as nvs
import modules.os_constants as osc

n_locks = cache.get_nvs('locks')
n_settings = cache.get_nvs('settings')
n_wifi = cache.get_nvs('wifi')

def ints(namespace, key, defvar, cachename):
    var = nvs.get_int(namespace, key)
    if var is None:
        nvs.set_int(namespace, key, defvar)
        var = defvar
    cache.set("n_cache_" + cachename, var)

def floats(namespace, key, defvar, cachename):
    var = nvs.get_float(namespace, key)
    if var is None:
        nvs.set_float(namespace, key, defvar)
        var = defvar
    cache.set("n_cache_" + cachename, var)
    
def strings(namespace, key, defvar, cachename):
    var = nvs.get_string(namespace, key)
    if var is None:
        nvs.set_string(namespace, key, defvar)
        var = defvar
    cache.set("n_cache_" + cachename, var)

def run():

    # Dummy mode settings
    ints(n_locks, 'dummy', 0, 'dummy')

    # Backlight settings
    floats(n_settings, 'backlight', 0.5, 'backlight')

    # Buzz vol
    floats(n_settings, 'volume', 0.5, 'volume')
    
    # Wifi conf
    floats(n_wifi, 'conf', 0.0, 'conf')

    # Auto rotation
    ints(n_settings, 'autorotate', 1, 'arotate')

    # Pwr saving
    ints(n_settings, 'allowsaving', 1, 'pwrsave')
    ints(n_settings, 'shutdown_mode', osc.DEFAULT_SHUTDOWN_MODE, 'shtd_mode')
    
    # Metrics
    ints(n_settings, 'allow_metrics', 0, 'metrics')
    
    # Language settings
    strings(n_settings, 'lang', "en", 'lang')
    
    # Neopixel settings
    ints(n_settings, 'neo_anim_style', 1, 'neo_anim_style') # Default, static
    ints(n_settings, 'neo_enabled', 1, 'neo_enabled')
    ints(n_settings, 'neo_R', 64, 'neo_R') # Neopixel R led color
    ints(n_settings, 'neo_G', 64, 'neo_G') # Neopixel G led color
    ints(n_settings, 'neo_B', 64, 'neo_B') # Neopixel B led color
    
    # XP
    ints(n_settings, 'xp', 0, 'xp')
    ints(n_settings, "mood", 50, 'mood')
    
def set_hardware():
    import modules.buzzer as buzz
    import modules.io_manager as io_man
    import modules.printer as debug
    from modules.printer import Levels as log_levels
    
    tft = io_man.get('tft')
    s_bl = cache.get_and_remove('n_cache_backlight')
    debug.log("Backlight: " + str(s_bl), log_levels.DEBUG)
    tft.set_backlight(s_bl)

    s_vl = cache.get_and_remove('n_cache_volume')
    debug.log("Buzzer volume: " + str(s_vl), log_levels.DEBUG)
    buzz.set_volume(s_vl)