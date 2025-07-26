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
    import modules.osconstants as osc
    import modules.menus as menus
    import modules.nvs as nvs
    import esp32
    import sys
    import machine
    import gc
    
    def dechache(name):
        sys.modules.pop(name, None)
    
    render = menus.menu("Menu/Others", [("PiMarkX", 5), ("Scorekeeper", 1), ("Resistor decoder", 2), ("Metronome", 3), ("Close", 13)])
    if render == 1:
        import apps.scorekeeper as a_sc
        a_sc.set_btf(button_a, button_b, button_c, tft)
        a_sc.run()
        del a_sc
        dechache('apps.scorekeeper')
    elif render == 2:
        import apps.resistors as a_re
        a_re.set_btf(button_a, button_b, button_c, tft)
        a_re.run()
        del a_re
        dechache('apps.resistors')
    elif render == 3:
        import apps.metronome as a_me
        a_me.set_btf(button_a, button_b, button_c, tft)
        a_me.run()
        del a_me
        dechache('apps.metronome')
    elif render == 5:
        import apps.pimarkx as a_pimark
        a_pimark.set_btf(button_a, button_b, button_c, tft)
        a_pimark.run()
        del a_pimark
        dechache('apps.pimarkx')
    gc.collect()
    machine.freq(osc.BASE_FREQ)