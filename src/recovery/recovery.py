import modules.osconstants as osc

def init_tft():
    import modules.st7789 as st7789
    from machine import PWM, Pin, SPI
    try:
        tft = st7789.ST7789(
            machine.SPI(osc.LCD_SPI_SLOT, baudrate=osc.LCD_SPI_BAUD, sck=machine.Pin(osc.LCD_SPI_SCK), mosi=machine.Pin(osc.LCD_SPI_MOSI), miso=osc.LCD_SPI_MISO),
            osc.LCD_HEIGHT,
            osc.LCD_WIDTH,
            reset=machine.Pin(osc.LCD_RESET, Pin.OUT),
            cs=machine.Pin(osc.LCD_SPI_CS, Pin.OUT),
            dc=machine.Pin(osc.LCD_DC, Pin.OUT),
            backlight=machine.PWM(Pin(osc.LCD_BL), freq=osc.LCD_BL_FREQ),
            rotation=osc.LCD_ROTATIONS["BUTTON_LEFT"])
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
    exec(open("/scripts/reset_nvs.py").read())

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
        render1 = menus.menu("Destroy nvs?", [("No", 1), ("Yes", 2)])
        if render1 == 2:
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