button_a = None
button_b = None
button_c = None
tft = None
power_hold = None

def set_btf(bta, btb, btc, power_h, ttft):
    global button_a
    global button_b
    global button_c
    global tft
    global power_hold
    
    power_hold = power_h
    button_a = bta
    button_b = btb
    button_c = btc
    tft = ttft

def run():
    import modules.menus as menus
    import machine
    import modules.sleep as m_sleep
    powermenu = menus.menu("Power", [("Sleep", 1), ("Power off", 2), ("Reboot", 3), ("Cancel", 4)])
    if powermenu == 1:
        machine.freq(80000000)
        m_sleep.sleep(tft, button_c, True)
    elif powermenu == 2:
        machine.freq(80000000)
        power_hold.value(0)
    elif powermenu == 3:
        machine.freq(80000000)
        tft.text(f8x8, "Reseting...", 0,0,2016)
        machine.reset()
    else:
        machine.freq(80000000)