"""
Clock GUI for settings
"""

import modules.cache as cache
import modules.menus as menus
import modules.ntp as ntp
import modules.nvs as nvs
from modules.translate import get as l_get


def run():
    """Clock settings GUI"""
    # TODO: Add clock manual date setting
    
    n_settings = cache.get_nvs("settings")
    
    while True:
        clock_menu = menus.menu(l_get("apps.clock.name"), [
            (l_get("apps.clock.ntp_sync"), 0),
            (l_get("apps.settings.wifi.timezone"), 1),
            (l_get("menus.menu_close"), None)
        ])
        
        # NTP Sync
        if clock_menu == 0:
            ntp.sync_interactive()
                
        # NTP Timezone
        elif clock_menu == 1:
            tim = True
            menu = 1
            while tim:
                if menu == 1:
                    timezone = menus.menu(l_get("apps.settings.wifi.timezone"), [
                        ("UTC+00:00", 0), ("UTC+01:00", 1), ("UTC+02:00", 2), ("UTC+03:00", 3),
                        ("UTC+03:30", 4), ("UTC+04:00", 5), ("UTC+04:30", 6), ("UTC+05:00", 7),
                        ("UTC+05:30", 8), ("UTC+05:45", 9), ("UTC+06:00", 10), ("UTC+06:30", 11),
                        ("UTC+07:00", 12), ("UTC+08:00", 13), ("UTC+08:45", 14),
                        ("UTC+09:00", 15), ("UTC+09:30", 16), ("UTC+10:00", 17), ("UTC+10:30", 18),
                        ("UTC+11:00", 19), ("UTC+12:00", 20), ("UTC+12:45", 21), ("UTC+13:00", 22),
                        ("UTC+14:00", 23), ("UTC-01:00", 24), ("UTC-02:00", 25),
                        ("UTC-03:00", 26), ("UTC-03:30", 27), ("UTC-04:00", 28), ("UTC-05:00", 29),
                        ("UTC-06:00", 30), ("UTC-07:00", 31), ("UTC-08:00", 32), ("UTC-09:00", 33),
                        ("UTC-10:00", 34), ("UTC-11:00", 35), ("UTC-12:00", 36)
                    ])
                    if timezone is None:
                        tim = False
                    else:
                        nvs.set_int(n_settings, "timezoneIndex", timezone)
                        tim = False
            ntp.get_time_timezoned(True)

        else:
            break