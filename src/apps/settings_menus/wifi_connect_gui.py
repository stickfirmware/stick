"""
Wifi connection for settings
"""

import time

import network

import fonts.def_8x8 as f8x8
import modules.cache as cache
import modules.crash_handler as c_handler
import modules.io_manager as io_man
import modules.menus as menus
import modules.nvs as nvs
import modules.popup as popup
import modules.printer as printer
import modules.wifi_master as wifi_man
from modules.translate import get as l_get


def run():
    n_wifi = cache.get_nvs("wifi")
    tft = io_man.get('tft')
    
    # TODO: Refactor this thing, make it work better
    if int(nvs.get_float(n_wifi, "conf")) == 1.0:
        try:
            nic = wifi_man.nic
            if not nic.isconnected():
                rend = menus.menu(l_get("apps.settings.wifi.connect_with") + nvs.get_string(n_wifi, "ssid") + "?", 
                                    [(l_get("menus.yes"),  1),
                                    (l_get("menus.no"),  2)])
                if rend == 1:
                    ssid = nvs.set_string(n_wifi, "ssid")
                    password = nvs.set_string(n_wifi, "passwd")
                                                    
                    wifi_man.nic_reset()
                    #wifi_man.set_pwr_modes(0)
                    tft.fill(0)
                    tft.text(f8x8, l_get("apps.settings.wifi.connecting"), 0,0, 65535)
                    tft.text(f8x8, ssid, 0,8, 65535)
                    
                    printer.log("Wifi connecting")
                    if password != "":
                        nic.connect(ssid, password)
                    else:
                        nic.connect(ssid)

                    start_time = time.ticks_ms()
                    while not nic.isconnected() and time.ticks_diff(time.ticks_ms(), start_time) < 10000:
                        time.sleep(0.2)

                    if nic.isconnected():
                        popup.show(l_get("apps.settings.wifi.connected_to") + ": " + ssid, "Info", 10)
                    elif nic.status() == network.STAT_WRONG_PASSWORD:
                        popup.show(l_get("apps.settings.wifi.wrong_passwd"), l_get("crashes.error"), 10)
                    elif nic.status() == network.STAT_NO_AP_FOUND:
                        popup.show(l_get("apps.settings.wifi.ap_not_found"), l_get("crashes.error"), 10)
                    else:
                        popup.show(l_get("apps.settings.wifi.could_not_conn_popup"), l_get("crashes.error"), 10)
            else:
                rend = menus.menu(l_get("apps.settings.wifi.connected_disconnect"),
                                    [(l_get("menus.yes"),  1),
                                    (l_get("menus.no"),  2)])
                if rend == 1:
                    nic.disconnect()
        except Exception as e:
            c_handler.crash_screen(tft, 3001, str(e), True, True, 2)
    else:
        popup.show(l_get("apps.settings.wifi.not_setup"), l_get("crashes.error"), 10)