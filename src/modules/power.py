"""
Unified power management module for Stick firmware
"""

import os
import time
import machine

import fonts.def_8x8 as f8x8
import modules.cache as cache
import modules.io_manager as io_man
import modules.nvs as nvs
import modules.os_constants as osc
import modules.popup as popup
import modules.sleep as m_sleep
import modules.wifi_master as wifi_man
from modules.translate import get as l_get

n_settings = cache.get_nvs("settings")

# HW
power_hold = io_man.get('power_hold')

def shutdown():
    """
    Shutdowns device
    """
    
    mode = nvs.get_int(n_settings, "shutdown_mode")
    tft = io_man.get('tft')
    
    if mode == 1:
        tft.fill(0)
        os.sync()
        if osc.HAS_HOLD_PIN:
            tft.text(f8x8, l_get("q_actions.powering_off"),0,0,65535,0)
            power_hold.value(0)
        else:
            # If doesn't have power hold, ask for switching power off
            popup.show(l_get("q_actions.you_can_now_switch"), l_get("popups.info"), 15)
            tft.fill(0)
            tft.text(f8x8, l_get("q_actions.to_sleep"), 0,0, 65535)
            time.sleep(3)
            
        deep_sleep() # Deepsleep so it doesn't draw power when something goes wrong
        
def light_sleep():
    """
    Puts ESP32 and other components to light sleep
    """
    
    m_sleep.sleep()
    
def deep_sleep():
    """
    Puts ESP32 and other components to deep sleep (Without RAM)
    """
    
    m_sleep.sleep(True)
    
def _REBOOT_ACTION():
    tft = io_man.get('tft')
    nic = wifi_man.nic
    
    nic.active(False)
    tft.fill(0)
    tft.text(f8x8, l_get("q_actions.rebooting"),0,0,65535,0)
    os.sync()
    time.sleep(0.05)
    
def soft_reboot():
    """
    Soft resets device
    """
    _REBOOT_ACTION()
    machine.soft_reset()

def reboot():
    """
    Reboots entire device
    """
    
    _REBOOT_ACTION()
    machine.reset()