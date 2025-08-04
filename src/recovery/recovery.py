import esp32

import modules.nvs as nvs
from modules.decache import decache

print("Init IO manager")
import modules.io_manager as io_man
if io_man.get('tft') != None:
    tft = io_man.get('tft')
else:
    import modules.tft_init as tft_init
    tft = tft_init.init_tft()

import modules.button_init as btn_init
buttons = btn_init.init_buttons()
button_a = buttons[0]
button_b = buttons[1]
button_c = buttons[2]
io_man.set('button_a', button_a)
io_man.set('button_b', button_b)
io_man.set('button_c', button_c)
io_man.set('tft', tft)

import machine
import modules.menus as menus

while True:
    render = menus.menu("Recovery menu", [("Factory reset", 1), ("File explorer", 5), ("Toggle dev apps", 6), ("Reboot", 13)])
    if render == 1:
        confirm_reset = menus.menu("Reset all settings?", [("No", None), ("Yes", 1)])
        if confirm_reset == 1:
            confirm_reset = menus.menu("It removes all files!", [("Cancel", 2), ("Confirm", 1)])
            if confirm_reset == 1:
                n_updates = esp32.NVS("updates")
                nvs.set_int(n_updates, "factory", 1)
                machine.reset()
    elif render == 5:
        import modules.file_explorer as a_fe
        a_fe.run()
        decache('modules.file_explorer')
        del a_fe
    elif render == 6:
        n_settings = esp32.NVS("settings")
        dev_settings = nvs.get_int(n_settings, "dev_apps")
        if dev_settings == 1:
            nvs.set_int(n_settings, "dev_apps", 0)
        else:
            nvs.set_int(n_settings, "dev_apps", 1)
    elif render == 13:
        machine.reset()