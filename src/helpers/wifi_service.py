"""
Helper for Wi-Fi
"""

import modules.wifi_master as wifi_man

def connect():
    """
    Connect to Wi-Fi
    """
    return wifi_man.connect_main_loop()

def disconnect():
    """
    Disconnect from Wi-Fi
    """
    wifi_man.nic.disconnect()
    wifi_man.nic.active(False)
    
def is_connected():
    """
    Check if Wi-Fi is connected

    Returns:
        bool: True if connected, False otherwise.
    """
    return wifi_man.nic.isconnected()

def enable():
    """
    Enable Wi-Fi module (Resets whole Wi-Fi)
    """
    
    wifi_man.nic_reset()
    
def disable():
    """
    Disable Wi-Fi module
    """
    
    wifi_man.nic.active(False)