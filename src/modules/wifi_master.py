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

def connect_main_loop():
    """
    Connect to Wi-Fi, mainos boot helper.
    """
    
    # Check Wi-Fi hostname
    if nvs.get_string(n_wifi, "hostname") is None:
        network.hostname(osc.WIFI_DEF_HOST)
    else:
        network.hostname(nvs.get_string(n_wifi, "hostname"))
        
    # Connect to Wi-Fi if its setup
    if nvs.get_float(n_wifi, "conf") is None:
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