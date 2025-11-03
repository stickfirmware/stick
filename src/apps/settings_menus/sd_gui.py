"""
SD Card settings GUI
"""

import time

import fonts.def_8x8 as f8x8
import modules.cache as cache
import modules.io_manager as io_man
import modules.menus as menus
import modules.nvs as nvs
import modules.os_constants as osc
from modules.translate import get as l_get


def run():
    """SD Card settings GUI"""
    tft = io_man.get("tft")
    n_settings = cache.get_nvs("settings")
    
    import modules.sdcard as sd
            
    # SD Card menu if SD is not mounted
    if sd.sd is None:
        sd_menu = menus.menu(l_get("apps.settings.sd.title"),
                                [(l_get("apps.settings.sd.init"), 1),
                                (l_get("menus.menu_close"), 13)])
        if sd_menu == 1:
            tft.fill(0)
            tft.text(f8x8, l_get("apps.settings.sd.init_load"),0,0, 65535)
            if nvs.get_int(n_settings, "sd_overwrite") == 1 and nvs.get_int(n_settings, "sd_automount") == 1:
                cs = nvs.get_int(n_settings, "sd_cs")
                if cs == 99:
                    cs = None
                sdin = sd.init(2, nvs.get_int(n_settings, "sd_clk"), cs, nvs.get_int(n_settings, "sd_miso"), nvs.get_int(n_settings, "sd_mosi"))
            else:
                sdin = sd.init(2, osc.SD_CLK, osc.SD_CS, osc.SD_MISO, osc.SD_MOSI)
            time.sleep(2)
            if sdin:
                if sd.mount():
                    tft.text(f8x8, l_get("apps.settings.sd.done"),0,8, 65535)
                else:
                    tft.text(f8x8, l_get("apps.settings.sd.failed"),0,8, 65535)
            else:
                tft.text(f8x8, l_get("apps.settings.sd.failed"),0,8, 65535)
            time.sleep(2)
            
    # Menu if SD is mounted
    else:
        sd_menu = menus.menu(l_get("apps.settings.sd.title"),
                                [(l_get("apps.settings.sd.unmount"), 1),
                                (l_get("menus.menu_close"), 13)])
        if sd_menu == 1:
            tft.fill(0)
            tft.text(f8x8, l_get("apps.settings.sd.unmount_load"),0,0, 65535)
            sdin = sd.umount()
            if sdin:
                tft.text(f8x8, l_get("apps.settings.sd.done"),0,8, 65535)
                sd.sd = None
            else:
                tft.text(f8x8, l_get("apps.settings.sd.failed"),0,8, 65535)
            time.sleep(2)