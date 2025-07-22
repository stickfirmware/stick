import ntptime
import machine
import time
import esp32
import modules.nvs as nvs
import modules.osconstants as osc

timezone_map = {
    0: (0, 0), 1: (1, 0), 2: (2, 0), 3: (3, 0),
    4: (3, 30), 5: (4, 0), 6: (4, 30), 7: (5, 0),
    8: (5, 30), 9: (5, 45), 10: (6, 0), 11: (6, 30),
    13: (7, 0), 14: (8, 0), 15: (8, 45), 16: (9, 0),
    17: (9, 30), 18: (10, 0), 19: (10, 30), 20: (11, 0),
    21: (12, 0), 22: (12, 45), 23: (13, 0),
    25: (14, 0), 26: (-1, 0), 27: (-2, 0), 28: (-3, 0),
    29: (-3, 30), 30: (-4, 0), 31: (-5, 0), 32: (-6, 0),
    33: (-7, 0), 34: (-8, 0), 35: (-9, 0),
    37: (-10, 0), 38: (-11, 0), 39: (-12, 0)
}

def wait_for_new_second():
    now = time.localtime()
    current_sec = now[5]
    while time.localtime()[5] == current_sec:
        time.sleep(0.01)

def sync(rtc):
    n_settings = esp32.NVS("settings")
    timezoneIndex = nvs.get_int(n_settings, "timezoneIndex")
    if timezoneIndex is None:
        timezoneIndex = 0
    try:
        ntptime.settime()
    except Exception as e:
        print("NTP sync failed")
        print(str(e))
        return False

    wait_for_new_second()

    current_time = time.localtime()
    
    offset = timezone_map.get(timezoneIndex, (0,0))
    hour_offset, min_offset = offset

    offset_sec = hour_offset * 3600 + min_offset * 60
    utc_timestamp = time.mktime(current_time)
    local_timestamp = utc_timestamp + offset_sec
    local_time = time.localtime(local_timestamp)
    
    if osc.HAS_RTC == True:
        rtc.set_time((local_time[0], local_time[1], local_time[2], local_time[6], local_time[3], local_time[4], local_time[5], 0))
        dt = rtc.get_time()
    return True
