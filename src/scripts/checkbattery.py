DISCHARGE_VOLTAGE = 3.00

import modules.osconstants as osc
from machine import ADC, Pin

def run():
    adc = ADC(Pin(osc.BATTERY_ADC))
    adc.atten(ADC.ATTN_11DB)

    def voltage(samplecount=100):
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
    if voltage() <= DISCHARGE_VOLTAGE:
        power_hold = Pin(4, Pin.OUT)
        power_hold.value(0)
        
run()