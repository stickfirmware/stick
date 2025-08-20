from machine import ADC, Pin

import modules.os_constants as osc

import fonts.def_8x8 as f8x8

adc = ADC(Pin(osc.BATTERY_ADC))
adc.atten(ADC.ATTN_11DB)

# Percentage anti-rerender
last_bitmap = None # temp value to force refresh

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
    
def run(tft):
    global last_bitmap
    perc = int(percentage(voltage()))
    if last_bitmap != perc:
        last_bitmap = perc
        tft.text(f8x8, "    ", 200, 5, 2027)
        tft.text(f8x8, f"{perc}%", 200, 5, 2027)