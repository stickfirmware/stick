import os

import modules.json as jso
import modules.cache as cache
from modules.translate import get as l_get

_APPS_JSON_PATH = "/usr/config/apps.json"
_LAST_UPDATED_TIME = 0

# Get apps config
def app_config_translated():
    appsConfig = {
            "apps": [
                {
                    "name": l_get("apps.file_reader.context_menu_text"),
                    "id": "com.kitki30.filereader",
                    "file": "helpers.run_in_reader",
                    "main_folder": "",
                    "is_system_app": True,
                    "dependency": False,
                    "hidden": True,
                    "handleExtensions": ["*"]
                    },
                {
                    "name": l_get("apps.music_player.context_menu_text"),
                    "id": "com.kitki30.musicplayer",
                    "file": "helpers.play_music",
                    "main_folder": "",
                    "is_system_app": True,
                    "dependency": False,
                    "hidden": True,
                    "handleExtensions": ["*.wav"]
                    },
                {
                    "name": l_get("apps.app_installer.context_menu_text"),
                    "id": "com.kitki30.packinstaller",
                    "file": "modules.handle_apps",
                    "main_folder": "",
                    "is_system_app": True,
                    "dependency": True,
                    "hidden": True,
                    "handleExtensions": ["*.zip", "*.stk"]
                    },
                {
                    "name": l_get("apps.python_executor.context_menu_text"),
                    "id": "com.kitki30.pythonexec",
                    "file": "helpers.python_exec",
                    "main_folder": "",
                    "is_system_app": True,
                    "dependency": False,
                    "hidden": True,
                    "handleExtensions": ["*.py"]
                    },
                {
                    "name": l_get("apps.ir_remote.name"),
                    "id": "com.kitki30.ir_remote",
                    "file": "apps.com_kitki30_ir_remote.IR",
                    "main_folder": "/apps/com_kitki30_ir_remote",
                    "is_system_app": True,
                    "dependency": False,
                    "hidden": False,
                    "handleExtensions": [""]
                    },
                {
                    "name": l_get("apps.file_explorer.name"),
                    "id": "com.kitki30.file_explorer",
                    "file": "apps.com_kitki30_file_explorer.explorer",
                    "main_folder": "/apps/com_kitki30_file_explorer",
                    "is_system_app": True,
                    "dependency": False,
                    "hidden": False,
                    "handleExtensions": [""]
                    },
                {
                    "name": l_get("apps.flashlight.name"),
                    "id": "com.kitki30.flashlight",
                    "file": "apps.com_kitki30_flashlight.flashlight",
                    "main_folder": "/apps/com_kitki30_flashlight",
                    "is_system_app": True,
                    "dependency": False,
                    "hidden": False,
                    "handleExtensions": [""]
                    },
                {
                    "name": l_get("apps.ir_remote.context_menu"),
                    "id": "com.kitki30.ir_helper",
                    "file": "helpers.ir_sender",
                    "main_folder": "",
                    "is_system_app": True,
                    "dependency": False,
                    "hidden": True,
                    "handleExtensions": ["*.ir"]
                    },
                {
                    "name": l_get("apps.package_manager.name"),
                    "id": "com.kitki30.pacman",
                    "file": "apps.com_kitki30_pacman.package_manager",
                    "main_folder": "/apps/com_kitki30_pacman",
                    "is_system_app": True,
                    "dependency": False,
                    "hidden": False,
                    "handleExtensions": [""]
                    }
                ]
        }
    return appsConfig

# Create starting config
def createConfig():
    jso.write(_APPS_JSON_PATH, app_config_translated())
    cache.reload_apps()
    
# Read app config
def read_config(bypass_cache=False):
    global _LAST_UPDATED_TIME
    if cache.get("app_config_last_modify") != _LAST_UPDATED_TIME or bypass_cache:
        config = jso.read(_APPS_JSON_PATH)
        _LAST_UPDATED_TIME =  cache.update_last_mod()
        return config
    else:
        return cache.get("app_config")
    
# Sync apps with actual ones
def sync_apps():
    config = read_config()
    apps = config.setdefault("apps", [])
    app_map = {app["id"]: app for app in apps}
    
    for new_app in app_config_translated()["apps"]:
        app_id = new_app["id"]
        if app_id in app_map:
            app_map[app_id].update(new_app)
        else:
            apps.append(new_app)
    
    jso.write(_APPS_JSON_PATH, config)
    cache.reload_apps()
    
# Edit app, example usage: edit_app("com.kitki30.musicplayer", name="Play music", handleExtensions=["*.wav", "*.mp3"])
def edit_app(app_id, **changes):
    try:
        config = read_config()
    except Exception:
        return False

    found = False
    for app in config.get("apps", []):
        if app.get("id") == app_id:
            for key, value in changes.items():
                app[key] = value
            found = True
            break

    if not found:
        new_app = {"id": app_id}
        new_app.update(changes)
        config.setdefault("apps", []).append(new_app)

    jso.write(_APPS_JSON_PATH, config)
    cache.reload_apps()
    return True

def get_entry(id, key):
    for app in read_config().get("apps", []):
        if app.get("id") == id:
            return app.get(str(key))
    return None

# Remove app from config by id
def remove_app(id):
    new_apps = []
    conf = read_config()

    # Filter out app id, leave apps that don't match
    for app in conf["apps"]:
        if app["id"] != id:
            new_apps.append(app)

    # Write new onfig
    conf["apps"] = new_apps
    jso.write(_APPS_JSON_PATH, conf)
    cache.reload_apps()
    
# Create user
def createUserFolder():
    if "usr" not in os.listdir("/"):
        os.mkdir("/usr")
        os.mkdir("/usr/ir")
        os.mkdir("/usr/music")
        os.mkdir("/usr/config")
        return True
    return False