# Hold power
from machine import Pin
print("\nEnable hold pin")
power_hold = Pin(4, Pin.OUT)
power_hold.value(1)