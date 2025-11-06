"""
Wifi status menu
"""

import time

import network

import fonts.def_8x8 as f8x8
import modules.button_combos as btn_combos
import modules.io_manager as io_man
import modules.os_constants as osc
import modules.wifi_master as wifi_man
from modules.translate import get as l_get


def run():
    tft = io_man.get('tft')
    
    nic = wifi_man.nic
    nic_active = nic.active()
    nic_ifconfig = nic.ifconfig()
    tft.fill(0)
    tft.text(f8x8, l_get("apps.settings.wifi.wlan_active") + str(nic_active),0,0, 65535)
    tft.text(f8x8, l_get("apps.settings.wifi.connected") + str(nic.isconnected()),0,8, 65535)
    if nic.isconnected():
        tft.text(f8x8, l_get("apps.settings.local_ip") + str(nic_ifconfig[0]),0,16, 65535)
        tft.text(f8x8, l_get("apps.settings.wifi.subnet") + str(nic_ifconfig[1]),0,24, 65535)
        tft.text(f8x8, l_get("apps.settings.wifi.gateway") + str(nic_ifconfig[2]),0,32, 65535)
        tft.text(f8x8, l_get("apps.settings.wifi.dns") + str(nic_ifconfig[3]),0,40, 65535)
        tft.text(f8x8, l_get("apps.settings.wifi.ssid") + nic.config('ssid'),0,48, 65535)
        tft.text(f8x8, l_get("apps.settings.wifi.channel") + str(nic.config('channel')),0,56, 65535)
        tft.text(f8x8, l_get("apps.settings.wifi.hostname") + network.hostname(),0,64, 65535)
    while not btn_combos.any_btn(["a", "b", "c"]):
        time.sleep(osc.DEBOUNCE_TIME)