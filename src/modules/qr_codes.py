import modules.uQR as uQR
import modules.powersaving as ps

def make_qr(tft, data, xd, yd, size=1):
    ps.boost_allowing_state(True)
    ps.boost_clock()
    qr = uQR.make(data=data)
    render_qr(tft, qr, xd, yd, size)
    ps.boost_allowing_state(False)
    ps.loop()

def render_qr(tft, qr, xd, yd, size=1):
    for y, line in enumerate(qr):
        for x, pixel in enumerate(line):
            color = 0x0000 if pixel else 0xFFFF
            px = xd + x * size
            py = yd + y * size

            if size == 1:
                tft.pixel(px, py, color)
            else:
                tft.fill_rect(px, py, size, size, color)