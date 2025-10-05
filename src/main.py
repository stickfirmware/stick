import os

import machine

import modules.buzzer as buzz
import modules.cache as cache
import modules.os_constants as osc
import modules.powersaving as ps
import modules.printer as printer

print("Stick Boot")

# Hold power
if osc.HAS_HOLD_PIN:
    power_hold = machine.Pin(osc.HOLD_PIN, machine.Pin.OUT)
    power_hold.value(1)
    
# Buzzer
if osc.HAS_BUZZER:
    buzzer = machine.PWM(machine.Pin(osc.BUZZER_PIN), duty=0, freq=500)
    buzz.set_volume(0.5)
    buzz.play_sound(buzzer, 400, 0.1)

ps.set_freq(osc.ULTRA_FREQ)

printer.log("Checking boot options...")

try:
    printer.log("Load fonts", printer.Levels.DEBUG)
    import fonts.def_8x8 as f8x8
    import fonts.def_16x32 as f16x32

    # Init tft
    printer.log("Init tft", printer.Levels.DEBUG)
    import modules.tft_init as tft_init
    tft = tft_init.init_tft()
    load_bg = osc.LCD_LOAD_BG
    text_color = osc.LCD_LOAD_TEXT
    printer.log("Showing progressbar render", printer.Levels.DEBUG)
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
    printer.log(str(e), printer.Levels.ERROR)
    
def set_f_boot(var):
    try:
        import modules.io_manager as io_man
        io_man.set('tft',var)
    except Exception:
        printer.log("Failed to set fastboot vars", printer.Levels.ERROR)
    

def recoveryf():
    import recovery.recovery  # noqa: F401
    
if tft is None:
    set_f_boot(None)
    recoveryf()
else:
    set_f_boot(tft)

# Recovery button
RECOVERY_BTN_PIN = osc.BOOT_RECOVERY_PIN

rbtn = machine.Pin(RECOVERY_BTN_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
recovery = rbtn.value() == 0

# Postinstall
import modules.nvs as nvs # noqa
n_updates = cache.get_nvs('updates')
requires_postinstall = nvs.get_int(n_updates, "postinstall")
if requires_postinstall is None:
    requires_postinstall = 1
if requires_postinstall == 1:
    tft.text(f8x8, "Postinstall...",0,106,text_color, load_bg)
    import modules.postinstall as pinstall
    pinstall.postinstall()
    
# Factory reset
factory_reset = nvs.get_int(n_updates, "factory")
if factory_reset == 1:
    tft.text(f8x8, "Factory reset...",0,106,text_color, load_bg)
    nvs.set_int(n_updates, "factory", 0)
    import scripts.factory  # noqa: F401

while True:
    if recovery and osc.BOOT_ENABLE_RECOVERY:
        tft.text(f8x8, "Recovery",180,127,2016)
        printer.log("Booting recovery")
        recovery = False
        recoveryf()
    elif osc.BOOT_UPDATE_PATH in os.listdir("/") and osc.BOOT_ENABLE_UPDATES:
        tft.text(f8x8, "Update script found! Booting..",0,24,65535)
        try:
            printer.log("Update script found! Booting!")
            exec(open(osc.BOOT_UPDATE_PATH).read())
            machine.soft_reset()
        except Exception as e:
            tft.text(f8x8, "Update failed! Rebooting..",0,32,65535)
            printer.log(e, printer.Levels.ERROR)
            machine.soft_reset()
    else:
        try:
            printer.log("Booting mainos")
            import mainos  # noqa: F401
            # Once main loop breaks, go to recovery
            recoveryf()
        except Exception as e:
            printer.log("Critical error, showing bsod", printer.Levels.ERROR)
            printer.log(e, printer.Levels.ERROR)
            import modules.crash_handler as c_handler
            c_handler.crash_screen(tft, 4001, e, True, True, 2)