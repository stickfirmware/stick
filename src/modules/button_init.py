from machine import Pin

import modules.printer as debug
import modules.io_manager as io_man
import modules.os_constants as osc

def init_buttons():
    if osc.INPUT_METHOD == 1:
        debug.log("Input method 1 - 3 Buttons")
        # Normal inputs, over gpio pins
        button_a = Pin(osc.BUTTON_A_PIN, Pin.IN, Pin.PULL_UP)
        button_b = Pin(osc.BUTTON_B_PIN, Pin.IN, Pin.PULL_UP)
        button_c = Pin(osc.BUTTON_C_PIN, Pin.IN, Pin.PULL_UP)
        clicker = None
    elif osc.INPUT_METHOD == 2:
        debug.log("Input method 2 - Cardputer")
        # Cardputer inputs, fake machine.Pin using keyboard keys
        import modules.cardputer_kb as ckb
        button_a = ckb.buttonemu(['enter'])
        button_b = ckb.buttonemu(['tab'])
        button_c = ckb.buttonemu(['`', '~'])
        # Super secret clicker game!
        clicker = ckb.buttonemu([' '])
    return [button_a, button_b, button_c, clicker]

# Invert buttons
def set_buttons(inverted=False):
    global button_b
    global button_c
    if osc.INPUT_METHOD == 1:
        if inverted:
            button_b = Pin(osc.BUTTON_C_PIN, Pin.IN, Pin.PULL_UP)
            button_c = Pin(osc.BUTTON_B_PIN, Pin.IN, Pin.PULL_UP)
        else:
            button_b = Pin(osc.BUTTON_B_PIN, Pin.IN, Pin.PULL_UP)
            button_c = Pin(osc.BUTTON_C_PIN, Pin.IN, Pin.PULL_UP)
        io_man.set('button_b', button_b)
        io_man.set('button_c', button_c)