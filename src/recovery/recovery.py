import machine

import modules.button_init as btn_init
import modules.cache as cache
import modules.io_manager as io_man
import modules.menus as menus
import modules.nvs as nvs
import modules.os_constants as osc
import modules.popup as popup
from modules.decache import decache
from modules.printer import log

log("Init IO manager")
if io_man.get('tft') is not None:
    tft = io_man.get('tft')
else:
    import modules.tft_init as tft_init
    tft = tft_init.init_tft()

buttons = btn_init.init_buttons()
button_a = buttons[0]
button_b = buttons[1]
button_c = buttons[2]
io_man.set('button_a', button_a)
io_man.set('button_b', button_b)
io_man.set('button_c', button_c)
io_man.set('tft', tft)

while True:
    render = menus.menu("Recovery menu", [("Factory reset", 1), ("File explorer", 2), ("Toggle dev apps", 3), ("Disable custom SD", 4), ("Mount sd card", 5), ("Reboot", 13)])
    if render == 1:
        confirm_reset = menus.menu("Reset all settings?", [("No", None), ("Yes", 1)])
        if confirm_reset == 1:
            confirm_reset = menus.menu("It removes all files!", [("Cancel", 2), ("Confirm", 1)])
            if confirm_reset == 1:
                n_updates = cache.get_nvs('updates')
                nvs.set_int(n_updates, "factory", 1)
                machine.reset()
    elif render == 2:
        popup.show("To run file explorer properly, I will need to load english translation. Make sure it is working, or else you can expect crashes/freezes.")
        import modules.translate as translate
        translate.load("en")
        import modules.file_explorer as a_fe
        a_fe.run()
        decache('modules.file_explorer')
        del a_fe
    elif render == 3:
        n_settings = cache.get_nvs('settings')
        dev_settings = nvs.get_int(n_settings, "dev_apps")
        if dev_settings == 1:
            nvs.set_int(n_settings, "dev_apps", 0)
        else:
            nvs.set_int(n_settings, "dev_apps", 1)
    elif render == 4:
        n_settings = cache.get_nvs('settings')
        nvs.set_int(n_settings, "sd_overwrite", 0)
    elif render == 5:
        try:
            import modules.sdcard as sd
            sd.init(2, osc.SD_CLK, osc.SD_CS, osc.SD_MISO, osc.SD_MOSI)
            sd.mount()
        except Exception as e:
            popup.show(f"Error mounting SD card.\nDoes your device have sdcard slot?\nCustom sd card is not currently supported here!\nError msg:\n{str(e)}", "Error", 10)
    elif render == 13:
        machine.reset()