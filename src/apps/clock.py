import machine

import fonts.def_8x8 as f8x8
import fonts.def_16x32 as f16x32
import network
import modules.io_manager as io_man

tft = io_man.get_tft()

allow_drawing_battery = True

def run_clock():
    print("Rendering clock base")
    tft.fill_rect(0, 0, 240, 3, 65535)
    tft.fill_rect(0, 16, 240, 3, 65535)
    tft.fill_rect(0, 132, 240, 3, 65535)
    tft.fill_rect(0, 0, 3, 135, 65535)
    tft.fill_rect(237, 0, 3, 135, 65535)
    tft.fill_rect(3, 3, 234, 13, 0)
    tft.fill_rect(3, 19, 234, 113, 0)
    tft.text(f8x8, "Clock",5,5,65535)
    
def run_clock_vert():
    print("Rendering clock base")
    tft.fill_rect(0, 0, 3, 240, 65535)
    tft.fill_rect(132, 0, 3, 240, 65535)
    tft.fill_rect(0, 0, 135, 3, 65535)
    tft.fill_rect(0, 16, 135, 3, 65535)
    tft.fill_rect(0, 237, 135, 3, 65535)
    tft.fill_rect(3, 3, 129, 13, 0)
    tft.fill_rect(3, 19, 129, 218, 0)
    tft.text(f8x8, "Clock",5,5,65535)
    
def clock_vert():
    rtc = machine.RTC()
    time_tuple = rtc.datetime()
    
    # Time
    hh = time_tuple[4]
    mm = time_tuple[5]
    ss = time_tuple[6]
    text = "{:02}:{:02}:{:02}".format(hh, mm, ss)
    text_width = len(text) * 16
    x = (135 - text_width) // 2
    tft.text(f16x32, text, x, 104, 65535)
    
    # Date
    text = "{:02d}.{:02d}.{:04d}".format(rtc.datetime()[2], rtc.datetime()[1], rtc.datetime()[0])
    text_width = len(text) * 8
    x = (135 - text_width) // 2
    tft.text(f8x8, text, x, 136, 65535)


def clock():
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
