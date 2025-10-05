"""
RAM Cleaning helper for Stick firmware
"""

import gc
import sys

import modules.printer as printer

_WHITELIST = {
        'esp32',
        'network',
        'os',
        'neopixel',
        'bitmaps',
        'scripts',
        'asyncio',
        'machine',
        'scripts.checkbattery',
        'modules',
        'modules.battery_check',
        'modules.xp_leveling',
        'modules.button_combos',
        'modules.appboot',
        'modules.neopixels',
        'modules.neopixel_anims',
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
        'modules.console_colors',
        'modules.buzzer',
        'modules.nvs',
        'modules.cardputer_kb',
        'modules.powersaving',
        'modules.ram_cleaner',
        'modules.rtc',
        'modules.ntp',
        'modules.translate',
        'modules.mpu6886',
        'fonts.def_8x8',
        'fonts.def_16x16',
        'fonts.def_16x32',
        'fonts',
        'apps.clock',
        'modules.oobe',
        'apps',
        'mainos',
        'flashbdev',
    }
"""Module whitelist for main loop"""

def deep_clean_module(modname: str):
    """
    Cleans module from RAM
    
    Args:
        modname (str): Module name (in python format like: "modules.files")
    """
    mod = sys.modules.get(modname)
    if not mod:
        return
    for attr in dir(mod):
        try:
            setattr(mod, attr, None)
        except Exception:
            pass
    sys.modules.pop(modname, None)

def clean():
    """
    Cleans all modules that are not whitelisted from RAM
    """
    printer.log_cleaner("Ram cleaner started")
    before = gc.mem_free()

    current_keys = list(sys.modules.keys())
    for k in current_keys:
        if k not in _WHITELIST and not k.startswith("uasyncio"):
            printer.log_cleaner(str(k))
            deep_clean_module(k)

    gc.collect()
    after = gc.mem_free()
    freed = after - before

    printer.log_cleaner("Freed {} bytes of RAM".format(freed))
