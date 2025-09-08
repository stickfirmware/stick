"""
Neopixel animation helper for Stick firmware
"""
import modules.neopixels as neopixels
import modules.io_manager as io_man
import modules.os_constants as osc
import modules.cache as cache
import modules.nvs as nvs

_RAINBOW_FRAME_COUNT = 0
_CACHE_COUNT = 0

enabled = None
anim_style = None
r = None
g = None
b = None

def _WHEEL(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)
    
def static(r: int, g: int, b: int):
    """
    Sets static color on all neopixels.
    
    Args:
        r (int): R color in RGB
        g (int): G color in RGB
        b (int): B color in RGB
    """
    
    for i in range(osc.NEOPIXEL_LED_COUNT):
        neopixels.set_led((r, g, b), i, False)
        
    neopixels.write()
    
def rainbow():
    """
    Plays rainbow animation on neopixels.
    """
    
    global _RAINBOW_FRAME_COUNT
    for i in range(osc.NEOPIXEL_LED_COUNT):
        neopixels.set_led(_WHEEL(_RAINBOW_FRAME_COUNT), i, False)
    neopixels.write()
    _RAINBOW_FRAME_COUNT += 1
    if _RAINBOW_FRAME_COUNT >= 255:
        _RAINBOW_FRAME_COUNT = 0
        
def disabled():
    """
    Disable all leds on neopixel
    """
    
    for i in range(osc.NEOPIXEL_LED_COUNT):
        neopixels.set_led((0, 0, 0), i, False)
    neopixels.write()
    
def automatic(use_cache: bool = False) -> int:
    """
    Automatic neopixel animation setter.
    
    Args:
        use_cache (bool, optional): Use cached values, default False
        
    Returns:
        int: Animation type
    """
    
    global enabled, r, g, b, anim_style, _CACHE_COUNT
    
    # Led type cardputer
    if osc.NEOPIXEL_TYPE == 1:
        tft = io_man.get("tft")
        if tft.get_backlight() < osc.NEOPIXEL_BACKLIGHT_THRESHOLD:
            disabled()
            return
        
    if _CACHE_COUNT == 0:
        _CACHE_COUNT = 50
        if use_cache == False:
            n_settings = cache.get_nvs("settings")
            
            enabled = nvs.get_int(n_settings, "neo_enabled")
            if enabled == False:
                disabled()
                return
            
            anim_style = nvs.get_int(n_settings, "neo_anim_style")
            r = nvs.get_int(n_settings, "neo_R")
            g = nvs.get_int(n_settings, "neo_G")
            b = nvs.get_int(n_settings, "neo_B")
        else:
            enabled = cache.get_and_remove("neo_enabled")
            if enabled == False:
                disabled()
                return
            
            anim_style = cache.get_and_remove("neo_anim_style")
            r = cache.get_and_remove("neo_R")
            g = cache.get_and_remove("neo_G")
            b = cache.get_and_remove("neo_B")
    else:
        _CACHE_COUNT -= 1
        if enabled == False:
            disabled()
            return
    
    if anim_style == 1:
        static(r, g, b)
    elif anim_style == 2:
        rainbow()
    
    return anim_style

def refresh_counters():
    """
    Refreshes cache and frame counters
    """
    
    global _RAINBOW_FRAME_COUNT, _CACHE_COUNT
    _CACHE_COUNT = 0
    _RAINBOW_FRAME_COUNT = 0