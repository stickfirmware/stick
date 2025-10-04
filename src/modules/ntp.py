"""
NTP sync module for Stick firmware, with timezones and automatic ntp sync.
"""

import time
import network

import modules.menus as menus
import modules.nvs as nvs
import modules.os_constants as osc
import modules.io_manager as io_man
import modules.cache as cache
import modules.popup as popup
from modules.translate import get as l_get

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

def get_time_timezoned(bypass_cache: bool = False):
    """
    Gets timezoned time, gets timezone from NVS (or cache)

    Args:
        bypass_cache (bool, optional): Bypasses NVS cache if True

    Returns:
        tuple: (year, month, mday, hour, minute, second, weekday, yearday)
            - year (int): year (ex. 2025)
            - month (int): month (1–12)
            - mday (int): day of the month (1–31)
            - hour (int): hour (0–23)
            - minute (int): minute (0–59)
            - second (int): second (0–59)
            - weekday (int): weekday (0 = monday, 6 = sunday)
            - yearday (int): year day (1–366)
    """
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
        if timezoneIndex_cached is not None:
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

def _WAIT_FOR_NEW_SECOND():
    now = time.localtime()
    current_sec = now[5]
    while time.localtime()[5] == current_sec:
        time.sleep(0.01)

def sync(host: str = "time.google.com") -> bool: 
    """
    Sync ntp time
    
    Args:
        host (str, optional): NTP server hostname, default is google ntp servers.

    Returns:
        bool: True if success, False if failed.
    """
    import ntptime # Add the import here cause ram cleaner will delete it


    rtc = io_man.get('rtc')
    
    timezoneIndex = nvs.get_int(n_settings, "timezoneIndex")

    if timezoneIndex is None:
        timezoneIndex = 0
    try:
        ntptime.host = host
        ntptime.settime()
    except Exception as e:
        print("NTP sync failed")
        print(str(e))
        return False

    _WAIT_FOR_NEW_SECOND()

    utc = time.localtime()
    
    if osc.HAS_RTC:
        rtc.set_time((utc[0], utc[1], utc[2], utc[6], utc[3], utc[4], utc[5], 0))
    return True

def sync_interactive(host: str = "time.google.com"):
    """
    Sync time with NTP with GUI

    Args:
        host (str, optional): NTP server hostname, default is google ntp servers.
    """
    nic = network.WLAN(network.STA_IF)
    if nic.isconnected():
        syncing = True
        while syncing:
            syn = sync(host)
            if syn:
                popup.show(l_get("ntp.success_popup"), l_get("popups.info"), 10)
                syncing = False
            elif not syn:
                rend = menus.menu(l_get("ntp.fail_popup"), 
                                  [(l_get("ntp.retry"),  1),
                                   (l_get("menus.ok"),  2)])
                if rend == 2:
                    syncing = False
    else:
        popup.show(l_get("ntp.no_wifi_popup"), l_get("crashes.error"), 10)

def wrong_time_support():
    """
    Checks if time is setup correctly on your device, if no it shows a popup.
    """
    
    # ESP's usually have default time set to 2000 something, 
    # check if its greater than the time im programming this.
    localtime = time.localtime()
    min_time = (2025, 8,8) # My cats birthday
    if localtime[0] < min_time[0] and localtime[1] < min_time[1] and localtime[2] < min_time[2] and osc.HAS_RTC:
        popup.show(l_get("ntp.time_incorrect_popup"), l_get("popups.info"), 30)