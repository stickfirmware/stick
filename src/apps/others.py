import modules.io_manager as io_man
from modules.decache import dechache
import modules.osconstants as osc
import modules.menus as menus
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
    
    render = menus.menu("Menu/Others", [("PiMarkX", 5), ("Scorekeeper", 1), ("Resistor decoder", 2), ("Metronome", 3), ("Close", 13)])
    if render == 1:
        import apps.scorekeeper as a_sc
        a_sc.run()
        del a_sc
        dechache('apps.scorekeeper')
    elif render == 2:
        import apps.resistors as a_re
        a_re.run()
        del a_re
        dechache('apps.resistors')
    elif render == 3:
        import apps.metronome as a_me
        a_me.run()
        del a_me
        dechache('apps.metronome')
    elif render == 5:
        import apps.pimarkx as a_pimark
        a_pimark.run()
        del a_pimark
        dechache('apps.pimarkx')
    gc.collect()
    machine.freq(osc.BASE_FREQ)