BATTERY_FULL = 3.95
BATTERY_MID = 3.65
BATTERY_LOW = 3.25

from machine import ADC, Pin
import modules.osconstants as osc
import bitmaps.battery as b_battery
import bitmaps.battery_1 as b_battery_1
import bitmaps.battery_2 as b_battery_2
import bitmaps.battery_3 as b_battery_3

adc = ADC(Pin(osc.BATTERY_ADC))
adc.atten(ADC.ATTN_11DB)

# Bitmap anti-rerender
last_bitmap = None

def voltage(samplecount=10):
    samples = []
    samplecalc = 0
    for i in range(samplecount):
        raw = adc.read()
        samples.append(raw)
    for i in samples:
        samplecalc += i
    avg = samplecalc / len(samples)
    volt = avg / 4095 * 3.6 * 2
    return round(volt, 2)

def percentage(voltage):
    pr = (voltage - 3.00) / 1.20 * 100
    if pr <= 0.00:
        pr = 0.00
    elif pr >= 100.00:
        pr = 100.00
    return pr

def bitmap():
    v = voltage()
    if v >= BATTERY_FULL:
        return 3
    elif v >= BATTERY_MID:
        return 2
    elif v >= 3.25:
        return 1
    else:
        return 0
    
def run(tft):
    bitm = bitmap()
    global last_bitmap
    if last_bitmap == bitm:
        return
    last_bitmap = bitm
    if bitm == 3:
        tft.bitmap(b_battery_3, 210,3)
    elif bitm == 2:
        tft.bitmap(b_battery_2, 210,3)
    elif bitm == 1:
        tft.bitmap(b_battery_1, 210,3)
    else:
        tft.bitmap(b_battery, 210,3)