"""
Context menu helper for music player
"""

import modules.os_constants as osc
import modules.popup as popup
from modules.translate import get as l_get

def open_file(path):
    if not osc.HAS_SPEAKER:
        popup.show(l_get("apps.music_player.no_speaker_popup"),
                   l_get("crashes.error"),
                   10)
        return
    import apps.player as player
    player.play(path)
