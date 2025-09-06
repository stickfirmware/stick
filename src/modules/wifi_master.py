import network
import time
import ubinascii

from modules.printer import log
import modules.nvs as nvs
import modules.cache as cache
import modules.crash_handler as c_handler
import modules.os_constants as osc

n_wifi = cache.get_nvs('settings')

nic = network.WLAN(network.STA_IF)

# Reset wifi
def nic_reset():
    """
    Resets Wi-Fi
    """
    
    nic.active(False)
    time.sleep(0.6)
    nic.active(True)
    time.sleep(0.5)

# Get mac address
def get_wifi_mac():
    """
    Get formatted Wi-Fi mac addr.

    Returns:
        str: Mac address (ex. AA:00:04:00:XX:YY)
    """
    return ubinascii.hexlify(nic.config('mac'), ':').decode()

# # Default NVS vars
# def set_defaults():
#     nvs.set_int(n_wifi, "wifimode", 3)
#     nvs.set_int(n_wifi, "txpower", 15)


# Dynamic power saving based on rssi (Change tx power and pm modes)
# Doesn't seem to work. ESP32 Wi-Fi stack just goes brrr
# _LAST_MODE = 0
# _MARGIN = 5

# def dynamic_pwr_save():
#     global _LAST_MODE
#     if nvs.get_int(n_wifi, "wifimode") != 3:
#         return

#     if not nic.isconnected():
#         if nic.active() and nic.status() != network.STAT_CONNECTING:
#             nic.active(False)
#             log("WiFi inactive, turning off")
#         return

#     rssi = nic.status('rssi')
#     log(f"RSSI: {rssi}")

#     if _LAST_MODE is None:
#         _LAST_MODE = 0

#     if rssi < (-75 - _MARGIN) and _LAST_MODE > 0:
#         _LAST_MODE -= 1
#         log(f"RSSI is falling down, change mode to {_LAST_MODE}")
#     elif rssi > (-60 + _MARGIN) and _LAST_MODE < 2:
#         _LAST_MODE += 1
#         log(f"RSSI is rising, changing mode to {_LAST_MODE}")

#     pm_map = {0: 0, 1: 1, 2: 2}
#     tx_map = {0: 20, 1: 15, 2: 10}

#     nic.config(pm=pm_map[_LAST_MODE], txpower=tx_map[_LAST_MODE])
#     log(f"PM Set to {pm_map[_LAST_MODE]}, txpower to {tx_map[_LAST_MODE]}")

def connect_main_loop():
    """
    Connect to Wi-Fi, mainos boot helper.
    """
    
    # Check Wi-Fi hostname
    if nvs.get_string(n_wifi, "hostname") == None:
        network.hostname(osc.WIFI_DEF_HOST)
    else:
        network.hostname(nvs.get_string(n_wifi, "hostname"))
        
    # Connect to Wi-Fi if its setup
    if nvs.get_float(n_wifi, "conf") == None:
        nvs.set_float(n_wifi, "conf", 0)
    if int(nvs.get_float(n_wifi, "conf")) == 1:
        if nvs.get_int(n_wifi, "autoConnect") == 1:
            log('Connecting to wifi!')
            try:
                log('Reset nic')
                nic_reset()
                log("Connect")
                ssid = nvs.get_string(n_wifi, "ssid")
                passwd = nvs.get_string(n_wifi, "passwd")
                if passwd != "":
                    nic.connect(ssid, passwd)
                else:
                    nic.connect(ssid)
            except Exception as e:
                import modules.io_manager as io_man
                tft = io_man.get('tft')
                c_handler.crash_screen(tft, 3001, str(e), True, True, 2)