"""
Neopixel helper for Stick firmware
"""

import machine
import neopixel

import modules.io_manager as io_man

def make(pin: int, led_count: int = 1) -> bool:
    """
    Make neopixel object and save it to IO Manager
    
    Args:
        pin (int): Neopixel GPIO pin number
        led_count (int, optional): Neopixel led count, default is 1
        
    Returns:
        bool: True if success, False if failed
    """
    
    np = None
    try:
        np = neopixel.NeoPixel(machine.Pin(pin), led_count)
        io_man.set("neopixel", np)
        return True
    except ValueError:
        print("Error, wrong pin number! NeoPixel object could not be created!")
        return False
    
def set_led(colors: tuple, led_num: int = 0, auto_write: bool = True):
    """
    Sets neopixel led color.
    
    Args:
        colors (tuple): RGB tuple ex. (255, 255, 64)
        led_num (int, optional): Led number, optional, zero-based
        auto_write (bool, optional): Write to led after setting color
    """
    
    np = io_man.get("neopixel")
    
    if np == None:
        return
    
    # Validate colors
    r, g, b = colors
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    np[led_num] = (r, g, b)

    # Write
    if auto_write == True: 
        np.write()
    
def write():
    """
    Writes colors to neopixel
    """
    
    np = io_man.get("neopixel")
    
    if np == None:
        return
    
    np.write()