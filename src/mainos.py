print("Kitki30 Stick")

##########################
#      IMPORTANT!!!!     #
# If you add some import #
# add it to whitelist in #
# /modules/ram_cleaner   #
# Only if main loop      #
# needs it! Its for      #
# saving ram!!!          #
# Otherwise it will      #
# de-init!!!             #
##########################

# First party imports
from machine import Pin, PWM, SPI
import machine
import esp32
import gc
import network
import os
import time

# System modules
from modules.decache import decache
import modules.ram_cleaner as ram_cleaner
import modules.crash_handler as c_handler
import modules.nvs as nvs
import modules.uptime as uptime
import modules.printer as debug
import modules.buzzer as buzz
import modules.os_constants as osc
import modules.fastboot_vars as fvars

# Scripts
import scripts.checkbattery as battery_shutdown

# Set frequencies
debug.log("Setting Ultra freq")
machine.freq(osc.ULTRA_FREQ)

# Buzzer
debug.log("Buzz tone")
if osc.HAS_BUZZER:
    buzzer = PWM(Pin(osc.BUZZER_PIN), duty_u16=0, freq=500)
    buzz.startup_sound(buzzer)

try:
    os.rmdir("/temp")
except Exception as e:
    print(str(e))
    print("temp deletion error")

if "temp" not in os.listdir():
        os.mkdir("temp")

# Garbage colector
debug.log("Enabling garbage collector")
gc.enable()
gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

# Hold power
if osc.HAS_HOLD_PIN:
    debug.log("Enable hold pin")
    power_hold = Pin(osc.HOLD_PIN, Pin.OUT)
    power_hold.value(1)
else:
    power_hold = None
 
# Import fonts
debug.log("Load fonts")
import fonts.def_8x8 as f8x8
import fonts.def_16x32 as f16x32

# Init tft
debug.log("Init tft")

try:
    tft = fvars.TFT
    if tft == None:
        import modules.tft_init as tft_init
        tft = tft_init.init_tft()
        del tft_init
        decache("modules.tft_init")
    load_bg = osc.LCD_LOAD_BG
    text_color = osc.LCD_LOAD_TEXT
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
debug.log("Load NVS")
n_settings = esp32.NVS("settings")
n_wifi = esp32.NVS("wifi")
n_boot = esp32.NVS("boot")
n_crash = esp32.NVS("crash")
n_locks = esp32.NVS("locks")

render_bar("Loading data...", True)

# Set default vars, load backlight, volume, autorotate and powersaving
if nvs.get_int(n_locks, "dummy") == None:
    nvs.set_int(n_locks, "dummy", 0)
    
s_bl = nvs.get_float(n_settings, "backlight")
if s_bl is None:
    s_bl = 0.5
debug.log("Backlight: " + str(s_bl))
tft.set_backlight(s_bl)

s_vl = nvs.get_float(n_settings, "volume")
if s_vl is None:
    s_vl = 0.5
debug.log("Buzzer volume: " + str(s_vl))
buzz.set_volume(s_vl)

auto_rotate = nvs.get_int(n_settings, "autorotate")
allow_saving = nvs.get_int(n_settings, "allowsaving")
if auto_rotate == None:
    nvs.set_int(n_settings, "autorotate", 1)
    auto_rotate = 1
if allow_saving == None:
    nvs.set_int(n_settings, "allowsaving", 1)
    allow_saving = 1

render_bar("Checking crash info...", True)
    
# Show crash info (if crashed last time)
import modules.crash_info as c_info
c_info.run_check(tft, n_crash)

# Free up some space
decache("modules.crash_info")
del c_info
del n_crash

render_bar("Checking first boot...", True)

# Check if its first boot
debug.log("Check for first boot")
import modules.first_boot_check as first_boot_check
first_boot_check.check(tft)
decache("modules.first_boot_check")
del first_boot_check
    
gc.collect()

render_bar("Init shared I2C", True)

# Import RTC
debug.log("Sync time from external RTC")
rtc = None
i2c = None
mpu = None
if osc.HAS_SHARED_I2C == True:
    try:
        # Init I2C
        i2c = machine.I2C(osc.I2C_SLOT, scl=machine.Pin(osc.I2C_SCL), sda=machine.Pin(osc.I2C_SDA))
    except Exception as e:
        c_handler.crash_screen(tft, 1001, str(e), True, True, 2)
        
    # Init and sync time from rtc
    if osc.HAS_RTC == True:
        import modules.rtc as rtc_bm8536  
        rtc = rtc_bm8536.BM8563(i2c)
        # rtc.set_time((2025, 4, 29, 1, 13, 37, 0, 0))
        dt = rtc.get_time()
        machine.RTC().datetime(dt)
        debug.log(dt)
    else:
        rtc = None
    
    # Init IMU/MPU
    if osc.HAS_IMU == True: 
        from modules.mpu6886 import MPU6886

        mpu = MPU6886(i2c)
        
        # If autorotate is disabled, put IMU to sleep for power saving
        if auto_rotate == 0:
            mpu.sleep_on()
    else:
        mpu = None
        nvs.set_int(n_settings, "autorotate", 0)
        auto_rotate = 0
else:
    mpu = None
    rtc = None
    nvs.set_int(n_settings, "autorotate", 0)
    auto_rotate = 0
    osc.HAS_IMU = False
    osc.HAS_RTC = False
    
render_bar("Init buttons...", True)

# Init buttons
debug.log("Init buttons")
import modules.button_init as btn_init
buttons = btn_init.init_buttons()
button_a = buttons[0]
button_b = buttons[1]
button_c = buttons[2]

# Init IO manager
render_bar("Init IO manager", True)
debug.log("Init IO manager")
import modules.io_manager as io_man
io_man.set_btn_a(button_a)
io_man.set_btn_b(button_b)
io_man.set_btn_c(button_c)
io_man.set_tft(tft)
io_man.set_rtc(rtc)
io_man.set_imu(mpu)
io_man.set_power_hold(power_hold)

render_bar("Wi-Fi init...", True)

# Check Wi-Fi hostname
if nvs.get_string(n_wifi, "hostname") == None:
    network.hostname(osc.WIFI_DEF_HOST)
else:
    network.hostname(nvs.get_string(n_wifi, "hostname"))
    
# Connect to Wi-Fi if its setup
nic = network.WLAN(network.STA_IF)
conn_time = None
if nvs.get_float(n_wifi, "conf") == None:
    nvs.set_float(n_wifi, "conf", 0)
if int(nvs.get_float(n_wifi, "conf")) == 1:
    if nvs.get_int(n_wifi, "autoConnect") == 1:
        try:
            nic.active(False)
            time.sleep(0.2)
            nic.active(True)
            debug.log("Wifi connecting")
            conn_time = time.ticks_ms()
            nic.connect(nvs.get_string(n_wifi, "ssid"), nvs.get_string(n_wifi, "passwd"))
        except Exception as e:
            c_handler.crash_screen(tft, 3001, str(e), True, True, 2)
        
render_bar("Loading other libraries...", True)

# Battery check
import modules.battery_check as b_check

menu = 0
menu_change = True
render_battery = False

# Loop timings
ntp_first = True
ntp_time = time.ticks_ms()
pwr_save_time = time.ticks_ms()
diagnostic_time = time.ticks_ms()
prev_bl = tft.get_backlight()
is_in_saving = False

# IMU Rotations cheat sheet
# 0 - button side down
# 1 - button side right
# 2 - button side up
# 3 - button side left

# IMU/rotation variables
imu_delay = time.ticks_ms()
last_orientation = None
orientation_start_time = 0
stable_orientation = osc.LCD_ROTATIONS["BUTTON_LEFT"]

current_rotation = osc.LCD_ROTATIONS["BUTTON_LEFT"]

# Force landscape function
def allow_only_landscape():
    if stable_orientation == osc.LCD_ROTATIONS["BUTTON_UPPER"] or stable_orientation == osc.LCD_ROTATIONS["BUTTON_BOTTOM"]:
        osc.LCD_ROTATIONS["BUTTON_LEFT"]
    else:
        tft.rotation(int(stable_orientation))
        
# Clean up
render_bar("Cleaning up...")
debug.log("Cleaning up")
debug.log("Before: " + str(gc.mem_free() / 1024 / 1024) + "MB")
del n_boot
gc.collect()
debug.log("After: " + str(gc.mem_free() / 1024 / 1024) + "MB")

# Log max loading count
debug.log("Loading count: " + str(loading_count))

# Init SD Card
render_bar("SD Init", True)
if osc.HAS_SD_SLOT:
    import modules.sdcard as sdcard
    sdcard.init(2, osc.SD_CLK, osc.SD_CS, osc.SD_MISO, osc.SD_MOSI)
    sdcard.mount()

# Load clock
render_bar("Loading clock...", True)
import apps.clock as app_clock

# Wake up function
def wake_up():
    global is_in_saving, pwr_save_time, prev_bl
    is_in_saving = False
    auto_rotate = nvs.get_int(n_settings, "autorotate")
    if auto_rotate == 0:
        stable_orientation = osc.LCD_ROTATIONS["BUTTON_LEFT"]
        if osc.HAS_IMU == True: 
            mpu.sleep_on()
    else:
        if osc.HAS_IMU == True: 
            mpu.sleep_off()
        else:
            auto_rotate = 0
    pwr_save_time = time.ticks_ms()
    tft.set_backlight(nvs.get_float(n_settings, "backlight"))
    machine.freq(osc.BASE_FREQ)

# Set uptime
uptime.uptime_loaded = time.ticks_ms()
was_sleep_triggered = False

# Slow down CPU
machine.freq(osc.BASE_FREQ)

# Print sys.modules
import sys
debug.log(str(sys.modules))

# Main loop
while True:

    # Set CPU frequencies depending on power saving state
    if is_in_saving == False:
        machine.freq(osc.BASE_FREQ)
    else:
        machine.freq(osc.SLOW_FREQ)
    
    # Render clock text
    if menu == 0 and menu_change == False:
        app_clock.clock()
    # Render clock text vertically
    elif menu == 1 and menu_change == False:
        app_clock.clock_vert()
    # Render entire clock
    elif menu_change == True:
        if was_sleep_triggered:
            tft.set_backlight(prev_bl)
            was_sleep_triggered = False

        # Set faster CPU freq for faster rendering
        machine.freq(osc.ULTRA_FREQ)
        render_battery = True
        is_in_saving = False
        pwr_save_time = time.ticks_ms()
        
        # Get values from NVS (To ensure that they are up to date)
        auto_rotate = nvs.get_int(n_settings, "autorotate")
        allow_saving = nvs.get_int(n_settings, "allowsaving")

        # Sleep IMU if not used for power saving
        if auto_rotate == 0:
            stable_orientation = osc.LCD_ROTATIONS["BUTTON_LEFT"]
            if osc.HAS_IMU:
                mpu.sleep_on()
        else:
            if osc.HAS_IMU:
                mpu.sleep_off()
            else:
                auto_rotate = 0

        # Rotate screen to stable orientation
        tft.rotation(int(stable_orientation))
        if stable_orientation in [osc.LCD_ROTATIONS["BUTTON_UPPER"], osc.LCD_ROTATIONS["BUTTON_BOTTOM"]]:
            app_clock.run_clock_vert()
            menu = 1
            btn_init.set_buttons()
        else:
            app_clock.run_clock()
            if stable_orientation == osc.LCD_ROTATIONS["BUTTON_LEFT"]:
                btn_init.set_buttons()
            else:
                btn_init.set_buttons(True)
            menu = 0

        menu_change = False
    
    # Disable wi-fi if not connected
    if conn_time is not None:
        if time.ticks_diff(time.ticks_ms(), conn_time) >= osc.WIFI_DISABLE_TIMEOUT:
            nic = network.WLAN(network.STA_IF)
            if not nic.isconnected():
                nic.active(False)
    
    # Check if Wi-Fi is connected, if not, set connection time     
    if nic.active() and nic.isconnected() == False:
        conn_time = time.ticks_ms()
    
    # Power saving
    if not is_in_saving and time.ticks_diff(time.ticks_ms(), pwr_save_time) >= osc.POWER_SAVE_TIMEOUT and allow_saving == 1:
        # Disable debug/battery info for less lag
        tft.fill_rect(4, 116, 190, 16, 0)
        
        is_in_saving = True
        tft.set_backlight(osc.LCD_POWER_SAVE_BL)
        auto_rotate = 0
        stable_orientation = osc.LCD_ROTATIONS["BUTTON_LEFT"]
        if osc.HAS_IMU:
            mpu.sleep_on()
        was_sleep_triggered = True
        machine.freq(osc.SLOW_FREQ)
    
    # Auto rotation
    if auto_rotate == 1 and time.ticks_diff(time.ticks_ms(), imu_delay) >= osc.IMU_CHECK_TIME and osc.HAS_IMU:
        prev_bl = nvs.get_float(n_settings, "backlight")
        if not is_in_saving:
            tft.set_backlight(prev_bl)
        orientation = mpu.get_orientation()
        imu_delay = time.ticks_ms()
        current_rotation = orientation
        if current_rotation == last_orientation:
            if orientation_start_time == 0:
                orientation_start_time = time.ticks_ms()
            elif time.ticks_diff(time.ticks_ms(), orientation_start_time) >= osc.IMU_STAY_TIME:
                if stable_orientation != current_rotation:
                    stable_orientation = current_rotation
                    debug.log("Orientation changed to:" + str(stable_orientation))
                    menu_change = True
        else:
            last_orientation = current_rotation
            orientation_start_time = time.ticks_ms()
            
    # Dummy mode unlocking
    if button_a.value() == 0 and button_b.value() == 0:
        hold_time = 0.00
        
        # Wake up (If in power saving)
        wake_up()
        
        # Check how much time button c is held down
        while button_b.value() == 0:
            time.sleep(osc.LOOP_WAIT_TIME)
            hold_time += osc.LOOP_WAIT_TIME
        
        # Log hold time
        debug.log(str(hold_time) + "  " + str(nvs.get_int(n_locks, "dummy")))
        
        # Let user through if hold time is more than 1s
        if hold_time >= 1 and nvs.get_int(n_locks, "dummy") != 0:
            if menu == 0:
                # Allow only landscape mode
                allow_only_landscape()
                
                # Init lock menu
                import apps.lock_menu as app_lockmen
                app_lockmen.run()
                # De-cache lock menu (to free up RAM)
                decache("apps.lock_menu")
                del app_lockmen
                menu = 0
                menu_change = True
                
        # Reset power saving time
        pwr_save_time = time.ticks_ms()
        
    # Menu
    if button_a.value() == 0:
        # Wake up (If in power saving)
        wake_up()
        
        # Set basic frequency
        machine.freq(osc.BASE_FREQ)
        
        # Button debounce (Reset loop if holding more than button a, for dummy unlock)
        while button_a.value() == 0 and button_c.value() == 1 and button_b.value() == 1:
            time.sleep(osc.LOOP_WAIT_TIME)
        if button_c.value() == 0 or button_b.value() == 0:
            continue
        
        # Don't allow to pass if in dummy mode
        if nvs.get_int(n_locks, "dummy") == 0:
            # Allow only landscape mode
            allow_only_landscape()
            
            # Sync with rtc (if device has one)
            if rtc is not None:
                dt = rtc.get_time()
                machine.RTC().datetime(dt)
                
            # Open menu
            try:
                import apps.menu as app_menu
                app_menu.run()
                del app_menu
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
            
        # Debounce (For some apps, to not enter power menu or apps menu accidentally)
        while button_a.value() == 0 or button_b.value() == 0 or button_c.value() == 0:
            time.sleep(osc.DEBOUNCE_TIME)
            
        # Additional delay to prevent accidental double click
        time.sleep(0.1)
            
        # Reset power saving
        pwr_save_time = time.ticks_ms()

        # Clean ram
        ram_cleaner.clean()
        
        continue
        
    # Power menu / Quick actions
    if button_c.value() == 0:
        # Wake up
        wake_up()
        
        # Check buttons
        while button_c.value() == 0 and button_a.value() == 1 and button_b.value() == 1:
            time.sleep(osc.LOOP_WAIT_TIME)
        if button_a.value() == 0 or button_b.value() == 0:
            continue
    
        # Open power menu
        import apps.power_menu as app_powermen
        allow_only_landscape()
        app_powermen.run()
        # De-cache
        decache("apps.power_menu")
        del app_powermen
        menu = 0
        menu_change = True
        
        # Reset power saving time
        pwr_save_time = time.ticks_ms()

        # Clean ram
        ram_cleaner.clean()
        
    # Locking menu / Clock menu
    if button_b.value() == 0:
        hold_time = 0.00
        
        # Wake up
        wake_up()
        
        # Check hold time
        while button_b.value() == 0 and button_c.value() == 1 and button_a.value() == 1:
            time.sleep(osc.LOOP_WAIT_TIME)
            hold_time += osc.LOOP_WAIT_TIME
        if button_c.value() == 0 or button_a.value() == 0:
            continue
        
        # Allow if hold more than 1s, else run clock menu
        if hold_time >= 1 and nvs.get_int(n_locks, "dummy") == 0:
            allow_only_landscape()
            # Open lock menu
            import apps.lock_menu as app_lockmen
            app_lockmen.run()
            # De-cache lock menu
            decache("apps.lockmen")
            del app_lockmen
            menu = 0
            menu_change = True
        # Run clock menu if hold less than seconds and not in dummy mode
        elif nvs.get_int(n_locks, "dummy") == 0:
            allow_only_landscape()
            app_clock.clock_menu()
            menu = 0
            menu_change = True
            
        # Reset pwr save
        pwr_save_time = time.ticks_ms()

        # Clean ram
        ram_cleaner.clean()
            
    # Battery check (Diagnostics)
    if not is_in_saving and time.ticks_diff(time.ticks_ms(), diagnostic_time) >= osc.DIAGNOSTIC_REFRESH_TIME and menu == 0:
        # Reset diagnostic refresh time
        diagnostic_time = time.ticks_ms()
        
        # Check battery for low voltage
        battery_shutdown.run()
        
        # Check dummy mode
        locks = nvs.get_int(n_locks, "dummy")
        
        # Collect garbage
        gc.collect()
        
        # Check battery voltage
        volts = b_check.voltage()
        
        # Render only in landscape
        if menu == 0:
            # Clear old info
            tft.fill_rect(4, 116, 190, 16, 0)
            
            # Render CPU info if not in dummy
            if locks == 0:
                tft.text(f8x8, "CPU: " + str(machine.freq() / 1000000) + "MHz",4,116,703)
                
            # Check percentage
            pr = b_check.percentage(volts)
            
            # Show either battery percentage or voltage based on dummy mode
            if locks == 0:
                tft.text(f8x8, "Battery: " + str(volts) + "V / " + str(int(pr)) + "%",4,124,2016)
            else:
                tft.text(f8x8, "Battery: " + str(int(pr)) + "%",4,124,2016)
                
        # Battery bitmap render
        b_check.run(tft)

        # Clean ram
        ram_cleaner.clean()
        
    # NTP sync
    if time.ticks_diff(time.ticks_ms(), ntp_time) >= osc.NTP_SYNC_TIME or ntp_first == False:
        ntp_first = True
        ntp_time = time.ticks_ms()
        nic = network.WLAN(network.STA_IF)
        if nic.isconnected() == True:
            import modules.ntp as ntp
            ntp.sync(rtc)
            del ntp
            if nvs.get_int(n_locks, "dummy") == 0:
                tft.fill_rect(4, 124, 60, 8, 0)
                if menu == 0:
                    tft.text(f8x8, "NTP",4,124,703)
                    
    time.sleep(osc.LOOP_WAIT_TIME)