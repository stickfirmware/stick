import gc
import os
import time

import esp32
import machine

import fonts.def_8x8 as f8x8
import modules.error_db as error_db
import modules.nvs as nvs
import modules.os_constants as osc
import modules.text_utils as t_utils

n_crash = esp32.NVS("crash")

def log_to_file(data):
    # Create folders
    if "temp" not in os.listdir():
        os.mkdir("temp")
    if "logs" not in os.listdir("/temp/"):
        os.mkdir("/temp/logs")

    # Format filename
    filename = "temp/logs/crash_{}.log".format(time.ticks_ms())

    # Write logs
    with open(filename, "w") as f:
        f.write(data)

    print("Crash log saved to", filename)
    return filename

def test_tft(tft):
    # Test tft to check if we can enable it
    print("Testing TFT, may take a while, expect artifacts.")
    
    if tft is None:
        return False
    
    try:
        for i in range(osc.LCD_HEIGHT // 8):
            tft.text(f8x8, "Testing tft...", 0, (i * 8), 65535)
        tft.fill(0)
        tft.fill(2137)
        return True
    except Exception:
        return False

def crash_screen(tft, error_code: int, log_message: any, log_error: bool = True, enable_tft: bool = True, reboot_method: int = 1):
    """
    Show critical error screen
    
    Args:
        tft: Instance of ST7789 screen
        error_code (int): Error code, to get display name from error_db
        log_message (any): Error message, logged to file (if enabled)
        log_error (bool, optional): True to enable logging to file (Default)
        enable_tft (bool, optional): True to show Graphical BSOD to user (Default)
        reboot_method (int, optional): 1 - Soft reboot (Default), 2 - Hard reboot
    """
    print("Showing crash screen")
    
    # Test tft for errors
    if enable_tft:
        enable_tft = test_tft(tft)
    
    # If tft enabled show crash error
    if enable_tft:
        gc.collect()
        print("Showing text")
        text = "It seems like your"
        tft.text(f8x8, text, t_utils.center_x(text, 8), 50, 65535, 2137)
        text = "device has crashed!"
        tft.text(f8x8, text, t_utils.center_x(text, 8), 58, 65535, 2137)
    
    if log_error:
        print("NVS error logging turned on!")
        
        # Show info for collecting logs
        if enable_tft:
            print("Showing text")
            text = "Collecting logs..."
            tft.text(f8x8, text, t_utils.center_x(text, 8), 70, 65535, 2137)
            
        # Increase crash count and log error code
        print("Log error code to NVS and Flash")
        nvs.set_int(n_crash, "latest", error_code)
        print("Increase crash count")
        count = nvs.get_int(n_crash, "crashCount")
        if count is not None:
            nvs.set_int(n_crash, "crashCount", (count + 1))
            count = count + 1
        else:
            nvs.set_int(n_crash, "crashCount", 1)
            count = 1

        # Log file
        rtc = machine.RTC()
        y, m, d, wd, h, mi, s, _ = rtc.datetime()
        try:
            stat = os.statvfs("/")
            free_flash = stat[0] * stat[3]
            log_file = log_to_file("Stick Firmware Crash Handler\nCrash on " 
                                   + str(d) + "." + str(m) + "." + str(y) + " " + str(h) + ":" + str(mi) + ":" + str(s) 
                                   + "\nError code: " + str(error_code) + "(" + error_db.check_code(error_code) 
                                   + ")\nCrash count: " + str(count) 
                                   + "\nDevice info:\nMCU Frequency: " + str(machine.freq() / 1000 / 1000) 
                                   + "MHz\nAvailable RAM (During logging): "+ str(gc.mem_free() / 1024) 
                                   + "KB\nAvailable flash space: " + str(free_flash / 1024) + "KB\nSystem name: " + os.uname()[0] 
                                   + "\nMicroPython version: " + os.uname()[3] 
                                   + "\nMachine name: " + os.uname()[4]
                                   +"\n\nError message:\n" + str(log_message))
            nvs.set_string(n_crash, "latestPath", log_file)
            print("Log saved")
        except Exception as e:
            print("Could not save log\n" + str(e))
            nvs.set_string(n_crash, "latestPath", "Couldn't save log")
        print("Crash count: " + str(count))
    else:
        print("NVS error logging disabled")
        
    # Reboot
    method = ""
    if reboot_method == 1:
        method = "soft"
    elif reboot_method == 2:
        method = "hard"
    else:
        method = "soft"
        
    # Show reboot text
    if enable_tft:
        print("Showing text")
        text = "Your device will"
        tft.text(f8x8, text, t_utils.center_x(text, 8), 90, 65535, 2137)
        text = "be rebooted!"
        tft.text(f8x8, text, t_utils.center_x(text, 8), 98, 65535, 2137)
        import modules.error_db as edb
        text = edb.check_code(error_code)
        tft.text(f8x8, text, t_utils.center_x(text, 8), 110, 65535, 2137)
        text = "Reboot method: " + method
        tft.text(f8x8, text, t_utils.center_x(text, 8), 120, 65535, 2137)
    
    print("Waiting before reboot")
    time.sleep(5)
    print("Clear display")
    tft.fill(0)
    print("Reboot method: " + method)
    print("Rebooting, bye!")
    if reboot_method == 1:
        machine.soft_reset()
    elif reboot_method == 2:
        machine.reset()
    else:
        machine.soft_reset()