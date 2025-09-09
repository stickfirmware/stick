import machine

import modules.os_constants as osc

# Hold power
if osc.HAS_HOLD_PIN:
    power_hold = machine.Pin(osc.HOLD_PIN, machine.Pin.OUT)
    power_hold.value(1)