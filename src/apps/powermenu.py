button_a = None
button_b = None
button_c = None
tft = None
power_hold = None

from machine import Pin

def set_btf(bta, btb, btc, power_h, ttft):
    global button_a
    global button_b
    global button_c
    global tft
    global power_hold
    
    power_hold = Pin(4, Pin.OUT)
    button_a = bta
    button_b = btb
    button_c = btc
    tft = ttft

def run():
    import esp32
    import modules.nvs as nvs
    import modules.menus as menus
    import machine
    import modules.sleep as m_sleep
    import fonts.def_8x8 as f8x8
    import network
    nic = network.WLAN(network.STA_IF)
    powermenu = menus.menu("Power", [("Sleep", 1), ("Power off", 2), ("Reboot", 3), ("Cancel", 4)])
    n_wifi = esp32.NVS("wifi")
    if powermenu == 1:
        machine.freq(80000000)
        wasConnected = False
        if nic.isconnected() == True:
            nic.disconnect()
            wasConnected = True
        nic.active(False)
        m_sleep.sleep(tft, button_c, True)
        if wasConnected == True:
            nic.active(True)
            nic.connect(nvs.get_string(n_wifi, "ssid"), nvs.get_string(n_wifi, "passwd"))
    elif powermenu == 2:
        machine.freq(80000000)
        nic.active(False)
        tft.fill(703)
        tft.text(f8x8, "Powering off...",0,0,65535,703)
        tft.text(f8x8, "Please wait!",0,8,65535,703)
        power_hold.value(0)
    elif powermenu == 3:
        machine.freq(80000000)
        import fonts.def_8x8 as f8x8
        nic.active(False)
        tft.fill(703)
        tft.text(f8x8, "Rebooting...",0,0,65535,703)
        tft.text(f8x8, "Please wait!",0,8,65535,703)
        machine.reset()
    else:
        machine.freq(80000000)