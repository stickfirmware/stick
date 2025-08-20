import machine
import time
import network

import fonts.def_8x8 as f8x8
import fonts.def_16x32 as f16x32

import modules.battery_check as battery_check
import modules.io_manager as io_man
import modules.menus as menus
import modules.os_constants as osc
import modules.text_utils as text_utils
import modules.printer as printer
import modules.powersaving as ps
import modules.ntp as ntp

tft = io_man.get('tft')

allow_drawing_battery = True

last_clock_text = ""
last_date_text = ""
last_mode = 0

nic = network.WLAN(network.STA_IF)

def run_clock():
    global last_clock_text, last_date_text, last_mode
    printer.log("Rendering clock base")
    tft.fill_rect(0, 0, 240, 3, 65535)
    tft.fill_rect(0, 16, 240, 3, 65535)
    tft.fill_rect(0, 132, 240, 3, 65535)
    tft.fill_rect(0, 0, 3, 135, 65535)
    tft.fill_rect(237, 0, 3, 135, 65535)
    tft.fill_rect(3, 3, 234, 13, 0)
    tft.fill_rect(3, 19, 234, 113, 0)
    tft.text(f8x8, "Clock",5,5,65535)
    last_clock_text = ""
    last_date_text = ""
    last_mode = 0
    
def run_clock_vert():
    global last_clock_text, last_date_text, last_mode
    printer.log("Rendering clock base")
    tft.fill_rect(0, 0, 3, 240, 65535)
    tft.fill_rect(132, 0, 3, 240, 65535)
    tft.fill_rect(0, 0, 135, 3, 65535)
    tft.fill_rect(0, 16, 135, 3, 65535)
    tft.fill_rect(0, 237, 135, 3, 65535)
    tft.fill_rect(3, 3, 129, 13, 0)
    tft.fill_rect(3, 19, 129, 218, 0)
    tft.text(f8x8, "Clock",5,5,65535)
    last_clock_text = ""
    last_date_text = ""
    last_mode = 0
    
def clock_vert(): 
    global last_clock_text, last_date_text, last_mode
    time_tuple = ntp.get_time_timezoned()
    
    # Time
    hh = time_tuple[3]
    mm = time_tuple[4]
    ss = time_tuple[5]
    text = "{:02}:{:02}:{:02}".format(hh, mm, ss)
    if last_clock_text != text or last_mode != 1:
        x = text_utils.center_x(text, 16)
        tft.text(f16x32, text, x, 104, 65535)
        last_clock_text = text
    # Date
    text = "{:02d}.{:02d}.{:04d}".format(time_tuple[2], time_tuple[1], time_tuple[0])
    if last_date_text != text or last_mode != 1:
        x = text_utils.center_x(text, 8)
        tft.text(f8x8, text, x, 136, 65535)
        last_date_text = text
    last_mode = 1


def clock():
    global last_clock_text, last_date_text, last_mode
    time_tuple = ntp.get_time_timezoned()

    if nic.isconnected() == True:
        tft.text(f8x8, "Wi-Fi",50,5,703)
    else:
        tft.text(f8x8, "     ",50,5,703)
    
    # Time
    hh = time_tuple[3]
    mm = time_tuple[4]
    ss = time_tuple[5]
    text = "{:02}:{:02}:{:02}".format(hh, mm, ss)
    if last_clock_text != text or last_mode != 0:
        x = text_utils.center_x(text, 16)
        tft.text(f16x32, text, x, 60, 65535)
        last_clock_text = text
    
    # Date
    text = "{:02d}.{:02d}.{:04d}".format(time_tuple[2], time_tuple[1], time_tuple[0])
    if last_date_text != text or last_mode != 0:
        x = text_utils.center_x(text, 8)
        tft.text(f8x8, text, x, 93, 65535)
        last_date_text = text
    last_mode = 0
    
def format_ticks_ms(ticks):
    ms = ticks % 1000
    seconds_total = ticks // 1000
    s = seconds_total % 60
    minutes_total = seconds_total // 60
    m = minutes_total % 60
    h = minutes_total // 60
    return f"{h:02}:{m:02}:{s:02}:{ms:03}"
    
def stopwatch():
    button_a = io_man.get('button_a')
    while button_a.value() == 0:
        time.sleep(osc.DEBOUNCE_TIME)
    button_b = io_man.get('button_b')
    button_c = io_man.get('button_c')
    is_running = False
    was_paused = True
    working = True
    render_time = True
    pauses_total = 0
    time_from_battery_check = time.ticks_ms()
    start_offset = time.ticks_ms()
    time_from_pause = time.ticks_ms()
    paused_time = 0
    tft.fill(0)
    tft.text(f8x8, "Stopwatch", 0, 0, 65535)
    tft.text(f8x8, "Press A to start/pause", 0, 111, 65535)
    tft.text(f8x8, "Press B to reset", 0, 119, 65535)
    tft.text(f8x8, "Press C to exit", 0, 127, 65535)
    while working:
        time.sleep(osc.LOOP_WAIT_TIME)
        if is_running and was_paused:
            pauses_total += time.ticks_diff(time.ticks_ms(), time_from_pause)
            was_paused = False
        if is_running or render_time:
            render_time = False
            tft.text(f16x32, "                ", 0, 8, 0)
            elapsed = time.ticks_diff(time.ticks_ms(), start_offset) - pauses_total
            if elapsed < 0:
                elapsed = 0
            text = format_ticks_ms(elapsed)
            x = text_utils.center_x(16)
            y = text_utils.center_y(32)
            tft.text(f16x32, text, x, y, 65535)
            if time.ticks_diff(time.ticks_ms(), time_from_battery_check) >= 5000:
                volts = battery_check.voltage()
                pr = battery_check.percentage(volts)
                text = "Battery: " + str(volts) + "V / " + str(int(pr)) + "%"
                x = text_utils.center_x(text, 8)
                y = text_utils.center_y(8) + 32
                tft.text(f8x8, text,x,y,2016)
                time_from_battery_check = time.ticks_ms()
        if button_a.value() == 0:
            if not is_running:
                while button_a.value() == 0:
                    time.sleep(osc.DEBOUNCE_TIME)
                    ps.set_freq(osc.ULTRA_FREQ)
                tft.text(f8x8, "Stopwatch         ", 0, 0, 65535)
                is_running = True
            else:
                tft.text(f8x8, "Stopwatch [PAUSED]", 0, 0, 65535)
                time_from_pause = time.ticks_ms()
                is_running = False
                was_paused = True
                while button_a.value() == 0:
                    time.sleep(osc.DEBOUNCE_TIME)
                ps.set_freq(osc.SLOW_FREQ)
        if button_b.value() == 0:
            tft.text(f8x8, "Release to reset!", 0, 0, 65535)
            while button_b.value() == 0:
                time.sleep(osc.DEBOUNCE_TIME)
            pauses_total = 0
            start_offset = time.ticks_ms()
            time_from_pause = start_offset
            is_running = False
            was_paused = True
            render_time = True
            tft.text(f8x8, "Stopwatch [PAUSED]", 0, 0, 65535)

        if button_c.value() == 0:
            working = False
            while button_c.value() == 0:
                time.sleep(osc.DEBOUNCE_TIME)

def clock_menu():
    ps.set_freq(osc.BASE_FREQ)
    clock_menu = menus.menu("Clock", [("Stopwatch", 1),  ("NTP Sync", 3), ("Cancel", None)])
    if clock_menu == 1:
        stopwatch()
    elif clock_menu == 3:
        ntp.sync_interactive()