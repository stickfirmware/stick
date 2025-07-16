import os
import fonts.def_8x8 as f8x8
import modules.json as jso
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

def createConfig():
    appsConfig = {
            "apps": [
                {
                    "name": "Run in file reader",
                    "id": "com.kitki30.filereader",
                    "file": "helpers.runinreader",
                    "hidden": True,
                    "handleExtensions": ["*"]
                    },
                {
                    "name": "Play music",
                    "id": "com.kitki30.musicplayer",
                    "file": "helpers.playmusic",
                    "hidden": True,
                    "handleExtensions": ["*.json", "*.music"]
                    },
                {
                    "name": "Run in Python executor",
                    "id": "com.kitki30.pythonexec",
                    "file": "helpers.pythonexec",
                    "hidden": True,
                    "handleExtensions": ["*.py", "*.pyw"]
                    }
                ]
        }
    jso.write("/usr/config/apps.json", appsConfig)
    
def createUserFolder():
    if "usr" not in os.listdir("/"):
        os.mkdir("/usr")
        os.mkdir("/usr/ir")
        os.mkdir("/usr/music")
        os.mkdir("/usr/config")
        return True
    return False

def draw_stick(offset_x=0, offset_y=0, m5_color=58564, size=1.0):
    def sc(val): return int(val * size)  # skalowanie na int dla TFT

    # Stick
    tft.fill_rect(int(offset_x), int(offset_y), sc(120), sc(70), m5_color)

    # Button
    tft.fill_rect(int(offset_x + sc(15)), int(offset_y + sc(10)), sc(20), sc(3), 0)
    tft.fill_rect(int(offset_x + sc(15)), int(offset_y + sc(60)), sc(20), sc(3), 0)
    tft.fill_rect(int(offset_x + sc(32)), int(offset_y + sc(10)), sc(3), sc(50), 0)

    # M5 Text
    text = "M5"
    text_w = len(text) * 8
    text_h = 8
    center_x = offset_x + sc(15) + sc(20) / 2
    center_y = offset_y + sc(10) + sc(50) / 2
    text_x = int(center_x - text_w / 2)
    text_y = int(center_y - text_h / 2)
    tft.text(f8x8, text, text_x, text_y, 0, m5_color)

    # Screen
    tft.fill_rect(int(offset_x + sc(45)), int(offset_y + sc(10)), sc(70), sc(53), 0)
        
def run():
    if createUserFolder():
        createConfig()
    tft.fill(0)
    tft.text(f8x8, "Welcome!", 0, 0, 58564)
    tft.text(f8x8, "Press M5 to continue!", 0, 127, 58564)
    stick_w = 120 * 1.2
    stick_h = 70 * 1.2
    offset_x = (240 - stick_w) // 2
    offset_y = (135 - stick_h) // 2

    draw_stick(offset_x, offset_y, size = 1.2)
    
    while button_a.value() == 1:
        time.sleep(0.025)
        
    tft.fill(0)