print("Kitki30 Stick")

# Hold power
from machine import Pin, PWM, SPI
print("\nEnable hold pin")
power_hold = Pin(4, Pin.OUT)
power_hold.value(1)

# Buzzer
print("Buzz tone")
import modules.buzzer as buzz
buzzer = PWM(Pin(2), duty_u16=0, freq=500)
buzz.startup_sound(buzzer)

# Allocate emergency buffer
import micropython
print("Allocating emergency buffer (1000 bytes)")
micropython.alloc_emergency_exception_buf(1000)
del micropython

import machine
import esp32

import modules.crash_handler as c_handler
import modules.nvs as nvs

import network

import time

# Garbage colector
print("Enabling garbage collector")
import gc
gc.enable()

# Hold power
print("Enable hold pin")
power_hold = Pin(4, Pin.OUT)
power_hold.value(1)

# Set frequencies
print("Setting 240mhz freq")
machine.freq(240000000)
  
# Import fonts
print("Load fonts")
import fonts.def_8x8 as f8x8
import fonts.def_8x16 as f8x16
import fonts.def_16x16 as f16x16
import fonts.def_16x32 as f16x32

# Init tft
print("Init tft")
import modules.st7789 as st7789

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
except Exception as e:
    c_handler.crash_screen(tft, 1002, str(e), True, False, 1)

# Load NVS
print("Load NVS")
tft.text(f8x8, "Init NVS...",0,0,65535)
n_settings = esp32.NVS("settings")
n_wifi = esp32.NVS("wifi")
n_boot = esp32.NVS("boot")
n_crash = esp32.NVS("crash")

# Show crash info (if crashed last time)
import modules.crash_info as c_info
c_info.run_check(tft, n_crash)

# Free up some space
del c_info
del n_crash

# Check first boot
print("Check for first boot")
import modules.first_boot_check as f_b_check
f_b_check.check(tft)
del f_b_check
    
# Clear tft
tft.fill(0)

gc.collect()

# Welcome screen
print("Show welcome screen")
tft.text(f16x16, "Kitki30 Stick",0,0,65535)
tft.text(f8x8, "Loading...",0,127,65535)

# Import RTC
print("Sync time from external RTC")
import modules.rtc as rtc_bm8536
tft.text(f8x8, "Getting RTC time...",0,16,65535)

try:
    i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))
    rtc = rtc_bm8536.BM8563(i2c)
except Exception as e:
    c_handler.crash_screen(tft, 1001, str(e), True, True, 2)

# rtc.set_time((2025, 4, 29, 1, 13, 37, 0, 0))
dt = rtc.get_time()
tft.text(f8x8, "DONE!",180,16,2016)
machine.RTC().datetime(dt)
print(dt)

# Init buttons
print("Init buttons")
tft.text(f8x8, "Init buttons...",0,24,65535)
button_a = Pin(37, Pin.IN, Pin.PULL_UP)
button_b = Pin(39, Pin.IN, Pin.PULL_UP)
button_c = Pin(35, Pin.IN, Pin.PULL_UP)
tft.text(f8x8, "DONE!",180,24,2016)

# Load settings
print("Loading settings from NVS")
tft.text(f8x8, "Load setting...",0,32,65535)
s_bl = nvs.get_float(n_settings, "backlight")
print("Backlight: " + str(s_bl))
tft.set_backlight(s_bl)
s_vl = nvs.get_float(n_settings, "volume")
print("Buzzer volume: " + str(s_vl))
buzz.set_volume(s_vl)
tft.text(f8x8, "DONE!",180,32,2016)

# Clean up
print("Cleaning up")
tft.text(f8x8, "Cleaning up...",0,40,65535)
print("Before: " + str(gc.mem_free() / 1024 / 1024) + "MB")
del n_boot
gc.collect()
print("After: " + str(gc.mem_free() / 1024 / 1024) + "MB")
tft.text(f8x8, "DONE!",180,40,2016)

tft.text(f8x8, "Connect to Wi-Fi",0,48,65535)
network.hostname("Kitki30Stick")
if int(nvs.get_float(n_wifi, "conf")) == 1:
    if nvs.get_int(n_wifi, "autoConnect") == 1:
        try:
            nic = network.WLAN(network.STA_IF)
            nic.active(False)
            time.sleep(0.2)
            nic.active(True)
            print("Wifi connecting")
            nic.connect(nvs.get_string(n_wifi, "ssid"), nvs.get_string(n_wifi, "passwd"))
        except Exception as e:
            c_handler.crash_screen(tft, 3001, str(e), True, True, 2)
        

# Battery check
time_to_check=0
import modules.battery_check as b_check

# Clock
import apps.clock as a_clock

menu = 0
menu_change = True
render_battery = False

ntp_sync = 1200

import modules.menus as menus
menus.set_btf(button_a, button_b, button_c, tft)

machine.freq(80000000)
while True: 
    if menu == 0 and menu_change == False:
        a_clock.clock()
    elif menu == 0 and menu_change == True:
        # Render base faster
        machine.freq(240000000)
        render_battery = True
        a_clock.set_tft(tft)
        a_clock.run_clock()
        a_clock.clock()
        menu_change = False
        # Back to power saving
        machine.freq(80000000)
        
    if button_a.value() == 0:
        while button_a.value() == 0:
            time.sleep(0.02)
        dt = rtc.get_time()
        machine.RTC().datetime(dt)
        import apps.menu as a_menu
        a_menu.set_btf(button_a, button_b, button_c, tft, rtc)
        a_menu.run()
        del a_menu
        menu = 0
        menu_change = True
        
    if button_c.value() == 0:
        while button_c.value() == 0:
            time.sleep(0.02)
        if menu == 0:
            import apps.powermenu as a_powermen
            a_powermen.set_btf(button_a, button_b, button_c, power_hold, tft)
            a_powermen.run()
            del a_powermen
            menu = 0
            menu_change = True
            
    # Battery check
    if time_to_check == 0 and menu  == 0:
        gc.collect()
        print("Checking battery")
        print("Voltage: " + str(b_check.voltage()) + "V")
        if menu == 0:
            tft.fill_rect(4, 124, 60, 8, 0)
            tft.text(f8x8, "Battery: " + str(b_check.voltage()) + "V",4,124,2016)
        b_check.run(tft)
        time_to_check = 120
    if ntp_sync == 0:
        ntp_sync = 24000
        if nic.isconnected() == True:
            import modules.ntp as ntp
            ntp.sync(rtc)
            del ntp
            tft.fill_rect(4, 124, 60, 8, 0)
            tft.text(f8x8, "NTP",4,124,703)
    time_to_check-=1
    ntp_sync-=1
    time.sleep(0.025)