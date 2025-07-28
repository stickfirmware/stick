import modules.printer as debug
from machine import Pin
import modules.os_constants as osc

def init_buttons():
    if osc.INPUT_METHOD == 1:
        debug.log("Input method 1 - 3 Buttons")
        # Normal inputs, over gpio pins
        button_a = Pin(osc.BUTTON_A_PIN, Pin.IN, Pin.PULL_UP)
        button_b = Pin(osc.BUTTON_B_PIN, Pin.IN, Pin.PULL_UP)
        button_c = Pin(osc.BUTTON_C_PIN, Pin.IN, Pin.PULL_UP)
    elif osc.INPUT_METHOD == 2:
        debug.log("Input method 2 - Cardputer")
        # Cardputer inputs, fake machine.Pin using keyboard keys
        import modules.cardputer_kb as ckb
        button_a = ckb.buttonemu('enter')
        button_b = ckb.buttonemu('tab')
        button_c = ckb.buttonemu('`')
    return [button_a, button_b, button_c]
