import os
import machine
import network
import machine

import fonts.def_8x8 as f8x8

from modules.decache import decache
import modules.os_constants as osc
import modules.nvs as nvs
import modules.menus as menus
import modules.io_manager as io_man
import modules.sleep as m_sleep
import modules.powersaving as ps
import modules.cache as cache
from modules.translate import get as l_get
import modules.popup as popup

button_a = io_man.get('button_a')
button_b = io_man.get('button_b')
button_c = io_man.get('button_c')
tft = io_man.get('tft')
power_hold = io_man.get('power_hold')
mpu = io_man.get('imu')

def run():
    global button_c, button_a, button_b, tft
    button_a = io_man.get('button_a')
    button_b = io_man.get('button_b')
    button_c = io_man.get('button_c')
    tft = io_man.get('tft')

    q_actions = menus.menu(l_get("q_actions.quick_actions"),
                           [(l_get("q_actions.pwr_menu"), 1),
                            (l_get("apps.settings.name"), 2),
                            (l_get("menus.menu_close"), None)])
    if q_actions == 1:
        power_menu()
    elif q_actions == 2:
        import apps.settings as a_se
        a_se.run()
        del a_se
        decache('apps.settings')

def power_menu():
    nic = network.WLAN(network.STA_IF)
    powermenu = menus.menu(l_get("q_actions.power"), 
                           [(l_get("q_actions.sleep"), 1),
                            (l_get("q_actions.pwr_off"), 2),
                            (l_get("q_actions.reboot"), 3),
                            (l_get("menus.menu_close"), 4)])
    n_wifi = cache.get_nvs('wifi')
    if powermenu == 1:
        ps.set_freq(osc.BASE_FREQ)
        wasConnected = False
        if nic.isconnected() == True:
            nic.disconnect()
            wasConnected = True
        nic.active(False)
        os.sync()
        if mpu != None:
            mpu.sleep_on()
        m_sleep.sleep()
        if mpu != None:
            mpu.sleep_off()
        if wasConnected == True:
            nic.active(True)
            nic.connect(nvs.get_string(n_wifi, "ssid"), nvs.get_string(n_wifi, "passwd"))
    elif powermenu == 2:
        ps.set_freq(osc.BASE_FREQ)
        nic.active(False)
        tft.fill(0)
        if osc.HAS_HOLD_PIN:
            tft.text(f8x8, l_get("q_actions.powering_off"),0,0,65535,0)
        os.sync()
        if osc.HAS_HOLD_PIN:
            power_hold.value(0)
        else:
            # If doesn't have power hold, ask for switching power off
            while True:
                popup.show(l_get("q_actions.you_can_now_switch"), l_get("popups.info"))
        m_sleep.sleep()
    elif powermenu == 3:
        ps.set_freq(osc.BASE_FREQ)
        nic.active(False)
        tft.fill(0)
        tft.text(f8x8, l_get("q_actions.rebooting"),0,0,65535,0)
        os.sync()
        machine.reset()
    else:
        ps.set_freq(osc.BASE_FREQ)