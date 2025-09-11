"""
App boot intro, async
"""

import asyncio

import modules.io_manager as io_man
import modules.os_constants as osc
import modules.text_utils as text_utils

import fonts.def_16x16 as f16x16

async def run(fill_tft=True):
    """
    Run app boot intro
    """
    
    tft = io_man.get("tft")
    if fill_tft:
        tft.fill(65535)

    text = "Stick firmware"
    x = text_utils.center_x(text, 16)
    y = text_utils.center_y(16)
    tft.text(f16x16, text, x, y, 0, 65535)

    bright = tft.get_backlight()
    tft.set_backlight(1)
    
    if osc.HAS_NEOPIXEL:
        import modules.neopixel_anims as np
        np.disabled()

    await asyncio.sleep(1.5)

    steps = 20
    delay = 0.5 / steps
    for i in range(steps, -1, -1):
        b = (i / steps) * bright
        tft.set_backlight(b)
        await asyncio.sleep(delay)
        
    tft.fill(0) 
    await asyncio.sleep(0.5)

    tft.set_backlight(bright)
    
    if osc.HAS_NEOPIXEL:
        np.automatic()