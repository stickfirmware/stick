import modules.io_manager as io_man
import modules.menus as menus
import modules.os_constants as osc
import modules.power as power
import modules.powersaving as ps
from modules.decache import decache
from modules.translate import get as l_get

button_a = io_man.get('button_a')
button_b = io_man.get('button_b')
button_c = io_man.get('button_c')
tft = None

def run():
    global button_c, button_a, button_b, tft
    button_a = io_man.get('button_a')
    button_b = io_man.get('button_b')
    button_c = io_man.get('button_c')
    tft = io_man.get('tft')

    q_actions = menus.menu(l_get("q_actions.quick_actions"),
                           [(l_get("q_actions.pwr_menu"), 1),
                            (l_get("apps.pet.name"), 2),
                            (l_get("apps.settings.name"), 3),
                            (l_get("menus.menu_close"), None)])
    if q_actions == 1:
        power_menu()
    elif q_actions == 2:
        import modules.open_app as open_app
        open_app.run("com.kitki30.pet", True)
    elif q_actions == 3:
        import apps.settings as a_se
        a_se.run()
        del a_se
        decache('apps.settings')

def power_menu(fast_sleep = False):
    if not fast_sleep:
        powermenu = menus.menu(l_get("q_actions.power"), 
                            [(l_get("q_actions.sleep"), 1),
                                (l_get("q_actions.pwr_off"), 2),
                                (l_get("q_actions.reboot"), 3),
                                (l_get("menus.menu_close"), 4)])
    else:
        powermenu = 1
        
    # Sleep
    if powermenu == 1:
        power.light_sleep()
        
    # Power off
    elif powermenu == 2:
        power.shutdown()
        
    # Reboot
    elif powermenu == 3:
        power.reboot()
        
    # Exit
    else:
        ps.set_freq(osc.BASE_FREQ)