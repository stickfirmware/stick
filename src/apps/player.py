import fonts.def_8x8 as f8x8
import fonts.def_16x32 as f16x32
import modules.menus as menus
import modules.nvs as nvs
import esp32
import os
import gc

from modules.buzzer_music import music
from time import sleep

from machine import Pin
import modules.json as json

n_settings = esp32.NVS("settings")
    
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

    
def skeleton(text="Music Player"):
    tft.fill_rect(0, 0, 240, 3, 65535)
    tft.fill_rect(0, 16, 240, 3, 65535)
    tft.fill_rect(0, 132, 240, 3, 65535)
    tft.fill_rect(0, 0, 3, 135, 65535)
    tft.fill_rect(237, 0, 3, 135, 65535)
    tft.fill_rect(3, 3, 234, 13, 0)
    tft.fill_rect(3, 19, 234, 113, 0)
    tft.text(f8x8, text,5,5,65535)
    
def about():
    skeleton("About")
    tft.text(f16x32, "Music Player",5,20,1984)
    tft.text(f8x8, "MIT License",5,52,65535)
    tft.text(f8x8, "Used libraries:",5,62,65535)
    tft.text(f8x8, "buzzer_music - MIT License",5,70,65535)
    tft.text(f8x8, "For more see CREDITS file",5,78,65535)
    tft.text(f8x8, "Press button A to exit!",5,124,65535)
    while button_a.value() == 1:
        sleep(0.02)
    while button_a.value() == 0:
        sleep(0.02)
        
def play(path):
    tft.fill(0)
    tft.text(f8x8, "Loading...",0,0,65535)
    vol = nvs.get_float(n_settings, "volume")
    song = json.read(path)
    tft.fill(0)
    skeleton()
    tft.text(f8x8, song["name"],5,20,65535)
    tft.text(f8x8, "Looping?: " + str(song["looping"]),5,28,65535)
    tft.text(f8x8, "Volume: " + str(vol),5,36,65535)
    tft.text(f8x8, "Press button A to exit!",5,124,65535)
    
    playSong = music(song["song"], pins=[Pin(2)], looping=song["looping"], duty=int(65536*vol))
    
    playing = True
    while playing == True and button_a.value() == 1:
        playing = playSong.tick()
        sleep(0.04)
    playSong.stop()
    del playSong
    del song
    gc.collect()
        
def listMusic():
    music = os.listdir("/usr/music")
    music_menu = []
    index = 0
    for i in music:
        if i.endswith(".json"):
            music_menu.append((str(i), index))
        index += 1
    if len(music_menu) == 0:
        tft.fill(0)
        tft.text(f8x8, "No music found!",0,0,65535)
        sleep(1)
        return
    render = menus.menu("Music list", music_menu)
    if render == None:
        return
    else:
        if os.stat("/usr/music/"+music[render])[6] <= gc.mem_free() // 2:
            play("/usr/music/" + music[render])
        else:
            tft.fill(0)
            gc.collect()
            tft.text(f8x8, "The file size is too high!",0,0,65535)
            tft.text(f8x8, "Try emptying the RAM or trim",0,8,65535)
            tft.text(f8x8, "the file in 'song' line.",0,8,65535)
            sleep(1)
            return
            
    
def run():
    import sys
    work = True
    while work == True:
        render = menus.menu("Music Player", [("List songs", 1), ("Browse music in explorer", 4), ("About", 2), ("Exit", 3)])
        try:
            if render == 3:
                work = False
            elif render == 2:
                about()
            elif render == 1:
                listMusic()
            elif render == 4:
                import modules.fileexplorer as a_fe
                a_fe.set_btf(button_a, button_b, button_c, tft)
                browser = a_fe.run(True)
                if browser != None:
                    play(browser)
                del a_fe
                sys.modules.pop('modules.fileexplorer', None)
            else:
                work = False
        except Exception as e:
            print("Oops!\nSomething wrong has happened in Music Player\nLogs:\n"+str(e))
            tft.fill(0)
            gc.collect()
            tft.text(f16x32, "Oops!",0,0,1984)
            tft.text(f8x8, "Something wrong has happened!",0,32,65535)
            tft.text(f8x8, "Please try again!",0,40,65535)
            sleep(3)
            work = False