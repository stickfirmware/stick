import network
import time
import esp32

from modules.printer import log
import modules.nvs as nvs

n_wifi = esp32.NVS("wifi")

nic = network.WLAN(network.STA_IF)

# Reset wifi
def nic_reset():
    nic.active(False)
    time.sleep(0.6)
    nic.active(True)
    time.sleep(0.5)

# Set pwr mode based on NVS
def set_pwr_modes(pm_mode=None):
    if pm_mode is None:
        pm_mode = nvs.get_int(n_wifi, "wifimode")
        tx_power = nvs.get_float(n_wifi, "txpower")
    else:
        nvs.set_int(n_wifi, "wifimode", pm_mode)
        tx_power = 20 - (pm_mode * 5)
        nvs.set_float(n_wifi, "txpower", tx_power)

    if pm_mode == 3:
        dynamic_pwr_save()
    else:
        nic.config(pm=pm_mode)
        if tx_power is not None:
            nic.config(txpower=tx_power)


# Dynamic power saving based on rssi (Change tx power and pm modes)
_LAST_MODE = 3
_MARGIN = 5

def dynamic_pwr_save():
    global _LAST_MODE
    if nvs.get_int(n_wifi, "wifimode") == 3:
        log('Started dynamic pwr save')
        if nic.isconnected():
            rssi = nic.status('rssi')
            log(rssi)
            if rssi < -75 - _MARGIN and _LAST_MODE != 0:
                log("Mode changed to 0")
                _LAST_MODE = 0
                nic.config(txpower=20)
                nic.config(pm=0)
            elif rssi < -60 - _MARGIN and _LAST_MODE != 1:
                log("Mode changed to 1")
                _LAST_MODE = 1
                nic.config(txpower=15)
                nic.config(pm=1)
            elif rssi > -60 + _MARGIN and _LAST_MODE != 2:
                log("Mode changed to 2")
                _LAST_MODE = 2
                nic.config(txpower=10)
                nic.config(pm=2)
        else:
            if nic.active() == True and nic.status() != network.STAT_CONNECTING:
                nic.active(False)