import esp32
import time
import machine
import os
import gc

import fonts.def_8x8 as f8x8

import modules.nvs as nvs
import modules.text_utils as t_utils
import modules.error_db as error_db

n_crash = esp32.NVS("crash")

def log_to_file(data):
    if "temp" not in os.listdir():
        os.mkdir("temp")
    if "logs" not in os.listdir("/temp/"):
        os.mkdir("/temp/logs")

    filename = "temp/logs/crash_{}.log".format(time.ticks_ms())

    with open(filename, "w") as f:
        f.write(data)

    print("Crash log saved to", filename)
    return filename

def crash_screen(tft, error_code, log_message, log_error, enable_tft, reboot_method):
    print("Showing crash screen")
    if enable_tft:
        print("Clear display")
        tft.fill(7128)
        gc.collect()
        print("Showing text")
        text = "It seems like your"
        tft.text(f8x8, text, t_utils.center_x(text, 8), 50, 65535, 7128)
        text = "device has crashed!"
        tft.text(f8x8, text, t_utils.center_x(text, 8), 58, 65535, 7128)
    
    if log_error:
        print("NVS error logging turned on!")
        if enable_tft:
            print("Showing text")
            text = "Collecting logs..."
            tft.text(f8x8, text, t_utils.center_x(text, 8), 70, 65535, 7128)
            
        print("Log error code to NVS and Flash")
        nvs.set_int(n_crash, "latest", error_code)
        print("Increase crash count")
        count = nvs.get_int(n_crash, "crashCount")
        if count is not None:
            nvs.set_int(n_crash, "crashCount", (count + 1))
        else:
            nvs.set_int(n_crash, "crashCount", 1)
        # Check again, could be none so None + 1 = error (in log below)
        count = nvs.get_int(n_crash, "crashCount")
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
        
    method = ""
    if reboot_method == 1:
        method = "soft"
    elif reboot_method == 2:
        method = "hard"
    else:
        method = "soft"
        
    if enable_tft:
        print("Showing text")
        text = "Your device will"
        tft.text(f8x8, text, t_utils.center_x(text, 8), 90, 65535, 7128)
        text = "be rebooted!"
        tft.text(f8x8, text, t_utils.center_x(text, 8), 98, 65535, 7128)
        import modules.error_db as edb
        text = edb.check_code(error_code)
        tft.text(f8x8, text, t_utils.center_x(text, 8), 110, 65535, 7128)
        text = "Reboot method: " + method
        tft.text(f8x8, text, t_utils.center_x(text, 8), 120, 65535, 7128)
    
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