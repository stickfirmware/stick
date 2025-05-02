import fonts.def_8x8 as f8x8
import time

button_a = None
button_b = None
button_c = None
tft = None

def set_btf(bta, btb, btc, ttft):
    global button_a
    global button_b
    global button_c
    global tft
    
    button_a = bta
    button_b = btb
    button_c = btc
    tft = ttft

def menu(name, choices):
    import bitmaps.menubase as b_menubase
    tft.bitmap(b_menubase, 0,0)
    tft.text(f8x8, str(name),5,5,65535)
    lcd_space = 13
    lcd_left = 104
    lcd_curr = 25
    for name, val in choices:
        if lcd_space == 0:
            break  # zatrzymaj wypisywanie jeśli brak miejsca
        tft.text(f8x8, str(name), 25, lcd_curr, 65535)
        lcd_curr += 8
        lcd_space -= 1
    choice = 1
    didnt_choose = False
    update = True
    chosen = False
    bt1_d = button_a.value()
    bt2_d = button_b.value()
    bt3_d = button_c.value()
    while chosen == False:
        if update == True:
            if choice == 1:
                tft.text(f8x8, " ",15,(17 + (len(choices) * 8)),49081)
            else:
                tft.text(f8x8, " ",15,(17 + (choice * 8) - 8),49081)
            tft.text(f8x8, ">",15,(17 + (choice * 8)),20365)
            update = False
            
        if button_c.value() == 0 and bt3_d == 1:
            while button_c.value() == 0:
                time.sleep(0.02)
            didnt_choose = True
            chosen = True
        elif button_c.value() == 1 and bt3_d == 0:
            bt3_d = 1
            
        if button_a.value() == 0 and bt1_d == 1:
            while button_a.value() == 0:
                time.sleep(0.02)
            chosen = True
        elif button_a.value() == 1 and bt1_d == 0:
            bt1_d = 1
            
        if button_b.value() == 0 and bt2_d == 1:
            while button_b.value() == 0:
                time.sleep(0.02)
            if choice == len(choices):
                choice = 1
            else:
                choice += 1
            update = True
        elif button_b.value() == 1 and bt2_d == 0:
            bt2_d = 1
        
        time.sleep(0.02)
        
    if didnt_choose == True:
        return None
    else:
        choicef = choices[choice - 1][1]
        return choicef