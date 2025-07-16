print("Kitki30 Stick")

import modules.osconstants as osc
import scripts.checkbattery as btshutdown
from machine import Pin, PWM, SPI
import random

# Buzzer
print("Buzz tone")
import modules.buzzer as buzz
buzzer = PWM(Pin(osc.BUZZER_PIN), duty_u16=0, freq=500)
buzz.startup_sound(buzzer)

# Uptime
import modules.uptime as uptime

import machine
import esp32

import modules.crash_handler as c_handler
import modules.nvs as nvs

import network
import os
import time

try:
    os.rmdir("/temp")
except Exception as e:
    print(str(e))
    print("temp deletion error")

if "temp" not in os.listdir():
        os.mkdir("temp")

# Garbage colector
print("Enabling garbage collector")
import gc
gc.enable()

# Hold power
print("Enable hold pin")
power_hold = Pin(osc.HOLD_PIN, Pin.OUT)
power_hold.value(1)

# Set frequencies
print("Setting Ultra freq")
machine.freq(osc.ULTRA_FREQ)
  
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
    import modules.fastboot_vars as fvars
    tft = fvars.TFT
    if tft == None:
        tft = st7789.ST7789(
            SPI(osc.LCD_SPI_SLOT, baudrate=osc.LCD_SPI_BAUD, sck=Pin(osc.LCD_SPI_SCK), mosi=Pin(osc.LCD_SPI_MOSI), miso=osc.LCD_SPI_MISO),
            osc.LCD_HEIGHT,
            osc.LCD_WIDTH,
            reset=Pin(osc.LCD_RESET, Pin.OUT),
            cs=Pin(osc.LCD_SPI_CS, Pin.OUT),
            dc=Pin(osc.LCD_DC, Pin.OUT),
            backlight=PWM(Pin(osc.LCD_BL), freq=osc.LCD_BL_FREQ),
            rotation=osc.LCD_ROTATIONS["BUTTON_LEFT"])
    load_bg = 0 # Loading screen backgroung
    text_color = 65535 # Loading screen text color
    tft.fill(load_bg)
    tft.text(f16x32, "Stick firmware",0,0,text_color, load_bg)
    tft.fill_rect(0, 132, 240, 3, text_color)
    tft.fill_rect(0, 112, 240, 3, text_color)
    tft.fill_rect(0, 112, 3, 23, text_color)
    tft.fill_rect(237, 112, 3, 23, text_color)
    tft.text(f8x8, "Developed by Kitki30",0,32,text_color, load_bg)
except Exception as e:
    c_handler.crash_screen(None, 1002, str(e), True, False, 1)

loading_count = 0 # Increased with every task
loading_max = 10 # Max loading_count will reach
bar_color = 2016 # Color of progress bar

def render_bar(text, increase_count=False):
    global loading_count
    tft.fill_rect(0, 106, 240, 8, load_bg)
    tft.text(f8x8, text,0,106,text_color, load_bg)
    if increase_count:
        loading_count += 1
    tft.fill_rect(3, 115, 3 + (234 // loading_max) * loading_count, 18, bar_color)
    
render_bar("Preparing NVS...")

# Load NVS
print("Load NVS")
n_settings = esp32.NVS("settings")
n_wifi = esp32.NVS("wifi")
n_boot = esp32.NVS("boot")
n_crash = esp32.NVS("crash")
n_locks = esp32.NVS("locks")

render_bar("Loading data...", True)

if nvs.get_int(n_locks, "dummy") == None:
    nvs.set_int(n_locks, "dummy", 0)
    
s_bl = nvs.get_float(n_settings, "backlight")
if s_bl is None:
    s_bl = 0.5
print("Backlight: " + str(s_bl))
tft.set_backlight(s_bl)

s_vl = nvs.get_float(n_settings, "volume")
if s_vl is None:
    s_vl = 0.5
print("Buzzer volume: " + str(s_vl))
buzz.set_volume(s_vl)

auto_rotate = nvs.get_int(n_settings, "autorotate")
allow_saving = nvs.get_int(n_settings, "allowsaving")
if auto_rotate == None:
    nvs.set_int(n_settings, "autorotate", 1)
    auto_rotate = 1
if allow_saving == None:
    nvs.set_int(n_settings, "allowsaving", 1)
    auto_rotate = 1

render_bar("Checking crash info...", True)
    
# Show crash info (if crashed last time)
import modules.crash_info as c_info
c_info.run_check(tft, n_crash)

# Free up some space
del c_info
del n_crash

render_bar("Checking first boot...", True)

# Check first boot
print("Check for first boot")
import modules.first_boot_check as f_b_check
f_b_check.check(tft)
del f_b_check
    
gc.collect()

render_bar("Sync RTC...", True)

# Import RTC
print("Sync time from external RTC")
import modules.rtc as rtc_bm8536
try:
    i2c = machine.I2C(osc.I2C_SLOT, scl=machine.Pin(osc.I2C_SCL), sda=machine.Pin(osc.I2C_SDA))
    rtc = rtc_bm8536.BM8563(i2c)
except Exception as e:
    c_handler.crash_screen(tft, 1001, str(e), True, True, 2)
    
# rtc.set_time((2025, 4, 29, 1, 13, 37, 0, 0))
dt = rtc.get_time()
machine.RTC().datetime(dt)
print(dt)

render_bar("Init IMU...", True)
    
from modules.mpu6886 import MPU6886

print("Init IMU")
mpu = MPU6886(i2c)

if auto_rotate == 0:
    mpu.sleep_on()

def get_orientation(ax, ay, az, threshold=osc.IMU_ROTATE_THRESHOLD):
    if ay < -threshold:
        return osc.LCD_ROTATIONS["BUTTON_UPPER"]
    elif ax > threshold:
        return osc.LCD_ROTATIONS["BUTTON_RIGHT"]
    elif ay > threshold:
        return osc.LCD_ROTATIONS["BUTTON_BOTTOM"]
    elif ax < -threshold:
        return osc.LCD_ROTATIONS["BUTTON_LEFT"]
    else:
        return osc.LCD_ROTATIONS["BUTTON_LEFT"]
    
render_bar("Init buttons...", True)

# Init buttons
print("Init buttons")
button_a = Pin(osc.BUTTON_A_PIN, Pin.IN, Pin.PULL_UP)
button_b = Pin(osc.BUTTON_B_PIN, Pin.IN, Pin.PULL_UP)
button_c = Pin(osc.BUTTON_C_PIN, Pin.IN, Pin.PULL_UP)

def set_buttons(inverted=False):
    global button_b
    global button_c
    if inverted:
        button_b = Pin(osc.BUTTON_C_PIN, Pin.IN, Pin.PULL_UP)
        button_c = Pin(osc.BUTTON_B_PIN, Pin.IN, Pin.PULL_UP)
    else:
        button_b = Pin(osc.BUTTON_B_PIN, Pin.IN, Pin.PULL_UP)
        button_c = Pin(osc.BUTTON_C_PIN, Pin.IN, Pin.PULL_UP)

render_bar("Check OOBE...", True)
import apps.oobe as oobe
#oobe.set_btf(button_a, button_b, button_c, tft)
#oobe.run()

render_bar("Wi-Fi init...", True)

if nvs.get_string(n_wifi, "hostname") == None:
    network.hostname(osc.WIFI_DEF_HOST)
else:
    network.hostname(nvs.get_string(n_wifi, "hostname"))
    
conn_time = None
if nvs.get_float(n_wifi, "conf") == None:
    nvs.set_float(n_wifi, "conf", 0)
if int(nvs.get_float(n_wifi, "conf")) == 1:
    if nvs.get_int(n_wifi, "autoConnect") == 1:
        try:
            nic = network.WLAN(network.STA_IF)
            nic.active(False)
            time.sleep(0.2)
            nic.active(True)
            print("Wifi connecting")
            conn_time = time.ticks_ms()
            nic.connect(nvs.get_string(n_wifi, "ssid"), nvs.get_string(n_wifi, "passwd"))
        except Exception as e:
            c_handler.crash_screen(tft, 3001, str(e), True, True, 2)
        
render_bar("Loading other libraries...", True)

# Battery check
time_to_check=0
import modules.battery_check as b_check

menu = 0
menu_change = True
render_battery = False

ntp_sync = 1200

import modules.menus as menus
menus.set_btf(button_a, button_b, button_c, tft)
import modules.numpad as npad
npad.set_btf(button_a, button_b, button_c, tft)
import modules.openFile as openfile
openfile.set_btf(button_a, button_b, button_c, tft)

machine.freq(osc.BASE_FREQ)

ntpfirst = False
ntpTime = time.ticks_ms()
sleepTime = time.ticks_ms()
prevBl = tft.get_backlight()
isInSaving = False

# IMU Rotations cheat sheet
# 0 - button side down
# 1 - button side right
# 2 - button side up
# 3 - button side left

mpuDelay = time.ticks_ms()
last_orientation = None
orientation_start_time = 0
stable_orientation = 3

currentrotation = 3

def allowonlylandscape():
    if stable_orientation == osc.LCD_ROTATIONS["BUTTON_UPPER"] or stable_orientation == osc.LCD_ROTATIONS["BUTTON_BOTTOM"]:
        tft.rotation(3)
    else:
        tft.rotation(int(stable_orientation))
        
# Clean up
render_bar("Cleaning up...")
print("Cleaning up")
print("Before: " + str(gc.mem_free() / 1024 / 1024) + "MB")
del n_boot
gc.collect()
print("After: " + str(gc.mem_free() / 1024 / 1024) + "MB")

print("Loading count: " + str(loading_count))

render_bar("Loading clock...", True)
import apps.clock as a_clock
a_clock.set_tft(tft)

def wakeUp():
    global isInSaving, sleepTime, prevBl
    if isInSaving == True:
        isInSaving = False
        sleepTime = time.ticks_ms()
        tft.set_backlight(prevBl)
        machine.freq(osc.BASE_FREQ)

while True:
    machine.freq(osc.BASE_FREQ)
    if conn_time is not None:
        if time.ticks_diff(time.ticks_ms(), conn_time) >= osc.WIFI_DISABLE_TIMEOUT:
            nic = network.WLAN(network.STA_IF)
            if nic.isconnected() == False:
                nic.active(False)
    if not isInSaving and time.ticks_diff(time.ticks_ms(), sleepTime) >= osc.POWER_SAVE_TIMEOUT and allow_saving == 1:
        prevBl = tft.get_backlight()
        isInSaving = True
        tft.set_backlight(osc.LCD_POWER_SAVE_BL)
        machine.freq(osc.SLOW_FREQ)
    if auto_rotate == 1 and time.ticks_diff(time.ticks_ms(), mpuDelay) >= osc.IMU_CHECK_TIME:
        prevBl = nvs.get_float(n_settings, "backlight")
        if not isInSaving:
            tft.set_backlight(prevBl)
        ax, ay, az = mpu.acceleration
        orientation = get_orientation(ax, ay, az)
        mpuDelay = time.ticks_ms()
        currentrotation = orientation
        if currentrotation == last_orientation:
            if orientation_start_time == 0:
                orientation_start_time = time.ticks_ms()
            elif time.ticks_diff(time.ticks_ms(), orientation_start_time) >= osc.IMU_STAY_TIME:
                if stable_orientation != currentrotation:
                    stable_orientation = currentrotation
                    print("Orientation changed to:", stable_orientation)
                    menu_change = True
        else:
            last_orientation = currentrotation
            orientation_start_time = time.ticks_ms()
    if menu == 0 and menu_change == False:
        a_clock.clock()
    elif menu == 1 and menu_change == False:
        a_clock.clock_vert()
    elif menu_change == True:
        
        # Render base faster
        machine.freq(osc.ULTRA_FREQ)
        render_battery = True
        
        isInSaving = False
        sleepTime = time.ticks_ms()
        a_clock.set_tft(tft)
        auto_rotate = nvs.get_int(n_settings, "autorotate")
        allow_saving = nvs.get_int(n_settings, "allowsaving")
        if auto_rotate == 0:
            stable_orientation = 3
            mpu.sleep_on()
        else:
            mpu.sleep_off()
        if stable_orientation == osc.LCD_ROTATIONS["BUTTON_UPPER"] or stable_orientation == osc.LCD_ROTATIONS["BUTTON_BOTTOM"]:
            tft.rotation(int(stable_orientation))
            a_clock.run_clock_vert()
            menu = 1
            set_buttons()
        else:
            tft.rotation(int(stable_orientation))
            a_clock.run_clock()
            if stable_orientation == 3:
                set_buttons()
            else:
                set_buttons(True)
            
            menu = 0
        menus.set_btf(button_a, button_b, button_c, tft)
        npad.set_btf(button_a, button_b, button_c, tft)
        
        menu_change = False
        # Back to power saving
        machine.freq(osc.BASE_FREQ)
    if button_a.value() == 0 and button_b.value() == 0:
        holdTime = 0.00
        wakeUp()
        while button_b.value() == 0:
            time.sleep(osc.LOOP_WAIT_TIME)
            holdTime += osc.LOOP_WAIT_TIME
        print(str(holdTime) + "  " + str(nvs.get_int(n_locks, "dummy")))
        if holdTime >= 1 and nvs.get_int(n_locks, "dummy") != 0:
            if menu == 0:
                allowonlylandscape()
                import apps.lockmen as a_lockmen
                a_lockmen.set_btf(button_a, button_b, button_c, tft)
                a_lockmen.run()
                del a_lockmen
                menu = 0
                menu_change = True
        sleepTime = time.ticks_ms()
    if button_a.value() == 0:
        wakeUp()
        machine.freq(osc.BASE_FREQ)
        while button_a.value() == 0 and button_c.value() == 1 and button_b.value() == 1:
            time.sleep(osc.LOOP_WAIT_TIME)
        if button_c.value() == 0 or button_b.value() == 0:
            continue
        
        if nvs.get_int(n_locks, "dummy") == 0:
            allowonlylandscape()
            dt = rtc.get_time()
            machine.RTC().datetime(dt)
            try:
                import apps.menu as a_menu
                a_menu.set_btf(button_a, button_b, button_c, tft, rtc)
                a_menu.run()
                del a_menu
            except Exception as e:
                tft.fill(0)
                gc.collect()
                tft.text(f16x32, "Oops!",0,0,17608)
                tft.text(f8x8, "One of your apps has crashed!",0,32,65535)
                tft.text(f8x8, "Please try again!",0,40,65535)
                print(str(e))
                time.sleep(3)
            menu = 0
            menu_change = True
        sleepTime = time.ticks_ms()
    if button_c.value() == 0:
        wakeUp()
        while button_c.value() == 0 and button_a.value() == 1 and button_b.value() == 1:
            time.sleep(osc.LOOP_WAIT_TIME)
        if button_a.value() == 0 or button_b.value() == 0:
            continue
        if menu == 0:
            import apps.powermenu as a_powermen
            allowonlylandscape()
            a_powermen.set_btf(button_a, button_b, button_c, power_hold, tft, mpu)
            a_powermen.run()
            del a_powermen
            menu = 0
            menu_change = True
        sleepTime = time.ticks_ms()
    if button_b.value() == 0:
        holdTime = 0.00
        wakeUp()
        while button_b.value() == 0 and button_c.value() == 1 and button_a.value() == 1:
            time.sleep(osc.LOOP_WAIT_TIME)
            holdTime += osc.LOOP_WAIT_TIME
        if button_c.value() == 0 or button_a.value() == 0:
            continue
        if holdTime >= 1 and nvs.get_int(n_locks, "dummy") == 0:
            if menu == 0:
                allowonlylandscape()
                import apps.lockmen as a_lockmen
                a_lockmen.set_btf(button_a, button_b, button_c, tft)
                a_lockmen.run()
                del a_lockmen
                menu = 0
                menu_change = True
        sleepTime = time.ticks_ms()
            
    # Battery check
    if time_to_check == 0 and menu  == 0:
        btshutdown.run()
        locks = nvs.get_int(n_locks, "dummy")
        gc.collect()
        print("Checking battery")
        volts = b_check.voltage()
        print("Voltage: " + str(volts) + "V")
        if menu == 0:
            tft.fill_rect(4, 116, 190, 8, 0)
            if locks == 0:
                tft.text(f8x8, "CPU: " + str(machine.freq() / 1000000) + "MHz",4,116,703)
            pr = (volts - 3.00) / 1.20 * 100
            print(pr)
            if pr <= 0.00:
                pr = 0.00
            elif pr >= 100.00:
                pr = 100.00
            if locks == 0:
                tft.text(f8x8, "Battery: " + str(volts) + "V / " + str(int(pr)) + "%",4,124,2016)
            else:
                tft.text(f8x8, "Battery: " + str(int(pr)) + "%",4,124,2016)
        b_check.run(tft)
        time_to_check = 120
    if time.ticks_diff(time.ticks_ms(), ntpTime) >= osc.NTP_SYNC_TIME or ntpfirst == False:
        ntpfirst = True
        ntpTime = time.ticks_ms()
        nic = network.WLAN(network.STA_IF)
        if nic.isconnected() == True:
            import modules.ntp as ntp
            ntp.sync(rtc)
            del ntp
            if nvs.get_int(n_locks, "dummy") == 0:
                tft.fill_rect(4, 124, 60, 8, 0)
                if menu == 0:
                    tft.text(f8x8, "NTP",4,124,703)
    time_to_check-=1
    time.sleep(osc.LOOP_WAIT_TIME)