"""
Battery voltage helper
"""

from machine import ADC, Pin

import fonts.def_8x8 as f8x8
import modules.os_constants as osc

# Check if it uses standard ADC measurements, or spoofed
if osc.BATTERY_MEASURE_MODE == 1:
    adc = ADC(Pin(osc.BATTERY_ADC))
    adc.atten(ADC.ATTN_11DB)

# Percentage anti-rerender
last_bitmap = None # temp value to force refresh

def voltage(samplecount: int = 10) -> float:
    """
    Get battery voltage

    Note:
        On devices with BATTERY_MEASURE_MODE set to 2 (Spoofed) will always return 4.20
    
    Args:
        samplecount (int, optional): ADC sample count, default is 10
        
    Returns:
        float: Battery voltage
    """
    if osc.BATTERY_MEASURE_MODE == 1:
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
    else:
        return 4.20

def percentage(voltage: float) -> float:
    """
    Get battery percentage from voltage
    
    Args:
        voltage (float): Battery voltage
        
    Returns:
        float: Battery percentage
    """
    pr = (voltage - osc.BATTERY_DISCHARGE_VOLTAGE) / (osc.BATTERY_FULL_CHARGE_VOLTAGE - osc.BATTERY_DISCHARGE_VOLTAGE) * 100
    if pr <= 0.00:
        pr = 0.00
    elif pr >= 100.00:
        pr = 100.00
    return pr
    
def run(tft):
    """
    Display battery percentage for clock screen

    Note:
        On devices with BATTERY_MEASURE_MODE set to 2 (Spoofed) will not render anything

    Args:
        tft (any): TFT class
    """
    global last_bitmap
    perc = int(percentage(voltage()))
    if last_bitmap != perc and osc.BATTERY_MEASURE_MODE == 1:
        last_bitmap = perc
        tft.text(f8x8, "    ", 200, 5, 2027)
        tft.text(f8x8, f"{perc}%", 200, 5, 2027)