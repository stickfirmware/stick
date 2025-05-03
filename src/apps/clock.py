import machine

import fonts.def_8x8 as f8x8
import fonts.def_16x32 as f16x32
import network

allow_draw_battery = True

tft = None

def set_tft(tft_n):
    global tft
    tft = tft_n

def run_clock():
    if tft == None:
        print("Please call 'set_tft(tft)' first")
        return
    print("Rendering clock base")
    tft.fill_rect(0, 0, 240, 3, 65535)
    tft.fill_rect(0, 16, 240, 3, 65535)
    tft.fill_rect(0, 132, 240, 3, 65535)
    tft.fill_rect(0, 0, 3, 135, 65535)
    tft.fill_rect(237, 0, 3, 135, 65535)
    tft.fill_rect(3, 3, 234, 13, 0)
    tft.fill_rect(3, 19, 234, 113, 0)
    tft.text(f8x8, "Clock",5,5,65535)

def clock():
    if tft == None:
        print("Please call 'set_tft(tft)' first")
        return
    rtc = machine.RTC()
    time_tuple = rtc.datetime()
    
    nic = network.WLAN(network.STA_IF)
    if nic.isconnected() == True:
        tft.text(f8x8, "Wi-Fi",50,5,703)
    else:
        tft.text(f8x8, "     ",50,5,703)
    
    # Time
    hh = time_tuple[4]
    mm = time_tuple[5]
    ss = time_tuple[6]
    text = "{:02}:{:02}:{:02}".format(hh, mm, ss)
    text_width = len(text) * 16
    x = (240 - text_width) // 2
    tft.text(f16x32, text, x, 60, 65535)
    
    # Date
    text = "{:02d}.{:02d}.{:04d}".format(rtc.datetime()[2], rtc.datetime()[1], rtc.datetime()[0])
    text_width = len(text) * 8
    x = (240 - text_width) // 2
    tft.text(f8x8, text, x, 93, 65535)
