import os
import modules.json as jso

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
        