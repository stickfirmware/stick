_CACHE = {}

def get(name):
    return _CACHE.get(name)

def set(name, value):
    _CACHE[name] = value

def clear(bypass_precache=False):
    _CACHE.clear()
    if bypass_precache == False:
        precache()

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