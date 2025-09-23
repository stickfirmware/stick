import modules.io_manager as io_man
import modules.os_constants as osc

import fonts.def_8x8 as f8x8

def show_saving_prompt(clear = False):
    """
    Shows saving prompt on display
    
    Args:
        clean (bool): If True, clears display before showing prompt
    """
    
    tft = io_man.get('tft')
    if clear:
        tft.fill(0)
        
    # TODO: Translate
    tft.text(f8x8, "Saving...", 0,0,65535)
    tft.text(f8x8, "Do not turn off!!!", 0,8,65535)
    
    # Make neopixel red
    if osc.HAS_NEOPIXEL:
        import modules.neopixel_anims as np
        np.static((255,0,0))