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
    
    menu1 = menus.menu("Menu", [("IR Remote", 10), ("Others", 11), ("Close", 13)])
    if menu1 == 11:
        import apps.others as a_ot
        a_ot.set_btf(button_a, button_b, button_c, tft)
        a_ot.run()
        del a_ot
    elif menu1 == 10:
        import apps.IR as a_ir
        a_ir.set_btf(button_a, button_b, button_c, tft)
        a_ir.run()
        del a_ir
    machine.freq(80000000)