from machine import ADC, Pin

import bitmaps.battery as b_battery
import bitmaps.battery_1 as b_battery_1
import bitmaps.battery_2 as b_battery_2
import bitmaps.battery_3 as b_battery_3

adc = ADC(Pin(38))
adc.atten(ADC.ATTN_11DB)

def voltage():
    raw = adc.read()
    volt = raw / 4095 * 3.6 * 2
    return round(volt, 2)

def bitmap():
    v = voltage()
    if v >= 3.95:
        return 3
    elif v >= 3.70:
        return 2
    elif v >= 3.45:
        return 1
    else:
        return 0
    
def run(tft):
    bitm = bitmap()
    print("Rendering battery bitmap")
    if bitm == 3:
        tft.bitmap(b_battery_3, 210,3)
    elif bitm == 2:
        tft.bitmap(b_battery_2, 210,3)
    elif bitm == 1:
        tft.bitmap(b_battery_1, 210,3)
    else:
        tft.bitmap(b_battery, 210,3)