button_a = None
button_b = None
button_c = None
tft = None

import fonts.def_8x8 as f8x8
import fonts.def_8x16 as f8x16
import fonts.def_16x16 as f16x16

def set_btf(bta, btb, btc, ttft):
    global button_a
    global button_b
    global button_c
    global tft
    
    button_a = bta
    button_b = btb
    button_c = btc
    tft = ttft

def writeNums(number=99):
    n = [65535, 65535, 65535, 65535, 65535, 65535, 65535, 65535, 65535, 65535, 65535, 65535]
    
    if not number == 99:
        n[number] = 10208
    
    # Row 1
    tft.text(f16x16, "|",45,43,65535)
    tft.text(f16x16, "1",65,43,n[0])
    tft.text(f16x16, "|",85,43,65535)
    tft.text(f16x16, "2",105,43,n[1])
    tft.text(f16x16, "|",125,43,65535)
    tft.text(f16x16, "3",145,43,n[2])
    tft.text(f16x16, "|",165,43,65535)
    
    # Row 2
    tft.text(f16x16, "|",45,59,65535)
    tft.text(f16x16, "4",65,59,n[3])
    tft.text(f16x16, "|",85,59,65535)
    tft.text(f16x16, "5",105,59,n[4])
    tft.text(f16x16, "|",125,59,65535)
    tft.text(f16x16, "6",145,59,n[5])
    tft.text(f16x16, "|",165,59,65535)
    
    # Row 3
    tft.text(f16x16, "|",45,75,65535)
    tft.text(f16x16, "7",65,75,n[6])
    tft.text(f16x16, "|",85,75,65535)
    tft.text(f16x16, "8",105,75,n[7])
    tft.text(f16x16, "|",125,75,65535)
    tft.text(f16x16, "9",145,75,n[8])
    tft.text(f16x16, "|",165,75,65535)
    
    # Row 4
    tft.text(f16x16, "|",45,91,65535)
    tft.text(f16x16, ">",65,91,n[9])
    tft.text(f16x16, "|",85,91,65535)
    tft.text(f16x16, "0",105,91,n[10])
    tft.text(f16x16, "|",125,91,65535)
    tft.text(f16x16, "X",145,91,n[11])
    tft.text(f16x16, "|",165,91,65535)

def numpad(title, maxnumber=0, hideInput=False):
    import time
    tft.fill(0)
    tft.fill_rect(0, 0, 240, 3, 65535)
    tft.fill_rect(0, 132, 240, 3, 65535)
    tft.fill_rect(0, 0, 3, 135, 65535)
    tft.fill_rect(237, 0, 3, 135, 65535)
    tft.fill_rect(3, 3, 234, 13, 0)
    tft.fill_rect(3, 19, 234, 113, 0)
    
    tft.fill_rect(0, 16, 240, 3, 65535)
    tft.text(f8x8, str(title),5,5,65535)
    
    inp = ""
    selection = 0
    tft.fill_rect(0, 39, 240, 3, 65535)
    tft.text(f8x16, str(inp),5,22,65535)
    
    writeNums(selection)
    
    upd = True
    work = True
    while work == True:
        time.sleep(0.02)
        if upd == True:
            writeNums(selection)
            tft.fill_rect(3, 19, 234, 20, 0)
            chunks = [inp[i:i+28] for i in range(0, len(inp), 28)]
            last_chunk = chunks[-1] if chunks else ""
            if hideInput == False:
                tft.text(f8x16, last_chunk, 5, 22, 65535)
            else:
                tft.text(f8x16, str("*" * len(last_chunk)),5,22,65535)
            upd = False
        if button_b.value() == 0:
            while button_b.value() == 0:
                time.sleep(0.02)
            if selection == 11:
                selection = 0
            else:
                selection += 1
            upd = True
        elif button_a.value() == 0:
            while button_a.value() == 0:
                time.sleep(0.02)
            if selection == 11:
                selection = 0
                inp = None
                work = False
            elif selection == 9:
                selection = 0
                work = False
            elif selection == 10:
                upd = True
                selection = 0
                if maxnumber == 0:
                    inp += str(0)
                else:
                    if len(inp) < maxnumber:
                        inp += str(0)
            else:
                upd = True
                print(selection)
                if maxnumber == 0:
                    inp += str(selection + 1)
                else:
                    if len(inp) < maxnumber:
                        inp += str(selection + 1)
                selection = 0
        elif button_c.value() == 0:
            while button_c.value() == 0:
                time.sleep(0.02)
            if len(inp) == 0:
                selection = 0
                inp = None
                work = False
            else:
                inp = inp[:-1]
            upd = True
    return inp