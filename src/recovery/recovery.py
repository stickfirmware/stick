import modules.os_constants as osc
from modules.decache import decache

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
        print(e)
        return None
    
import modules.fastboot_vars as fvars
if fvars.TFT != None:
    tft = fvars.TFT
else:
    tft = init_tft()
import modules.button_init as btn_init
buttons = btn_init.init_buttons()
button_a = buttons[0]
button_b = buttons[1]
button_c = buttons[2]
print("Init IO manager")
import modules.io_manager as io_man
io_man.set_btn_a(button_a)
io_man.set_btn_b(button_b)
io_man.set_btn_c(button_c)
io_man.set_tft(tft)

import machine
import modules.menus as menus

def reset_nvs():
    import scripts.reset_nvs

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
        
while True:
    render = menus.menu("Recovery menu", [("Reset NVS configuration", 1), ("Delete update.py", 2), ("Clear /temp/", 3), ("Terminal", 4), ("File explorer", 5), ("Reboot", 13)])
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
        a_tm.run()
        decache('apps.terminal')
        del a_tm
    elif render == 5:
        import modules.file_explorer as a_fe
        a_fe.run()
        decache('modules.file_explorer')
        del a_fe
    elif render == 13:
        machine.reset()