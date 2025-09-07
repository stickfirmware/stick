"""
TFT Display init helper for Stick firmware
"""

from machine import SPI, Pin, PWM

from modules.printer import log
import modules.os_constants as osc
import modules.st7789 as st7789

def init_tft() -> any | None:
    """
    Init and get TFT display from OS Constants
    
    Returns:
        any | None: ST7789 class or None if failed to init
    """
    try:
        tft = st7789.ST7789(
                SPI(osc.LCD_SPI_SLOT, baudrate=osc.LCD_SPI_BAUD, sck=Pin(osc.LCD_SPI_SCK), mosi=Pin(osc.LCD_SPI_MOSI), miso=osc.LCD_SPI_MISO),
                osc.LCD_HEIGHT,
                osc.LCD_WIDTH,
                reset=Pin(osc.LCD_RESET, Pin.OUT),
                cs=Pin(osc.LCD_SPI_CS, Pin.OUT),
                dc=Pin(osc.LCD_DC, Pin.OUT),
                backlight=PWM(Pin(osc.LCD_BL), freq=osc.LCD_BL_FREQ),
                rotation=osc.LCD_ROTATIONS["BUTTON_LEFT"])
        return tft
    except Exception as e:
        log("Failed to init tft")
        log(str(e))
        return None