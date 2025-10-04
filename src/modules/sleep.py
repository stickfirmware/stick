"""
Sleep helper for Stick firmware, helps to put device in sleep
"""

import esp32
import machine
import os
import time

from modules.printer import log
import modules.nvs as nvs
import modules.os_constants as osc
import modules.io_manager as io_man
import modules.cache as cache
import modules.battery_check as b_check
import modules.json as json
import modules.wifi_master as wifiman

tft = None
mpu = io_man.get('imu') 
nic = wifiman.nic
wasConnected = False

# TODO: Refactor this thing
def sleep(deepsleep = False):
    """
    Puts device to lightsleep (or deepsleep),
    disables display and backlight.
    
    Args:
        deepsleep (bool, optional): If true device will go into deepsleep (Doesn't keep RAM!!!)
    """
    global tft
    log("Sleeping")
    
    # Battery report
    bat_info = {
        "time_before_sleep": time.time(),
        "voltage_before_sleep": b_check.voltage(2),
        "time_after_sleep": None,
        "voltage_after_sleep": None
    }
    
    log("Set wake on ext")
    if osc.INPUT_METHOD == 1:
        button_c = io_man.get('button_c')
        esp32.wake_on_ext0(pin = button_c, level = esp32.WAKEUP_ALL_LOW)
    elif osc.INPUT_METHOD == 2:
        esp32.wake_on_ext0(pin = machine.Pin(0,machine.Pin.IN, machine.Pin.PULL_UP), level = esp32.WAKEUP_ALL_LOW)
        
    tft = io_man.get('tft')
        
    log("Turn off backlight")
    tft.set_backlight(0)
    
    log("Clear display")
    tft.fill(0)
    
    log("Put st7789 to sleep")
    tft.sleep_mode(True)
    
    log("Deinit things")
    deinit_things()
    
    log("Going to sleep, Bye!")
    old_freq = machine.freq()
    machine.freq(osc.ULTRA_SLOW_FREQ) # Set freq to ultra slow, i don't know if this helps. Leave it as it is.
    if not deepsleep:
        machine.lightsleep()
    else:
        machine.deepsleep()
        machine.reset() # To prevent any bugs
    
    log("Woken up from light sleep, Hi!")
    machine.freq(osc.ULTRA_FREQ)
    
    log("Init things again")
    init_things()
    
    log("Save battery report")
    bat_info["time_after_sleep"] = time.time()
    bat_info["voltage_after_sleep"] = b_check.voltage(2)
    
    # Save only if something changes
    if bat_info["voltage_after_sleep"] != bat_info["voltage_before_sleep"]:
        json.write(f"/temp/sleep_report_{bat_info["time_after_sleep"]}.json", bat_info)
        
    machine.freq(old_freq)
    
# Functions to deinit or init some power hungry things like PWM.
def deinit_things():
    """
    Deinit power hungry things like PWM, Wi-Fi and even IMU
    """
    global wasConnected, tft
    
    # TFT
    tft = None
    io_man.set('tft', None)
    
    # IR
    ir = io_man.get('IR')
    
    if ir is not None:
        ir.deinit()
        
    # Buzzer
    buzzer = io_man.get('buzzer')
    
    if buzzer is not None:
        buzzer.deinit()
        
    # Wifi
    wasConnected = False
    if nic.isconnected():
        nic.disconnect()
        wasConnected = True
    nic.active(False)
    
    # Sync FS
    os.sync()
    
    # IMU / MPU sleep
    if mpu is not None:
        mpu.sleep_on()
            
def init_things():
    """
    Reinit PWM, Wi-Fi and IMU
    """
    global tft
    # TFT
    import modules.tft_init as tftinit
    
    tft = tftinit.init_tft()
    io_man.set('tft', tft)
    
    n_settings = cache.get_nvs('settings')
    s_bl = nvs.get_float(n_settings, "backlight")
    del n_settings
    if s_bl is None:
        tft.set_backlight(0.5)
    else:
        tft.set_backlight(s_bl)
        
    # IR
    ir = io_man.get('IR')
    
    if ir is not None:
        ir.init(freq=38000, duty_u16=0)
        
    # Buzzer
    buzzer = io_man.get('buzzer')
    
    if buzzer is not None:
        buzzer.init(duty_u16=0, freq=400)
        
    # IMU
    if mpu is not None:
        mpu.sleep_off()
            
    # Wi-Fi
    if wasConnected:
        n_wifi = cache.get_nvs('wifi')
        nic.active(True)
        nic.connect(nvs.get_string(n_wifi, "ssid"), nvs.get_string(n_wifi, "passwd"))