"""
QR Code display helper for Stick firmware
"""

import modules.uQR as uQR
import modules.powersaving as ps

def make_qr(tft: any, data: str, xd: int, yd: int, size: int = 1, black_only: bool = False):
    """
    Make and display QR code from provided data
    
    Args:
        tft (any): TFT Display object
        data (str): QR Code data
        xd (int): X position on screen
        yd (int): Y position on screen
        size (int, optional): QR code size, default 1
        black_only (bool, optional): Render only black parts of QR, default is False (White and Black render)
    """
    ps.boost_allowing_state(True)
    ps.boost_clock()
    qr = uQR.make(data=data)
    render_qr(tft, qr, xd, yd, size, black_only)
    ps.boost_allowing_state(False)
    ps.loop()

def render_qr(tft: any, qr: any, xd: int, yd: int, size: int = 1, black_only: bool = False):
    """
    Render QR code on screen
    
    Args:
        tft (any): TFT Display object
        qr (any): QR Code object
        xd (int): X position on screen
        yd (int): Y position on screen
        size (int, optional): QR code size, default 1
        black_only (bool, optional): Render only black parts of QR, default is False (White and Black render)
    """
    if black_only:
        tft.fill(65535)
    for y, line in enumerate(qr):
        for x, pixel in enumerate(line):
            color = 0x0000 if pixel else 0xFFFF
            px = xd + x * size
            py = yd + y * size

            if color == 0x0000 or black_only == False:
                if size == 1:
                    tft.pixel(px, py, color)
                else:
                    tft.fill_rect(px, py, size, size, color)