button_a = None
button_b = None
button_c = None
tft = None

def set_btf(bta, btb, btc, ttft):
    global button_a
    global button_b
    global button_c
    global tft
    
    button_a = bta
    button_b = btb
    button_c = btc
    tft = ttft

def run():
    import modules.menus as menus
    import modules.nvs as nvs
    import esp32
    import machine
    
    machine.freq(240000000)
    
    render = menus.menu("Menu/Unit modules", [("Heart", 1), ("Close", 13)])
    if render == 1:
        import apps.heart as a_hr
        a_hr.set_btf(button_a, button_b, button_c, tft)
        a_hr.run()
        del a_hr
