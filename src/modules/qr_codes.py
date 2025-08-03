import machine

import modules.os_constants as osc
import modules.uQR as uQR

def make_qr(tft, data, xd, yd, size=1):
    qr = uQR.make(data=data)
    render_qr(tft, qr, xd, yd, size)

def render_qr(tft, qr, xd, yd, size=1):
    curr_freq = machine.freq()
    machine.freq(osc.ULTRA_FREQ)
    for y, line in enumerate(qr):
        for x, pixel in enumerate(line):
            color = 0x0000 if pixel else 0xFFFF
            px = xd + x * size
            py = yd + y * size

            if size == 1:
                tft.pixel(px, py, color)
            else:
                tft.fill_rect(px, py, size, size, color)
    machine.freq(curr_freq)