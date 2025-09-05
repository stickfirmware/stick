_CACHE = {}

def get(name):
    return _CACHE.get(name)

def set(name, value):
    _CACHE[name] = value

def clear(bypass_precache=False):
    _CACHE.clear()
    if bypass_precache == False:
        precache()

def remove(name):
    if name in _CACHE:
        del _CACHE[name]

def get_and_remove(name):
    val = get(name)
    remove(name)
    return val

def get_nvs(name):
    key = "nvs_" + name
    nvs_obj = _CACHE.get(key)
    if nvs_obj is None:
        import esp32
        nvs_obj = esp32.NVS(name)
        _CACHE[key] = nvs_obj
    return nvs_obj

def update_last_mod():
    import time
    
    curr_ticks = time.ticks_ms()
    set("app_config_last_modify", curr_ticks)
    return curr_ticks
    

def reload_apps():
    import time
    
    import apps.oobe as oobe
    
    set("app_config", oobe.read_config(True))
    set("app_config_last_modify", time.ticks_ms())

def precache():
    import modules.random_func_checker as rand_func_check
    set("rand_extra_func", rand_func_check.check_random_extra_functions())

    import version
    v_major = version.MAJOR
    v_minor = version.MINOR
    v_patch = version.PATCH
    v_beta = version.is_beta
    v_disp = "v" + str(v_major) + "." + str(v_minor) + "." + str(v_patch)
    
    set("ver_displayname", v_disp)
    set("ver_major", v_major)
    set("ver_minor", v_minor)
    set("ver_patch", v_patch)
    set("ver_isbeta", v_beta)

    get_nvs('settings')
    get_nvs('boot')
    get_nvs('wifi')
    get_nvs('locks')
    get_nvs('guides')
    
    reload_apps()