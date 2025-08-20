import time
import network

import modules.menus as menus
import modules.nvs as nvs
import modules.os_constants as osc
import modules.io_manager as io_man
import modules.cache as cache
import modules.popup as popup

n_settings = cache.get_nvs('settings')

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

t_index_ttl = 0 # Time to live of NVS cache, make sure its 0 so timezone is right first time clock appears
t_ttl_new = 50 # New ttl when cache expired
def get_time_timezoned(bypass_cache=False):
    global t_index_ttl
    timezoneIndex_cached = cache.get("timezone_index")
    timezoneIndex = 0
    if t_index_ttl <= 0 or bypass_cache:
        timezoneIndex = nvs.get_int(n_settings, "timezoneIndex")
        if timezoneIndex is None:
            timezoneIndex = 0
        cache.set("timezone_index", timezoneIndex)
        t_index_ttl = t_ttl_new
    else:
        if timezoneIndex_cached != None:
            timezoneIndex = timezoneIndex_cached

    current_time = time.localtime()
    
    offset = timezone_map.get(timezoneIndex, (0,0))
    hour_offset, min_offset = offset

    offset_sec = hour_offset * 3600 + min_offset * 60
    utc_timestamp = time.mktime(current_time)
    local_timestamp = utc_timestamp + offset_sec
    local_time = time.localtime(local_timestamp)
    t_index_ttl -= 1
    return local_time

def wait_for_new_second():
    now = time.localtime()
    current_sec = now[5]
    while time.localtime()[5] == current_sec:
        time.sleep(0.01)

def sync(): 
    import ntptime # Add the import here cause ram cleaner will delete it


    rtc = io_man.get('rtc')
    
    timezoneIndex = nvs.get_int(n_settings, "timezoneIndex")

    if timezoneIndex is None:
        timezoneIndex = 0
    try:
        ntptime.host = "time.google.com"
        ntptime.settime()
    except Exception as e:
        print("NTP sync failed")
        print(str(e))
        return False

    wait_for_new_second()

    utc = time.localtime()
    
    if osc.HAS_RTC == True:
        rtc.set_time((utc[0], utc[1], utc[2], utc[6], utc[3], utc[4], utc[5], 0))
    return True

def sync_interactive():
    nic = network.WLAN(network.STA_IF)
    if nic.isconnected() == True:
        syncing = True
        while syncing == True:
            syn = sync()
            if syn == True:
                popup.show("NTP Sync successfull!", "Info", 10)
                syncing = False
            elif syn == False:
                rend = menus.menu("NTP Sync failed :(", [("Retry?",  1), ("OK",  2)])
                if rend == 2:
                    syncing = False
    else:
        popup.show("No Wi-Fi connection, please connect.", "Error", 10)

def wrong_time_support():
    # ESP's usually have default time set to 2000 something, 
    # check if its greater than the time im programming this.
    localtime = time.localtime()
    min_time = (2025, 8,8) # My cats birthday
    if localtime[0] < min_time[0] and localtime[1] < min_time[1] and localtime[2] < min_time[2] and osc.HAS_RTC == True:
        import modules.menus as menus
        popup.show("Time set in your device is incorrect but external RTC was detected! Please sync through settings!", "Info", 30)