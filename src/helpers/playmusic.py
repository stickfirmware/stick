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
    
def openFile(path):
    import apps.player as player
    player.set_btf(button_a, button_b, button_c, tft)
    player.play(path)
