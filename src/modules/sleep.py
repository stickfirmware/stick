import esp32
import machine
import time

import modules.nvs as nvs
import modules.os_constants as osc
import modules.io_manager as io_man

def sleep(verbose=False):
    button_c = io_man.get('button_c')
    tft = io_man.get('tft')
    def log(msg):
        if verbose == True:
            print("[SLEEP]" + msg)
    n_settings = esp32.NVS("settings")
    log("Sleeping")
    log("Set wake on ext0")
    if osc.INPUT_METHOD == 1:
        esp32.wake_on_ext0(pin = button_c, level = esp32.WAKEUP_ALL_LOW)
    elif osc.INPUT_METHOD == 2:
        esp32.wake_on_ext0(pin = machine.Pin(0,machine.Pin.IN, machine.Pin.PULL_UP), level = esp32.WAKEUP_ALL_LOW)
    log("Turn off backlight")
    tft.set_backlight(0)
    log("Clear display")
    tft.fill(0)
    log("Put st7789 to sleep")
    tft.sleep_mode(True)
    log("Going to lightsleep, Bye!")
    machine.lightsleep()
    log("Woken up from light sleep, Hi!")
    log("Setting backlight to previous level")
    s_bl = nvs.get_float(n_settings, "backlight")
    del n_settings
    tft.set_backlight(s_bl)
    log("Turning st7789 back from sleep")
    tft.sleep_mode(False)
    log("Waiting (st7789 needs some time before drawing after sleep)")
    time.sleep(0.3)