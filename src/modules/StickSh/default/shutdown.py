import machine
from machine import Pin

def execute(args):
    power_hold = Pin(4, Pin.OUT)
    machine.freq(80000000)
    power_hold.value(0)
    return "Powering off"
