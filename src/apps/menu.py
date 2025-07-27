import modules.io_manager as io_man

button_a = io_man.get_btn_a()
button_b = io_man.get_btn_b()
button_c = io_man.get_btn_c()
tft = io_man.get_tft()

def run():
    global button_c, button_a, button_b, tft
    button_a = io_man.get_btn_a()
    button_b = io_man.get_btn_b()
    button_c = io_man.get_btn_c()
    tft = io_man.get_tft()
    
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
    menu1 = menus.menu("Menu", [("IR Remote", 1), ("Terminal", 2), ("Music Player", 6), ("File explorer", 7), ("Others", 4), ("Settings", 3), ("Close", 13)])
    if menu1 == 3:
        import apps.settings as a_se
        a_se.run()
        del a_se
        dechache('apps.settings')
    elif menu1 == 4:
        import apps.others as a_ot
        a_ot.run()
        del a_ot
        dechache('apps.others')
    elif menu1 == 1:
        import apps.IR as a_ir
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
        import apps.player as a_pl
        a_pl.run()
        del a_pl
        dechache('apps.player')
    elif menu1 == 7:
        import modules.fileexplorer as a_fe
        a_fe.run()
        del a_fe
        dechache('modules.fileexplorer')
    gc.collect()
    machine.freq(osc.BASE_FREQ)