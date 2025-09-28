import time
import machine
import gc

import fonts.def_8x8 as f8x8
#import fonts.def_16x16 as f16x16

import modules.os_constants as osc
import modules.io_manager as io_man
import modules.cache as cache
import modules.nvs as nvs
import modules.powersaving as ps

button_a = io_man.get('button_a')
button_b = io_man.get('button_b')
button_c = io_man.get('button_c')
tft = None

arrow_up = None
arrow_down = None
arrow_left = None
arrow_right = None
    
# Refresh io
def _LOAD_IO():
    global button_c, button_a, button_b, tft, arrow_up, arrow_down, arrow_left, arrow_right
    button_a = io_man.get('button_a')
    button_b = io_man.get('button_b')
    button_c = io_man.get('button_c')
    
    if osc.INPUT_METHOD == 2:
        import modules.cardputer_kb as ckb
        arrow_up = ckb.buttonemu([';', ':'])
        arrow_down = ckb.buttonemu(['.', '>'])
        arrow_left = ckb.buttonemu([',', '<'])
        arrow_right = ckb.buttonemu(['/', '?'])
    
    tft = io_man.get('tft')
    
def elems_split(arr, chunk_size=13):
    return [arr[i:i+chunk_size] for i in range(0, len(arr), chunk_size)]

def menu(name, choices):
    _LOAD_IO()
    # Boost freq
    curr_freq = machine.freq()
    ps.boost_allowing_state(True)
    ps.boost_clock()
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
    
    # Sleep backup
    bl_now = tft.get_backlight()
    
    # Is in sleep
    sleep_on = False
    
    # Init NVS
    n_settings = cache.get_nvs("settings")
    
    # Check if allow sleep
    allow_saving = nvs.get_int(n_settings, "allowsaving")
    
    # Sleep timer
    now_time = time.ticks_ms()
    
    if osc.INPUT_METHOD == 2:
        ar_up_d = arrow_up.value()
        ar_dn_d = arrow_down.value()
        ar_lt_d = arrow_left.value()
        ar_rt_d = arrow_right.value()
    
    # Return to base freq after render
    ps.set_freq(osc.BASE_FREQ)
    ps.boost_allowing_state(False)
    
    def menu_down():
        nonlocal choice, curr_page, page_upd, update
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
    
    def menu_up():
        nonlocal choice, curr_page, page_upd, update
        if choice == 1:
            if curr_page == 0:
                curr_page = page_count - 1
            else:
                curr_page -= 1
            choice = len(pages[curr_page])
            page_upd = True
        else:
            choice -= 1
        update = True
        
    def page_right():
        nonlocal curr_page, choice, page_upd, update
        if curr_page + 1 == page_count:
            curr_page = 0
        else:
            curr_page += 1

        if choice > len(pages[curr_page]):
            choice = len(pages[curr_page])

        page_upd = True
        update = True


    def page_left():
        nonlocal curr_page, choice, page_upd, update
        if curr_page == 0:
            curr_page = page_count - 1
        else:
            curr_page -= 1

        if choice > len(pages[curr_page]):
            choice = len(pages[curr_page])

        page_upd = True
        update = True
        
    def sleep(on = False):
        nonlocal now_time, bl_now, sleep_on
        sleep_on = on
        if on:
            if time.ticks_diff(time.ticks_ms(), now_time) > osc.POWER_SAVE_TIMEOUT:
                if osc.HAS_NEOPIXEL:
                    import modules.neopixel_anims as np_anims
                    np_anims.automatic()
                machine.freq(osc.SLOW_FREQ)
                bl_now = tft.get_backlight()
                tft.set_backlight(osc.LCD_POWER_SAVE_BL)
        else:
            machine.freq(osc.BASE_FREQ)
            tft.set_backlight(bl_now)
            now_time = time.ticks_ms()

    
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
            sleep(False)
            while button_c.value() == 0:
                time.sleep(osc.DEBOUNCE_TIME)
            didnt_choose = True
            chosen = True
        elif button_c.value() == 1 and bt3_d == 0:
            bt3_d = 1

        # Select    
        if button_a.value() == 0 and bt1_d == 1:
            sleep(False)
            while button_a.value() == 0:
                time.sleep(osc.DEBOUNCE_TIME)
            chosen = True
        elif button_a.value() == 1 and bt1_d == 0:
            bt1_d = 1
            
        # Cycle
        if button_b.value() == 0 and bt2_d == 1:
            sleep(False)
            while button_b.value() == 0:
                time.sleep(osc.DEBOUNCE_TIME)
            menu_down()
        elif button_b.value() == 1 and bt2_d == 0:
            bt2_d = 1
        
        # Cardkb arrow handler
        if osc.INPUT_METHOD == 2:
            
            # Down
            if arrow_down.value() == 0 and ar_dn_d == 1:
                sleep(False)
                while arrow_down.value() == 0:
                    time.sleep(osc.DEBOUNCE_TIME)
                menu_down()
            elif arrow_down.value() == 1 and ar_dn_d == 0:
                ar_dn_d = 1
                
            # Up
            if arrow_up.value() == 0 and ar_up_d == 1:
                sleep(False)
                while arrow_up.value() == 0:
                    time.sleep(osc.DEBOUNCE_TIME)
                menu_up()
            elif arrow_up.value() == 1 and ar_up_d == 0:
                ar_up_d = 1
                
            # Page right
            if arrow_right.value() == 0 and ar_rt_d == 1:
                sleep(False)
                while arrow_right.value() == 0:
                    time.sleep(osc.DEBOUNCE_TIME)
                page_right()
            elif arrow_right.value() == 1 and ar_rt_d == 0:
                ar_rt_d = 1
                
            # Page left
            if arrow_left.value() == 0 and ar_lt_d == 1:
                sleep(False)
                while arrow_left.value() == 0:
                    time.sleep(osc.DEBOUNCE_TIME)
                page_left()
            elif arrow_left.value() == 1 and ar_lt_d == 0:
                ar_lt_d = 1
        
        # Sleep timer
        if time.ticks_diff(time.ticks_ms(), now_time) > osc.POWER_SAVE_TIMEOUT and sleep_on == False and allow_saving == 1:
            sleep(True)
        
        # Refresh neopixel
        if osc.HAS_NEOPIXEL:
            import modules.neopixel_anims as np_anims
            np_anims.automatic()
            
        time.sleep(osc.LOOP_WAIT_TIME)
        
    gc.collect()
    # Return to starting frequency
    ps.set_freq(curr_freq)
    
    if didnt_choose == True:
        return None
    else:
        choicef = pages[curr_page][choice - 1][1]
        return choicef