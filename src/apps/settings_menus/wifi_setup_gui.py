"""
Wifi setup wizard
"""

import time

import network

import fonts.def_8x8 as f8x8
import modules.cache as cache
import modules.io_manager as io_man
import modules.menus as menus
import modules.nvs as nvs
import modules.popup as popup
import modules.printer as printer
import modules.wifi_master as wifi_man
from modules.translate import get as l_get


def run():
    tft = io_man.get("tft")
    n_wifi = cache.get_nvs("wifi")
    
    # Reset Wi-Fi to ensure that it works
    tft.text(f8x8, l_get("apps.settings.wifi.scanning"), 0,0, 65535)
    nic = network.WLAN(network.STA_IF)
    wifi_man.nic_reset()
    #wifi_man.set_pwr_modes(0)
    
    # Scan for Access points
    nic_scan = nic.scan()
    if nic_scan == []:
        attempts = 5
        while attempts != 0 and nic_scan == []:
            nic_scan = nic.scan()
            wifi_man.nic_reset()
            attempts -= 1
            
        # If no AP found in 5 attempts, show popup
        # Why does ESP doesn't detect any AP sometimes? It just crashes wifi module, you need to reset your ESP.
        # I don't know if this is by me, or maybe micropython, or even espressif fault, but it seems unfixable once it crashes.
        # Thats also the reason why i had to remove the wifi power saving functions in wifi_master (better known as wifi_man).
        if nic_scan == []:
            popup.show(l_get("apps.settings.wifi.no_ap_error_popup"), l_get("crashes.error"), 10)
            return
    
    # Show AP list
    wlan_scan = []
    index = 0
    for ap in nic_scan:
        ap_name = ap[0].decode()
        if ap_name != '' and ap_name is not None and not ap[5]:
            wlan_scan.append((ap_name, index))
        index += 1
    wlan_scan.append((l_get("menus.menu_close"), None))
    num = menus.menu(l_get("apps.settings.wifi.select_ssid"), wlan_scan)
    if num is None:
        return

    # Check if AP is unsecured, if it isn't ask for password
    ssid = nic_scan[num][0].decode()
    if nic_scan[num][4] != 0:
        import modules.numpad as keypad
        password = str(keypad.keyboard(l_get("apps.settings.wifi.enter_passwd"), maxlen=63, hideInput=False))
        if password is None:
            return
    else:
        password = ""
        
    # Ask for autoconnect input
    autoconnect = menus.menu(l_get("apps.settings.wifi.auto_connect_ask"),
                                [(l_get("menus.yes"), 1),
                                (l_get("menus.no"), 0)])
    if autoconnect is None:
        autoconnect = 0
    tft.fill(0)
    tft.text(f8x8, l_get("apps.settings.wifi.connecting"), 0,0, 65535)
    tft.text(f8x8, ssid, 0,8, 65535)
    #wifi_man.set_pwr_modes()
    
    # Connect to see if wifi credentials are OK
    printer.log("Wifi connecting")
    if password != "":
        nic.connect(ssid, password)
    else:
        nic.connect(ssid)

    # Wait for status
    start_time = time.ticks_ms()
    while not nic.isconnected() and time.ticks_diff(time.ticks_ms(), start_time) < 10000:
        time.sleep(0.2)

    # Show status
    if nic.isconnected():
        # Set NVS
        nvs.set_float(n_wifi, "conf", 1.0)
        nvs.set_int(n_wifi, "autoConnect", autoconnect)
        nvs.set_string(n_wifi, "ssid", ssid)
        nvs.set_string(n_wifi, "passwd", password)
        popup.show(l_get("apps.settings.wifi.connected_to") + ": " + ssid, "Info", 10)
    elif nic.status() == network.STAT_WRONG_PASSWORD:
        popup.show(l_get("apps.settings.wifi.wrong_passwd"), l_get("crashes.error"), 10)
    elif nic.status() == network.STAT_NO_AP_FOUND:
        popup.show(l_get("apps.settings.wifi.ap_not_found"), l_get("crashes.error"), 10)
    else:
        popup.show(l_get("apps.settings.wifi.could_not_conn_popup"), l_get("crashes.error"), 10)