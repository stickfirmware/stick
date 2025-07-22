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
    import modules.osconstants as osc
    import modules.nvs as nvs
    import esp32
    import machine
    import sys
    import gc
    
    def dechache(name):
        sys.modules.pop(name, None)
    
    machine.freq(osc.ULTRA_FREQ)
    menu1 = menus.menu("Menu", [("IR Remote", 1), ("Terminal (Needs CardKB)", 2), ("Music Player", 6), ("File explorer", 7), ("Others", 4), ("Settings", 3), ("Close", 13)])
    if menu1 == 3:
        import apps.settings as a_se
        a_se.set_btf(button_a, button_b, button_c, tft, rtc)
        a_se.run()
        del a_se
        dechache('apps.settings')
    elif menu1 == 4:
        import apps.others as a_ot
        a_ot.set_btf(button_a, button_b, button_c, tft)
        a_ot.run()
        del a_ot
        dechache('apps.others')
    elif menu1 == 1:
        import apps.IR as a_ir
        a_ir.set_btf(button_a, button_b, button_c, tft)
        a_ir.run()
        del a_ir
        dechache('apps.IR')
    elif menu1 == 2:
        import apps.terminal as a_tm
        a_tm.set_tft(tft)
        a_tm.run()
        del a_tm
        dechache('apps.terminal')
    elif menu1 == 6:
        if osc.HAS_BUZZER:
            import apps.player as a_pl
            a_pl.set_btf(button_a, button_b, button_c, tft)
            a_pl.run()
            del a_pl
            dechache('apps.player')
        else:
            menus.menu("You don't have buzzer!", [("OK", 1)])
    elif menu1 == 7:
        import modules.fileexplorer as a_fe
        a_fe.set_btf(button_a, button_b, button_c, tft)
        a_fe.run()
        del a_fe
        dechache('modules.fileexplorer')
    gc.collect()
    machine.freq(osc.BASE_FREQ)