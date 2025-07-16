import gc
import time
import modules.crash_handler as c_handler

# System supervisor messages
# 0 - All good
# 1 - Memory critical, clean it up

# App replies
# 1 - Fixed
# 3 - Critical process in progress

supervisor_warn = False
supervisor_msg = 0
supervisor_time = None
supervisor_timeout = 15000

def ram_check():
    gc.collect()
    memfree = gc.mem_free() / 1024 / 1024
    if memfree <= 0.2:
        print("[SysSupervisor] Memory too low!!! Closing the app!!!")
        supervisor_warn = True
        supervisor_msg = 1
        supervisor_time = time.ticks_ms()
        return True
    return False

def check_time():
    if time.ticks_diff(time.ticks_ms(), supervisor_time) >= supervisor_timeout:
        return True
    return False

def loop():
    # Check for warnings
    if supervisor_warn == True:
        if supervisor_msg == 1:
            if check_time():
                c_handler.crash_screen(tft, 4001, "Warning from supervisor has not been handled by the app properly!", True, True, 2)
    
    if ram_check():
        return 1
    
    return 0
    
def app_respond(msg):
    if msg == 1:
        if supervisor_warn == True:
            if supervisor_msg == 1:
                if ram_check():
                    return 1
                else:
                    supervisor_warn = False
                    return 0
