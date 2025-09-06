# NVS Set defaults script
# Sets default nvs vars

import modules.cache as cache
import modules.nvs as nvs

n_locks = cache.get_nvs('locks')
n_settings = cache.get_nvs('settings')
n_wifi = cache.get_nvs('wifi')

def ints(namespace, key, defvar, cachename):
    var = nvs.get_int(namespace, key)
    if var == None:
        nvs.set_int(namespace, key, defvar)
        var = defvar
    cache.set("n_cache_" + cachename, var)

def floats(namespace, key, defvar, cachename):
    var = nvs.get_float(namespace, key)
    if var == None:
        nvs.set_float(namespace, key, defvar)
        var = defvar
    cache.set("n_cache_" + cachename, var)
    
def strings(namespace, key, defvar, cachename):
    var = nvs.get_string(namespace, key)
    if var == None:
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
    
    # Metrics
    ints(n_settings, 'allow_metrics', 0, 'metrics')
    
    # Language settings
    strings(n_settings, 'lang', "en", 'lang')