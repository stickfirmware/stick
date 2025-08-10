_CACHE = {}

def get(name):
    return _CACHE.get(name)

def set(name, value):
    _CACHE[name] = value

def clear(bypass_precache=False):
    _CACHE.clear()
    if bypass_precache == False:
        precache()

def get_nvs(name):
    key = "nvs_" + name
    nvs_obj = _CACHE.get(key)
    if nvs_obj is None:
        import esp32
        nvs_obj = esp32.NVS(name)
        _CACHE[key] = nvs_obj
    return nvs_obj

def precache():
    import modules.random_func_checker as rand_func_check
    set("rand_extra_func", rand_func_check.check_random_extra_functions())

    import version
    v_major = version.MAJOR
    v_minor = version.MINOR
    v_patch = version.PATCH
    v_disp = "v" + str(v_major) + "." + str(v_minor) + "." + str(v_patch)
    set("ver_displayname", v_disp)
    set("ver_major", v_major)
    set("ver_minor", v_minor)
    set("ver_patch", v_patch)

    get_nvs('settings')
    get_nvs('boot')
    get_nvs('wifi')
    get_nvs('locks')
    get_nvs('guides')