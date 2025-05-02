import esp32
import machine
import modules.nvs as nvs
import time

def sleep(tft, button_c, verbose=False):
    def log(msg):
        if verbose == True:
            print("[SLEEP]" + msg)
    n_settings = esp32.NVS("settings")
    log("Sleeping")
    log("Set wake on ext0")
    esp32.wake_on_ext0(pin = button_c, level = esp32.WAKEUP_ALL_LOW)
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