import modules.uQR as uQR
import framebuf

def make_qr(tft, data, xd, yd, size=1):
    qr = uQR.make(data=data)
    render_qr(tft, qr, xd, yd, size)
    
def render_qr(tft, qr, xd, yd, size=1):
    qr_w = len(qr[0]) * size
    qr_h = len(qr) * size

    buf = bytearray(qr_w * qr_h * 2)
    fb = framebuf.FrameBuffer(buf, qr_w, qr_h, framebuf.RGB565)

    for y, line in enumerate(qr):
        for x, pixel in enumerate(line):
            color = 0xFFFF if pixel == False else 0x0000
            for dy in range(size):
                for dx in range(size):
                    fb.pixel(x * size + dx, y * size + dy, color)

    tft.blit_buffer(buf, xd, yd, qr_w, qr_h)