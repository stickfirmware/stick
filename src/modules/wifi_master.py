import network
import time
import esp32
import ubinascii

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

# Get mac address
def get_wifi_mac():
    return ubinascii.hexlify(nic.config('mac'), ':').decode()

# Default NVS vars
def set_defaults():
    nvs.set_int(n_wifi, "wifimode", 3)
    nvs.set_int(n_wifi, "txpower", 15)

# Set pwr mode based on NVS
def set_pwr_modes(pmm=None):
    if pmm is None:
        pm_mode = nvs.get_int(n_wifi, "wifimode")
        tx_power = nvs.get_int(n_wifi, "txpower")
    else:
        nvs.set_int(n_wifi, "wifimode", pmm)
        pm_mode = pmm
        tx_power = 20 - (pmm * 5)
        nvs.set_int(n_wifi, "txpower", tx_power)
    
    if pm_mode is None:
        set_defaults()
        return set_pwr_modes(pmm)

    if pm_mode == 3:
        dynamic_pwr_save()
    else:
        if nic.active():
            nic.config(pm=pm_mode)
            if tx_power is not None:
                nic.config(txpower=tx_power)


# Dynamic power saving based on rssi (Change tx power and pm modes)
_LAST_MODE = 0
_MARGIN = 5

def dynamic_pwr_save():
    global _LAST_MODE
    if nvs.get_int(n_wifi, "wifimode") != 3:
        return

    if not nic.isconnected():
        if nic.active() and nic.status() != network.STAT_CONNECTING:
            nic.active(False)
            log("WiFi inactive, turning off")
        return

    rssi = nic.status('rssi')
    log(f"RSSI: {rssi}")

    if _LAST_MODE is None:
        _LAST_MODE = 0

    if rssi < (-75 - _MARGIN) and _LAST_MODE > 0:
        _LAST_MODE -= 1
        log(f"RSSI is falling down, change mode to {_LAST_MODE}")
    elif rssi > (-60 + _MARGIN) and _LAST_MODE < 2:
        _LAST_MODE += 1
        log(f"RSSI is rising, changing mode to {_LAST_MODE}")

    pm_map = {0: 0, 1: 1, 2: 2}
    tx_map = {0: 20, 1: 15, 2: 10}

    nic.config(pm=pm_map[_LAST_MODE], txpower=tx_map[_LAST_MODE])
    log(f"PM Set to {pm_map[_LAST_MODE]}, txpower to {tx_map[_LAST_MODE]}")
