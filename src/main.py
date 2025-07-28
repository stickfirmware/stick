print("Stick Boot")

# Uptime
import modules.uptime as uptime

class FakeST:
    def text(self, *k):
        return None
    def fill(self, *k):
        return None

import machine, time
import os
import modules.os_constants as osc
machine.freq(osc.ULTRA_FREQ)

# Hold power
if osc.HAS_HOLD_PIN:
    print("\nEnable hold pin")
    power_hold = machine.Pin(osc.HOLD_PIN, machine.Pin.OUT)
    power_hold.value(1)

import modules.buzzer as buzz
if osc.HAS_BUZZER:
    buzzer = machine.PWM(machine.Pin(osc.BUZZER_PIN), duty_u16=0, freq=500)
    buzz.set_volume(0.1)
    buzz.play_sound(buzzer, 2000, 0.0125)

print("Checking boot options...")

# Recovery button
RECOVERY_BTN_PIN = osc.BOOT_RECOVERY_PIN

rbtn = machine.Pin(RECOVERY_BTN_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
recovery = rbtn.value() == 0

try:
    print("Load fonts")
    import fonts.def_8x8 as f8x8
    import fonts.def_16x32 as f16x32

    # Init tft
    print("Init tft")
    import modules.st7789 as st7789
    tft = st7789.ST7789(
            machine.SPI(osc.LCD_SPI_SLOT, baudrate=osc.LCD_SPI_BAUD, sck=machine.Pin(osc.LCD_SPI_SCK), mosi=machine.Pin(osc.LCD_SPI_MOSI), miso=osc.LCD_SPI_MISO),
            osc.LCD_HEIGHT,
            osc.LCD_WIDTH,
            reset=machine.Pin(osc.LCD_RESET, machine.Pin.OUT),
            cs=machine.Pin(osc.LCD_SPI_CS, machine.Pin.OUT),
            dc=machine.Pin(osc.LCD_DC, machine.Pin.OUT),
            backlight=machine.PWM(machine.Pin(osc.LCD_BL), freq=osc.LCD_BL_FREQ),
            rotation=osc.LCD_ROTATIONS["BUTTON_LEFT"])
    load_bg = osc.LCD_LOAD_BG
    text_color = osc.LCD_LOAD_TEXT
    tft.fill(load_bg)
    tft.text(f16x32, "Stick firmware",0,0,text_color, load_bg)
    tft.text(f8x8, "Booting...",0,106,text_color, load_bg)
    tft.fill_rect(0, 132, 240, 3, text_color)
    tft.fill_rect(0, 112, 240, 3, text_color)
    tft.fill_rect(0, 112, 3, 23, text_color)
    tft.fill_rect(237, 112, 3, 23, text_color)
    tft.text(f8x8, "Developed by Kitki30",0,32,text_color, load_bg)
except Exception as e:
    tft = None
    print(str(e))
    
def set_f_boot(var):
    try:
        import modules.fastboot_vars as fvars
        fvars.TFT = var
    except:
        print("Failed to set fastboot vars")
    
if tft == None:
    tft = FakeST()
    set_f_boot(None)
else: 
    set_f_boot(tft)


def recoveryf():
    import recovery.recovery

while True:
    if recovery and osc.BOOT_ENABLE_RECOVERY == True:
        tft.text(f8x8, "Recovery",180,127,2016)
        print("Booting recovery")
        recovery = False
        recoveryf()
    elif osc.BOOT_UPDATE_PATH in os.listdir("/") and osc.BOOT_ENABLE_UPDATES:
        tft.text(f8x8, "Update script found! Booting..",0,24,65535)
        try:
            print("Update script found! Booting!")
            exec(open(osc.BOOT_UPDATE_PATH).read())
            machine.soft_reset()
        except Exception as e:
            tft.text(f8x8, "Update failed! Rebooting..",0,32,65535)
            print(e)
            machine.soft_reset()
    else:
        try:
            uptime.uptime_bootloader = time.ticks_ms()
            print("Booting mainos")
            import mainos
        except Exception as e:
            print(e)
            print("Booting mainos failed, booting recovery!")
            recoveryf()