from machine import Pin
import time

import modules.os_constants as osc

aa_toggle_state = False
aa_debounce = False

if osc.INPUT_METHOD == 2:
    A0 = Pin(8, Pin.OUT)
    A1 = Pin(9, Pin.OUT)
    A2 = Pin(11, Pin.OUT)
            
    col_pins_nums = [13,15,3,4,5,6,7]
    cols = [Pin(pin_num, Pin.IN, Pin.PULL_UP) for pin_num in col_pins_nums]

def set_decoder(val):
    A0.value(val & 0x01)
    A1.value((val >> 1) & 0x01)
    A2.value((val >> 2) & 0x01)

def scan_keyboard():
    matrix = [[False]*14 for _ in range(4)]
    
    for dec_out in range(8):
        set_decoder(dec_out)
        time.sleep_us(10)
        
        if dec_out >= 4:
            row = 7 - dec_out 
            col_offset = 0 
        else:
            row = 3 - dec_out
            col_offset = 1
        
        for idx, pin in enumerate(cols):
            val = not pin.value()
            
            col = idx * 2 + col_offset
            
            if col < 14:
                matrix[row][col] = val
    
    return matrix

keymap_normal = [
    ['`','1','2','3','4','5','6','7','8','9','0','_','=','backspace'],
    ['tab','q','w','e','r','t','y','u','i','o','p','[',']','\\'],
    ['fn','Aa','a','s','d','f','g','h','j','k','l',';',"'",'enter'],
    ['ctrl','opt','alt','z','x','c','v','b','n','m',',','.','/',' ']
]

keymap_Aa = [
    ['~','!','@','#','$','%','^','&','*','(',')','-','+','backspace'],
    ['tab','Q','W','E','R','T','Y','U','I','O','P','{','}','|'],
    ['fn','Aa','A','S','D','F','G','H','J','K','L',':','"','enter'],
    ['ctrl','opt','alt','Z','X','C','V','B','N','M','<','>','?',' ']
]

def scan_and_map():
    global aa_toggle_state, aa_debounce

    matrix = scan_keyboard()
    keymap = keymap_Aa if aa_toggle_state else keymap_normal

    pressed_keys = []
    for r in range(4):
        for c in range(14):
            if matrix[r][c]:
                pressed_keys.append(keymap[r][c])
                
    if "Aa" in pressed_keys:
        if not aa_debounce:
            aa_toggle_state = not aa_toggle_state
            aa_debounce = True
        return []
    else:
        aa_debounce = False

    return pressed_keys


class buttonemu:
    def __init__(self, btn):
        self.btn = btn
    def value(self):
        scan = scan_and_map()
        if any(b in scan for b in self.btn):
            return 0
        else:
            return 1