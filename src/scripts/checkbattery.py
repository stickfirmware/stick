"""
Checks battery voltage and shuts down device if it's too low
"""

from machine import Pin

import modules.os_constants as osc
from modules.battery_check import voltage


def run():
    if osc.BATTERY_MEASURE_MODE == 1:
        if voltage(50) <= osc.BATTERY_DISCHARGE_VOLTAGE:
            if osc.HAS_HOLD_PIN:
                power_hold = Pin(osc.HOLD_PIN, Pin.OUT)
                power_hold.value(0)
        
run()