import sys
import gc

import modules.printer as printer

_WHITELIST = {
        'esp32',
        'network',
        'os',
        'bitmaps',
        'scripts',
        'scripts.checkbattery',
        'modules',
        'modules.battery_check',
        'modules.cache',
        'modules.wifi_master',
        'modules.sdcard',
        'modules.menus',
        'modules.popup',
        'modules.os_constants',
        'modules.io_manager',
        'modules.st7789',
        'modules.json',
        'modules.decache',
        'modules.crash_handler',
        'modules.text_utils',
        'modules.button_init',
        'modules.error_db',
        'modules.printer',
        'modules.buzzer',
        'modules.nvs',
        'modules.cardputer_kb',
        'modules.powersaving',
        'modules.ram_cleaner',
        'modules.rtc',
        'modules.ntp',
        'modules.mpu6886',
        'fonts.def_8x8',
        'fonts.def_16x16',
        'fonts.def_16x32',
        'fonts',
        'apps.clock',
        'apps',
        'mainos',
        'flashbdev',
    }

def deep_clean_module(modname):
    mod = sys.modules.get(modname)
    if not mod:
        return
    for attr in dir(mod):
        try:
            setattr(mod, attr, None)
        except:
            pass
    sys.modules.pop(modname, None)

def clean():
    printer.log("Ram cleaner started")
    before = gc.mem_free()

    current_keys = list(sys.modules.keys())
    for k in current_keys:
        if k not in _WHITELIST and not k.startswith("uasyncio"):
            printer.log(str(k))
            deep_clean_module(k)

    gc.collect()
    after = gc.mem_free()
    freed = after - before

    printer.log("Freed {} bytes of RAM".format(freed))
