import modules.io_manager as io_man
from modules.decache import decache
import modules.menus as menus
import modules.osconstants as osc
import machine
import gc

button_a = None
button_b = None
button_c = None
tft = None

def run():
    global button_c, button_a, button_b, tft
    button_a = io_man.get_btn_a()
    button_b = io_man.get_btn_b()
    button_c = io_man.get_btn_c()
    tft = io_man.get_tft()
    
    machine.freq(osc.ULTRA_FREQ)
    menu1 = menus.menu("Menu", [("IR Remote", 1), ("Terminal", 2), ("Music Player", 6), ("File explorer", 7), ("Others", 4), ("Settings", 3), ("Close", 13)])
    if menu1 == 3:
        import apps.settings as a_se
        a_se.run()
        del a_se
        decache('apps.settings')
    elif menu1 == 4:
        import apps.others as a_ot
        a_ot.run()
        del a_ot
        decache('apps.others')
    elif menu1 == 1:
        import apps.IR as a_ir
        a_ir.run()
        a_ir.exit()
        del a_ir
        decache('apps.IR')
    elif menu1 == 2:
        import apps.terminal as a_tm
        a_tm.run()
        a_tm.exit()
        del a_tm
        decache('apps.terminal')
    elif menu1 == 6:
        import apps.player as a_pl
        a_pl.run()
        del a_pl
        decache('apps.player')
    elif menu1 == 7:
        import modules.fileexplorer as a_fe
        a_fe.run()
        del a_fe
        decache('modules.fileexplorer')
    gc.collect()
    machine.freq(osc.BASE_FREQ)