# Score keeper app
# App ID: 1001

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
    import modules.menus as menus
    import modules.nvs as nvs
    import esp32
    import machine
    import modules.osconstants as osc
    
    machine.freq(osc.ULTRA_FREQ)
    
    app_storage = esp32.NVS("apps_1001")
    
    if tft == None:
        print("Please call 'set_btf(bta. btb, btc, ttft)' first")
        return
    
    print("Going into main loop")
    
    team1 = 0
    team2 = 0
    
    t1_nvs = nvs.get_int(app_storage, "team1")
    t2_nvs = nvs.get_int(app_storage, "team2")
    if t1_nvs != None:
        team1 = t1_nvs
    else:
        nvs.set_int(app_storage, "team1", 0)
    if t2_nvs != None:
        team2 = t2_nvs
    else:
        nvs.set_int(app_storage, "team2", 0)
    
    work = True
    while work == True:
        render = menus.menu("Scorekeeper", [("Team 1: " + str(team1), 1), ("Team 2: " + str(team2), 2), ("Reset", 3), ("Close", 4)])
        if render == 1:
            team1 += 1
        elif render == 2:
            team2 += 1
        elif render == 3:
            team1 = 0
            team2 = 0
        else:
            work = False
    
    nvs.set_int(app_storage, "team1", team1)
    nvs.set_int(app_storage, "team2", team2)
        
