button_a = None
button_b = None
button_c = None
tft = None
rtc = None

def set_btf(bta, btb, btc, ttft, rtcc):
    global button_a
    global button_b
    global button_c
    global tft
    global rtc
    
    rtc = rtcc
    button_a = bta
    button_b = btb
    button_c = btc
    tft = ttft

def run():
    import modules.menus as menus
    import modules.nvs as nvs
    import esp32
    import machine
    import gc
    
    machine.freq(240000000)
    menu1 = menus.menu("Menu", [("IR Remote", 1), ("Settings", 3), ("Others", 4), ("Close", 13)]) # , ("Unit modules", 2)
    if menu1 == 2:
        import apps.unit as a_un
        a_un.set_btf(button_a, button_b, button_c, tft)
        a_un.run()
        del a_un
    elif menu1 == 3:
        import apps.settings as a_se
        a_se.set_btf(button_a, button_b, button_c, tft, rtc)
        a_se.run()
        del a_se
    elif menu1 == 4:
        import apps.others as a_ot
        a_ot.set_btf(button_a, button_b, button_c, tft)
        a_ot.run()
        del a_ot
    elif menu1 == 1:
        import apps.IR as a_ir
        a_ir.set_btf(button_a, button_b, button_c, tft)
        a_ir.run()
        del a_ir
    gc.collect()
    machine.freq(80000000)