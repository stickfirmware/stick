import os

import modules.json as jso

def createConfig():
    appsConfig = {
            "apps": [
                {
                    "name": "Run in file reader",
                    "id": "com.kitki30.filereader",
                    "file": "helpers.run_in_reader",
                    "hidden": True,
                    "handleExtensions": ["*"]
                    },
                {
                    "name": "Play music",
                    "id": "com.kitki30.musicplayer",
                    "file": "helpers.play_music",
                    "hidden": True,
                    "handleExtensions": ["*.wav"]
                    },
                {
                    "name": "Run in Python executor",
                    "id": "com.kitki30.pythonexec",
                    "file": "helpers.python_exec",
                    "hidden": True,
                    "handleExtensions": ["*.py"]
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