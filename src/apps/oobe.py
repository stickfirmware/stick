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
                    "handleExtensions": ["*.json", "*.wav"]
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