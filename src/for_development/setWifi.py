WIFI_SSID = ""
WIFI_PASSWD = ""
WIFI_AUTOCONN = 1

import esp32
import modules.nvs as nvs

n_wifi = esp32.NVS("wifi")
nvs.set_float(n_wifi, "conf", 1)
nvs.set_int(n_wifi, "autoConnect", WIFI_AUTOCONN)
nvs.set_string(n_wifi, "ssid", WIFI_SSID)
nvs.set_string(n_wifi, "passwd", WIFI_PASSWD)
print("Done")