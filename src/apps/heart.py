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

def run():
    import fonts.def_8x8 as f8x8
    import time
    tft.fill(0)
    work = True
    try:
        import modules.UNIT.heart as heart
    except Exception as e:
        print(str(e))
        work = False
        tft.text(f8x8, "Please connect unit",0,0,65535)
        tft.text(f8x8, "heart module first!",0,8,65535)
        time.sleep(2)
        
    while button_b.value() == 1 and work == True:
        tft.fill_rect(0, 0, 60, 240, 0)
        try:
            tft.text(f8x8, "Measuring...",0,16,65535)
            data = heart.check()
        except Exception as e:
            print(str(e))
            work = False
            tft.text(f8x8, "Please connect unit",0,0,65535)
            tft.text(f8x8, "heart module first!",0,8,65535)
        tft.text(f8x8, "Heartrate: " + data[1] + " bpm",0,0,63488)
        tft.text(f8x8, "SPO2: " + data[0] + "%",0,8,1279)
        tft.text(f8x8, "Hold button B to exit",0,48,65535)