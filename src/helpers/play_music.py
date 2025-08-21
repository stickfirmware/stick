import modules.os_constants as osc
import modules.popup as popup

def open_file(path):
    if not osc.HAS_SPEAKER:
        popup.show("Speaker was not detected in your device, music player is not supported.", "Error", 10)
        return
    import apps.player as player
    player.play(path)
