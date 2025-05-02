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
    import fonts.def_8x8 as f8x8
    import machine
    
    machine.freq(240000000)
    tft.text(f8x8, "Please wait for the render!",0,0,2022)
    del f8x8
    
    render = menus.menu("Menu/Others", [("Scorekeeper", 1), ("Resistor decoder", 2), ("Close", 13)])
    if render == 1:
        import apps.scorekeeper as a_sc
        a_sc.set_btf(button_a, button_b, button_c, tft)
        a_sc.run()
        machine.freq(240000000)
    elif render == 2:
        import apps.resistors as a_re
        a_re.set_btf(button_a, button_b, button_c, tft)
        a_re.run()
        machine.freq(240000000)