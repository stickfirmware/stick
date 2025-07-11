def init_tft():
    import modules.st7789 as st7789
    from machine import PWM, Pin, SPI
    try:
        tft = st7789.ST7789(
            SPI(1, baudrate=31250000, sck=Pin(13), mosi=Pin(15), miso=None),
            135,
            240,
            reset=Pin(12, Pin.OUT),
            cs=Pin(5, Pin.OUT),
            dc=Pin(14, Pin.OUT),
            backlight=PWM(Pin(27), freq=1000),
            rotation=3) 
        tft.fill(0)
        return tft
    except Exception as e:
        return None
    
tft = init_tft()
from machine import Pin
button_a = Pin(37, Pin.IN, Pin.PULL_UP)
button_b = Pin(39, Pin.IN, Pin.PULL_UP)
button_c = Pin(35, Pin.IN, Pin.PULL_UP)

import machine
import modules.menus as menus
menus.set_btf(button_a, button_b, button_c, tft)

def reset_nvs():
    import esp32
    import modules.nvs as nvs
    n_settings = esp32.NVS("settings")
    n_wifi = esp32.NVS("wifi")
    n_boot = esp32.NVS("boot")
    n_crash = esp32.NVS("crash")
    nvs.set_float(n_settings, "volume", 0.5)
    nvs.set_float(n_settings, "backlight", 0.5)
    nvs.set_float(n_wifi, "conf", 0)
    nvs.set_int(n_wifi, "autoConnect", 0)
    nvs.set_string(n_wifi, "ssid", "")
    nvs.set_string(n_wifi, "passwd", "")

def remove_upd():
    try:
        os.remove("/update.py")
    except:
        print("Update.py deletion error")
        
def clear_temp():
    try:
        os.rmdir("/temp")
    except:
        print("/temp deletion error")

import time

while True:
    render = menus.menu("Recovery menu", [("Reset NVS configuration", 1), ("Delete update.py", 2), ("Clear /temp/", 3), ("Terminal (Requires CardKB)", 4), ("Reboot", 13)])
    if render == 1:
        reset_nvs()
    elif render == 2:
        remove_upd()
    elif render == 3:
        clear_temp()
    elif render == 4:
        import apps.terminal as a_tm
        a_tm.set_tft(tft)
        a_tm.run()
        del a_tm
    elif render == 13:
        machine.reset()