# Resistor decoder app
# App ID: 1002

import time

import fonts.def_8x8 as f8x8

import modules.os_constants as osc
import modules.menus as menus
import modules.io_manager as io_man
import modules.printer as printer
import modules.powersaving as ps
from modules.translate import get as l_get

button_a = io_man.get('button_a')
button_b = io_man.get('button_b')
button_c = io_man.get('button_c')
tft = None
    
#BLACK = 0 #1
#BROWN = 14693 #2
#RED = 63488 #3
#ORANGE = 64640 #4
#YELLOW = 63456 #5
#GREEN = 2016 #6
#BLUE = 5723 #7
#VIOLET = 37019 #8
#GRAY = 25356 #9
#WHITE = 65535 #10
#GOLD = 65184 #11
#SILVER = 48631 #12

colors_f = [0, 37222, 63488, 64640, 63456, 2016, 5723, 37019, 25356, 65535]
colors_m = [0, 37222, 63488, 64640, 63456, 2016, 5723, 37019, 65184, 48631]
colors_t = [37222, 63488, 2016, 5723, 37019, 25356, 65184, 48631]

mapping_first = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
mapping_second = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
mapping_third = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
mapping_fourth = [1.0, 10.0, 100.0, 1000.0, 10000.0, 100000.0, 1000000.0, 10000000.0, 0.1, 0.01]
mapping_fifth = [1.0, 2.0, 0.5, 0.25, 0.1, 0.05, 5, 10]
    
def format_resistance(res):
    if res >= 1_000_000_000:
        return "{:.2f} G ohm".format(res / 1_000_000_000)
    elif res >= 1_000_000:
        return "{:.2f} M ohm".format(res / 1_000_000)
    elif res >= 1_000:
        return "{:.2f} k ohm".format(res / 1_000)
    else:
        return "{} ohm".format(int(res))

def four():
    import fonts.def_8x8 as f8x8
    tft.fill(0)
    tft.text(f8x8, l_get("apps.resistors.four_color_mode"),0,0,2022)
    tft.text(f8x8, l_get("apps.resistors.c_exit"),0,8,2022)
    tft.text(f8x8, l_get("apps.resistors.a_change"),0,16,2022)
    tft.text(f8x8, l_get("apps.resistors.b_line"),0,24,2022)
    tft.fill_rect(0, 65, 240, 20, 54938)
    tft.fill_rect(25, 35, 190, 80, 5119)
    
    line_num = 1
    
    res1 = 6
    res2 = 6
    res3 = 6
    res4 = 3
    
    work = True
    upd = True
    while work:
        if upd:
            tft.fill_rect(0, 105, 240, 30, 0)
            if line_num == 1:
                tft.text(f8x8, "^",66,105,2022)
            elif line_num == 2:
                tft.text(f8x8, "^",86,105,2022)
            elif line_num == 3:
                tft.text(f8x8, "^",106,105,2022)
            elif line_num == 4:
                tft.text(f8x8, "^",146,105,2022)
            tft.fill_rect(60, 40, 12, 60, colors_f[res1 - 1])
            tft.fill_rect(80, 40, 12, 60, colors_f[res2 - 1])
            tft.fill_rect(100, 40, 12, 60, colors_m[res3 - 1])
            tft.fill_rect(140, 40, 12, 60, colors_t[res4 - 1])
            resistance = (mapping_second[res1 - 1] + mapping_third[res2 - 1]) * mapping_fourth[res3 - 1]
            tft.text(f8x8, l_get("apps.resistors.resistance") + ": " + str(format_resistance(resistance)),0,119,2022)
            tft.text(f8x8, l_get("apps.resistors.tolerance") + ": +-" + str(mapping_fifth[res4 - 1]) + "%",0,127,2022)
            upd = False
        
        if button_a.value() == 0:
            while button_a.value() == 0:
                time.sleep(0.02)
            if line_num == 1:
                if res1 == len(colors_f):
                    res1 = 1
                else:
                    res1 += 1
            elif line_num == 2:
                if res2 == len(colors_f):
                    res2 = 1
                else:
                    res2 += 1
            elif line_num == 3:
                if res3 == len(colors_m):
                    res3 = 1
                else:
                    res3 += 1
            elif line_num == 4:
                if res4 == len(colors_t):
                    res4 = 1
                else:
                    res4 += 1
            upd = True
                    
        if button_b.value() == 0:
            while button_b.value() == 0:
                time.sleep(0.02)
            if line_num == 4:
                line_num = 1
            else:
                line_num += 1
            upd = True
        
        if button_c.value() == 0:
            while button_c.value() == 0:
                time.sleep(0.02)
            work = False
    
def five():
    import fonts.def_8x8 as f8x8
    tft.fill(0)
    tft.text(f8x8, l_get("apps.resistors.five_color_mode"),0,0,2022)
    tft.text(f8x8, l_get("apps.resistors.c_exit"),0,8,2022)
    tft.text(f8x8, l_get("apps.resistors.a_change"),0,16,2022)
    tft.text(f8x8, l_get("apps.resistors.b_line"),0,24,2022)
    tft.fill_rect(0, 65, 240, 20, 54938)
    tft.fill_rect(25, 35, 190, 80, 5119)
    
    line_num = 1
    
    res1 = 6
    res2 = 6
    res3 = 6
    res4 = 6
    res5 = 3
    
    work = True
    upd = True
    while work:
        if upd:
            tft.fill_rect(0, 105, 240, 30, 0)
            if line_num == 1:
                tft.text(f8x8, "^",66,105,2022)
            elif line_num == 2:
                tft.text(f8x8, "^",86,105,2022)
            elif line_num == 3:
                tft.text(f8x8, "^",106,105,2022)
            elif line_num == 4:
                tft.text(f8x8, "^",126,105,2022)
            elif line_num == 5:
                tft.text(f8x8, "^",166,105,2022)
            tft.fill_rect(60, 40, 12, 60, colors_f[res1 - 1])
            tft.fill_rect(80, 40, 12, 60, colors_f[res2 - 1])
            tft.fill_rect(100, 40, 12, 60, colors_f[res3 - 1])
            tft.fill_rect(120, 40, 12, 60, colors_m[res4 - 1])
            tft.fill_rect(160, 40, 12, 60, colors_t[res5 - 1])
            resistance = (mapping_first[res1 - 1] + mapping_second[res2 - 1] + mapping_third[res3 - 1]) * mapping_fourth[res4 - 1]
            tft.text(f8x8, l_get("apps.resistors.resistance") + ": " + str(format_resistance(resistance)),0,119,2022)
            tft.text(f8x8, l_get("apps.resistors.tolerance") + ": +-" + str(mapping_fifth[res5 - 1]) + "%",0,127,2022)
            upd = False
        
        if button_a.value() == 0:
            while button_a.value() == 0:
                time.sleep(0.02)
            if line_num == 1:
                if res1 == len(colors_f):
                    res1 = 1
                else:
                    res1 += 1
            elif line_num == 2:
                if res2 == len(colors_f):
                    res2 = 1
                else:
                    res2 += 1
            elif line_num == 3:
                if res3 == len(colors_f):
                    res3 = 1
                else:
                    res3 += 1
            elif line_num == 4:
                if res4 == len(colors_m):
                    res4 = 1
                else:
                    res4 += 1
            elif line_num == 5:
                if res5 == len(colors_t):
                    res5 = 1
                else:
                    res5 += 1
            upd = True
                    
        if button_b.value() == 0:
            while button_b.value() == 0:
                time.sleep(0.02)
            if line_num == 5:
                line_num = 1
            else:
                line_num += 1
            upd = True
        
        if button_c.value() == 0:
            while button_c.value() == 0:
                time.sleep(0.02)
            work = False

def run():
    global button_c, button_a, button_b, tft
    button_a = io_man.get('button_a')
    button_b = io_man.get('button_b')
    button_c = io_man.get('button_c')
    tft = io_man.get('tft')
    
    ps.set_freq(osc.BASE_FREQ)

    printer.log("Going into main loop")
    
    render = menus.menu(l_get("apps.resistors.select_type"),
                        [(l_get("apps.resistors.four_colors"), 1),
                         (l_get("apps.resistors.five_colors"), 2),
                         (l_get("menus.menu_close"), 3)])
    if render == 1:
        tft.text(f8x8, l_get("apps.resistors.wait"),0,0,2022)
        four()
    elif render == 2:
        tft.text(f8x8, l_get("apps.resistors.wait"),0,0,2022)
        five()
    
        

