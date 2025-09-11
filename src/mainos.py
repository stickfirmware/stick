print("Stick firmware")

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
from machine import Pin, PWM
import machine
import gc
import network
import os
import time

# System modules
from modules.decache import decache
import modules.ram_cleaner as ram_cleaner
import modules.crash_handler as c_handler
import modules.nvs as nvs
import modules.printer as debug
import modules.buzzer as buzz
import modules.os_constants as osc
import modules.io_manager as io_man
import modules.cache as cache
import modules.powersaving as ps
import modules.files as files

# Scripts
import scripts.checkbattery as battery_shutdown

# Set frequencies
debug.log("Setting Ultra freq")
ps.set_freq(osc.ULTRA_FREQ)

# Buzzer
debug.log("Buzz tone")
if osc.HAS_BUZZER:
    buzzer = PWM(Pin(osc.BUZZER_PIN), duty_u16=0, freq=500)
    io_man.set("buzzer", buzzer)
    buzz.startup_sound(buzzer)

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
    tft = io_man.get('tft')
    if tft == None:
        import modules.tft_init as tft_init
        tft = tft_init.init_tft()
        del tft_init
        decache("modules.tft_init")
    load_bg = osc.LCD_LOAD_BG
    text_color = osc.LCD_LOAD_TEXT
except Exception as e:
    c_handler.crash_screen(None, 1002, str(e), True, False, 1)
io_man.set('tft', tft)

loading_count = 0 # Increased with every task
loading_max = 12 # Max loading_count will reach
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
debug.log("Load cache")
cache.precache()
n_settings = cache.get_nvs('settings')
n_wifi = cache.get_nvs('wifi')
n_boot = cache.get_nvs('boot')
n_locks = cache.get_nvs('locks')
n_guides = cache.get_nvs('guides')

render_bar("Loading data...", True)

# Set default vars, load backlight, volume, autorotate and powersaving
import modules.nvs_set_def as nsd
nsd.run()
    
s_bl = cache.get_and_remove('n_cache_backlight')
debug.log("Backlight: " + str(s_bl))
tft.set_backlight(s_bl)

s_vl = cache.get_and_remove('n_cache_volume')
debug.log("Buzzer volume: " + str(s_vl))
buzz.set_volume(s_vl)

auto_rotate = cache.get('n_cache_arotate')
allow_saving = cache.get_and_remove('n_cache_pwrsave')

render_bar("Load translations...", True)
debug.log("Load translations")

import modules.translate as translate
translate.load(cache.get('n_cache_lang'))
from modules.translate import get as l_get
render_bar(l_get("mainos_load.first_boot_check"), True) # Checking first boot...

# Check if its first boot
debug.log("Check for first boot")
import modules.first_boot_check as first_boot_check
first_boot_check.check()
decache("modules.first_boot_check")
del first_boot_check
    
gc.collect()

# Init shared i2c
debug.log("Init shared i2c")
render_bar(l_get("mainos_load.shared_iic_init"), True) # Init shared I2C...

# Import RTC
debug.log("Sync time from external RTC")
rtc = None
i2c = None
mpu = None
if osc.HAS_SHARED_I2C == True:
    import modules.i2c_init as i2c_init
    i2c, rtc, mpu = i2c_init.init()
else:
    mpu = None
    rtc = None
    nvs.set_int(n_settings, "autorotate", 0)
    auto_rotate = 0
    osc.HAS_IMU = False
    osc.HAS_RTC = False

render_bar(l_get("mainos_load.init_btns"), True) # Init buttons...

# Init buttons
debug.log("Init buttons")
import modules.button_init as btn_init
button_a, button_b, button_c, clicker = btn_init.init_buttons()

# Init neopixel
render_bar(l_get("mainos_load.init_neopixel"), True)
if osc.HAS_NEOPIXEL == True:
    import modules.neopixels as neopixels
    import modules.neopixel_anims as np_anims
    neopixels.make(osc.NEOPIXEL_PIN, osc.NEOPIXEL_LED_COUNT)

# Init IO manager (Set buttons, tft, etc.)
render_bar(l_get("mainos_load.init_io_man"), True)
debug.log("Init IO manager")
io_man.set('button_a', button_a)
io_man.set('button_b', button_b)
io_man.set('button_c', button_c)
io_man.set('clicker_btn', clicker)
io_man.set('rtc', rtc)
io_man.set('mpu', mpu)
io_man.set('power_hold', power_hold)

render_bar(l_get("mainos_load.check_time"), True)

import modules.ntp as ntp
ntp.wrong_time_support()

render_bar(l_get("mainos_load.init_wifi"), True)
import modules.wifi_master as wifi_master
wifi_master.connect_main_loop()
nic = network.WLAN(network.STA_IF)
conn_time = time.ticks_ms()
        
# Sync apps
render_bar(l_get("mainos_load.sync_apps"), True)
import apps.oobe as oobe
oobe.sync_apps()
        
render_bar(l_get("mainos_load.load_libs"), True) # Loading other libraries...

# Battery check
import modules.battery_check as b_check

menu = 0
menu_change = True
render_battery = False

# Loop timings
ntp_first = True
ticks = time.ticks_ms()
ntp_time = ticks
pwr_save_time = ticks
diagnostic_time = ticks
wifi_master_dynamic = ticks
cleaner_time = ticks
ps_time = ticks

prev_bl = tft.get_backlight()
is_in_saving = False

# Secret variables
eeg_click_entry = 0

# IMU Rotations cheat sheet
# 0 - button side down
# 1 - button side right
# 2 - button side up
# 3 - button side left

# IMU/rotation variables
imu_delay = ticks
last_orientation = None
orientation_start_time = 0
stable_orientation = osc.LCD_ROTATIONS["BUTTON_LEFT"]

current_rotation = osc.LCD_ROTATIONS["BUTTON_LEFT"]

# Force landscape function
def allow_only_landscape():
    if stable_orientation == osc.LCD_ROTATIONS["BUTTON_UPPER"] or stable_orientation == osc.LCD_ROTATIONS["BUTTON_BOTTOM"]:
        tft.rotation(osc.LCD_ROTATIONS["BUTTON_LEFT"])
    else:
        tft.rotation(int(stable_orientation))
        
# Clean up
render_bar(l_get("mainos_load.cleaning_up"), True) # Cleaning up...
debug.log("Cleaning up...")
debug.log("Before: " + str(gc.mem_free() / 1024 / 1024) + "MB")
del n_boot
gc.collect()
debug.log("After: " + str(gc.mem_free() / 1024 / 1024) + "MB")

# Log max loading count
debug.log("Loading count: " + str(loading_count))

# Init SD Card
render_bar(l_get("mainos_load.sd_init"), True) # SD Init
if osc.HAS_SD_SLOT or nvs.get_int(n_settings, "sd_overwrite") == 1:
    import modules.sdcard as sdcard
    if nvs.get_int(n_settings, "sd_overwrite") == 1 and nvs.get_int(n_settings, "sd_automount") == 1:
        cs = nvs.get_int(n_settings, "sd_cs")
        if cs == 99:
            cs = None
        sdcard.init(2, nvs.get_int(n_settings, "sd_clk"), cs, nvs.get_int(n_settings, "sd_miso"), nvs.get_int(n_settings, "sd_mosi"))
    else:
        sdcard.init(2, osc.SD_CLK, osc.SD_CS, osc.SD_MISO, osc.SD_MOSI)
    sdcard.mount()

# Load clock
render_bar(l_get("mainos_load.load_clock"), True) # Loading clock...
import apps.clock as app_clock

# Wake up function
def wake_up():
    global is_in_saving, pwr_save_time, prev_bl, stable_orientation
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
    ps.set_freq(osc.BASE_FREQ)

was_sleep_triggered = False

# Slow down CPU
ps.set_freq(osc.BASE_FREQ)

# Print sys.modules
import sys
debug.log(str(sys.modules))

# Show quick start guide if not shown yet
if nvs.get_int(n_guides, 'quick_start') == None:
    import helpers.run_in_reader as rir
    rir.open_file(f'/guides/quick_start_{cache.get('n_cache_lang')}.txt')
    nvs.set_int(n_guides, 'quick_start', 1)
    
# Show account popup if not shown yet and account is not logged in
allow_account_popup = False
if nvs.get_int(n_guides, 'account_popup') == None and nvs.get_int(n_wifi, 'account_logged_in') != 1 and allow_account_popup:
    import apps.popups.account_popup as account_popup
    account_popup.run()
    nvs.set_int(n_guides, 'account_popup', 1)

# Main loop
while True:

    # Set CPU frequencies depending on power saving state
    if is_in_saving == False:
        ps.set_freq(osc.BASE_FREQ)
    else:
        ps.set_freq(osc.SLOW_FREQ)

    # Disallow boosting
    ps.boost_allowing_state(False)
    
    # Render clock text
    if menu == 0 and menu_change == False:
        app_clock.clock()
    # Render clock text vertically
    elif menu == 1 and menu_change == False:
        app_clock.clock_vert()
    # Render entire clock
    elif menu_change == True:
        # Allow boosts for a while
        ps.boost_allowing_state(True)

        # Reset eastereggs on render
        egg_click_entry = 0

        # Change bitmap cache to none so battery bitmap renders after render clock
        b_check.last_bitmap = None

        if was_sleep_triggered:
            tft.set_backlight(prev_bl)
            was_sleep_triggered = False

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
    
    # Wifi power saver
    #if time.ticks_diff(time.ticks_ms(), wifi_master_dynamic) >= osc.WIFI_PWR_SAVER_TIME:
    #    wifi_master.dynamic_pwr_save()
    #    wifi_master_dynamic = time.ticks_ms()

    # Power saver loop
    if time.ticks_diff(time.ticks_ms(), ps_time) >= osc.POWER_SAVER_TIME:
        ps.loop()
        ps_time = time.ticks_ms()

    # Power saving
    if not is_in_saving and time.ticks_diff(time.ticks_ms(), pwr_save_time) >= osc.POWER_SAVE_TIMEOUT and allow_saving == 1:
        # Disable debug/battery info for less lag
        tft.fill_rect(4, 116, 190, 16, 0) # Info text
        tft.text(f8x8, "    ", 200, 5, 2027) # Battery percentage
        
        # Change bitmap cache to none so battery bitmap renders after wake up
        b_check.last_bitmap = None
        
        is_in_saving = True
        tft.set_backlight(osc.LCD_POWER_SAVE_BL)
        auto_rotate = 0
        stable_orientation = osc.LCD_ROTATIONS["BUTTON_LEFT"]
        if osc.HAS_IMU:
            mpu.sleep_on()
        was_sleep_triggered = True
        ps.set_freq(osc.SLOW_FREQ)
    
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

    # Detect spam (Very secret!!!)
    if clicker != None:
        if clicker.value() == 0:
            while clicker.value() == 0:
                time.sleep(osc.DEBOUNCE_TIME)
            eeg_click_entry += 1
            if eeg_click_entry >= 25:
                menu_change = True
                eeg_click_entry = 0
                import apps.eastereggs as eggs
                eggs.trigger(2)
                
    # Load button states to not double poll them
    btn_a_state = button_a.value()
    btn_b_state = button_b.value()
    btn_c_state = button_c.value()
            
    # Dummy mode unlocking
    if btn_a_state == 0 and btn_b_state == 0:
        hold_time = 0.00
        
        # Wake up (If in power saving)
        wake_up()
        
        # Check how much time button b is held down
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
    if btn_a_state == 0:
        # Wake up (If in power saving)
        wake_up()
        
        # Set basic frequency
        ps.set_freq(osc.BASE_FREQ)
        
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
                tft.text(f16x32, l_get("crashes.app_crashed_oops"),0,0,17608) # Oops!
                tft.text(f8x8, l_get("crashes.app_crashed_info"),0,32,65535) # One of your apps has crashed!
                tft.text(f8x8, l_get("crashes.app_crashed_try_again"),0,40,65535) # Please try again!
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
    if btn_c_state == 0:
        # Wake up
        wake_up()
        
        # Check buttons
        while button_c.value() == 0 and button_a.value() == 1 and button_b.value() == 1:
            time.sleep(osc.LOOP_WAIT_TIME)
        if button_a.value() == 0 or button_b.value() == 0:
            continue
        
        try:                
            try:
                # Open power menu
                import apps.power_menu as app_powermen
                allow_only_landscape()
                if nvs.get_int(n_locks, 'dummy') != 0:
                    app_powermen.power_menu()
                else:
                    app_powermen.run()
            except Exception as e:
                tft.fill(0)
                gc.collect()
                tft.text(f16x32, l_get("crashes.app_crashed_oops"),0,0,17608) # Oops!
                tft.text(f8x8, l_get("crashes.app_crashed_info"),0,32,65535) # One of your apps has crashed!
                tft.text(f8x8, l_get("crashes.app_crashed_try_again"),0,40,65535) # Please try again!
                print(str(e))
                time.sleep(3)
                
            # De-cache
            decache("apps.power_menu")
            del app_powermen
            menu = 0
            menu_change = True
            
            # Reset power saving time
            pwr_save_time = time.ticks_ms()

            # Clean ram
            ram_cleaner.clean()
        except Exception as e:
                tft.fill(0)
                gc.collect()
                tft.text(f16x32, l_get("crashes.app_crashed_oops"),0,0,17608) # Oops!
                tft.text(f8x8, l_get("crashes.app_crashed_info"),0,32,65535) # One of your apps has crashed!
                tft.text(f8x8, l_get("crashes.app_crashed_try_again"),0,40,65535) # Please try again!
                print(str(e))
                time.sleep(3)

    # Locking menu / Clock menu
    if btn_b_state == 0:
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
        if hold_time >= 1 and hold_time <= 9.99 and nvs.get_int(n_locks, "dummy") == 0:
            allow_only_landscape()
            # Open lock menu
            import apps.lock_menu as app_lockmen
            app_lockmen.run()
            # De-cache lock menu
            decache("apps.lockmen")
            del app_lockmen
            menu = 0
            menu_change = True
        # Easteregg if more than 10s (VERY SECRET!!!)
        elif nvs.get_int(n_locks, "dummy") == 0 and hold_time >= 9.99:
            allow_only_landscape()
            import apps.eastereggs as eggs
            eggs.trigger(1)
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

    # Ram cleaner
    if time.ticks_diff(time.ticks_ms(), cleaner_time) >= osc.RAM_CLEANER_TIME:
        ram_cleaner.clean()
        cleaner_time = time.ticks_ms()
            
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
            
            if locks == 0:
                tft.text(f8x8, l_get("mainos_diagnostics.battery") + ": " + str(volts) + "V",4,124,2016)
                
        # Battery bitmap render
        b_check.run(tft)
        
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
                    
    # RGB Handler
    if osc.HAS_NEOPIXEL:
        np_anims.automatic()
                    
    time.sleep(osc.LOOP_WAIT_TIME)