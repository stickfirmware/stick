import time
import machine
import gc

import fonts.def_8x8 as f8x8

import modules.os_constants as osc
import modules.io_manager as io_man
import modules.powersaving as ps

button_a = io_man.get('button_a')
button_b = io_man.get('button_b')
button_c = io_man.get('button_c')
tft = io_man.get('tft')
    
# Refresh io
def load_io():
    global button_c, button_a, button_b, tft
    button_a = io_man.get('button_a')
    button_b = io_man.get('button_b')
    button_c = io_man.get('button_c')
    tft = io_man.get('tft')
    
def elems_split(arr, chunk_size=13):
    return [arr[i:i+chunk_size] for i in range(0, len(arr), chunk_size)]

def menu(name, choices):
    load_io()
    curr_freq = machine.freq()
    ps.boost_allowing_state(True)
    ps.set_freq(osc.ULTRA_FREQ)
    tft.fill_rect(0, 0, 240, 3, 65535)
    tft.fill_rect(0, 16, 240, 3, 65535)
    tft.fill_rect(0, 132, 240, 3, 65535)
    tft.fill_rect(0, 0, 3, 135, 65535)
    tft.fill_rect(237, 0, 3, 135, 65535)
    tft.fill_rect(3, 3, 234, 13, 0)
    tft.fill_rect(3, 19, 234, 113, 0)
    tft.text(f8x8, str(name),5,5,65535)
    
    pages = elems_split(choices)
    curr_page = 0
    page_count = len(pages)
    
    lcd_space = 13
    lcd_left = 104
    lcd_curr = 25
    choice = 1
    didnt_choose = False
    update = True
    page_upd = True
    chosen = False
    
    # Debounce
    bt1_d = button_a.value()
    bt2_d = button_b.value()
    bt3_d = button_c.value()
    
    # Return to base freq after render
    ps.set_freq(osc.BASE_FREQ)
    
    # Main menu loop
    while chosen == False:
        # Update marker
        if update:
            tft.fill_rect(15, 19, 8, 104, 0)
            tft.text(f8x8, ">", 15, (17 + ((choice) * 8)), 20365)
            update = False
            
        # Update page
        if page_upd == True:
            lcd_space = 13
            lcd_curr = 25
            tft.fill_rect(3, 19, 234, 113, 0)
            for name, val in pages[curr_page]:
                if lcd_space == 0:
                    break 
                tft.text(f8x8, str(name), 25, lcd_curr, 65535)
                lcd_curr += 8
                lcd_space -= 1
            update = True
            page_upd = False
            
        # Exit
        if button_c.value() == 0 and bt3_d == 1:
            while button_c.value() == 0:
                time.sleep(osc.DEBOUNCE_TIME)
            didnt_choose = True
            chosen = True
        elif button_c.value() == 1 and bt3_d == 0:
            bt3_d = 1

        # Select    
        if button_a.value() == 0 and bt1_d == 1:
            while button_a.value() == 0:
                time.sleep(osc.DEBOUNCE_TIME)
            chosen = True
        elif button_a.value() == 1 and bt1_d == 0:
            bt1_d = 1
            
        # Cycle
        if button_b.value() == 0 and bt2_d == 1:
            while button_b.value() == 0:
                time.sleep(osc.DEBOUNCE_TIME)
            if choice == len(pages[curr_page]):
                choice = 1
                if (curr_page + 1) == page_count:
                    curr_page = 0
                    page_upd = True
                else:
                    curr_page += 1
                    page_upd = True
            else:
                choice += 1
            update = True
        elif button_b.value() == 1 and bt2_d == 0:
            bt2_d = 1
        
        time.sleep(osc.LOOP_WAIT_TIME)
        
    gc.collect()
    # Return to starting frequency
    ps.set_freq(curr_freq)
    ps.boost_allowing_state(False)
    
    if didnt_choose == True:
        return None
    else:
        choicef = pages[curr_page][choice - 1][1]
        return choicef