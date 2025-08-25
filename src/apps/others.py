import gc

import modules.io_manager as io_man
import modules.cache as cache
from modules.decache import decache
import modules.os_constants as osc
import modules.menus as menus
import modules.powersaving as ps
import modules.popup as popup
from modules.translate import get as l_get

button_a = None
button_b = None
button_c = None
tft = None

def run():
    global button_c, button_a, button_b, tft
    button_a = io_man.get('button_a')
    button_b = io_man.get('button_b')
    button_c = io_man.get('button_c')
    tft = io_man.get('tft')
    
    render = menus.menu(l_get("apps.others.title"),
                        [(l_get("apps.qr_gen.name"), 6),
                         ("PiMarkX", 5),
                         (l_get("apps.dice.name"), 7),
                         (l_get("apps.scorekeeper.name"), 1),
                         (l_get("apps.resistors.name"), 2),
                         (l_get("apps.metronome.name"), 3),
                         (l_get("menus.menu_close"), 13)])
    if render == 1:
        import apps.scorekeeper as a_sc
        a_sc.run()
        del a_sc
        decache('apps.scorekeeper')
    elif render == 2:
        import apps.resistors as a_re
        a_re.run()
        del a_re
        decache('apps.resistors')
    elif render == 3:
        if osc.HAS_BUZZER == False:
            popup.show(l_get("apps.others.buzzer_info_metronome"), l_get("crashes.error"), 10)
            return
        import apps.metronome as a_me
        a_me.run()
        del a_me
        decache('apps.metronome')
    elif render == 5:
        import apps.pimarkx as a_pimark
        a_pimark.run()
        del a_pimark
        decache('apps.pimarkx')
    elif render == 6:
        import apps.qr_gen as a_qr
        a_qr.run()
        del a_qr
        decache('apps.qr_gen')
    elif render == 7:
        if cache.get("rand_extra_func") == True:
            import apps.dice as a_dc
            a_dc.run()
            del a_dc
            decache('apps.dice')
        else:
            menus.menu(l_get("apps.others.rand_extra_func"), [(l_get("menus.menu_close"),1)])
    gc.collect()
    ps.set_freq(osc.BASE_FREQ)