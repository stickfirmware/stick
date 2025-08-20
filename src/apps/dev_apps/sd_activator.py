import modules.os_constants as osc
import modules.cache as cache
import modules.nvs as nvs
import modules.popup as popup
import modules.menus as menus
import modules.numpad as keypad

# Overwrite SD Card config from osc, so you can use custom one (ex. M5Stick)
def run():
    
    # Check if activator needed
    n_settings = cache.get_nvs('settings')
    if nvs.get_int(n_settings, "sd_overwrite") == 1:
        popup.show("SD Card Activator is already configured. You first need to disable it", "Info", 10)
        disable = menus.menu("SD Card Activator", [("Disable custom SD", 1), ("Close", None)])
        if disable == 1:
            nvs.set_int(n_settings, "sd_overwrite", 0)
            popup.show("SD Card Activator was disabled.", "Info", 10)
        return
    if osc.HAS_SD_SLOT:
        popup.show("SD Card Activator is not needed. Your config has SD Card Slot setup.", "Info", 10)
        return
    
    # Confirmation
    popup.show("SD Card Activator is used to setup developer SD Card slot in your device. Make sure you now what you are doing, or else your device can be stuck in a bootloop", "Info")
    popup.show("Make sure you downloaded sdcard.py module from our repo to /modules/sdcard.py (or sdcard.mpy), or else you will get a BSOD.", "Info")
    popup.show("This feature is experimental and is not guaranted to work!", "Info")
    confirmation = menus.menu("Continue?", [("Yes", 1), ("No", None)])
    if confirmation != 1:
        return
    
    # Get pins from user input
    SD_CLK = keypad.numpad("Enter SD CLK pin", maxlen=2)
    SD_CS = keypad.numpad("Enter CS pin or 99 if none", maxlen=2)
    SD_MOSI = keypad.numpad("Enter MOSI pin", maxlen=2)
    SD_MISO = keypad.numpad("Enter MISO pin", maxlen=2)
    if SD_CS == "99":
        CS_TEXT = "None (Short to GND)"
    else:
        CS_TEXT = str(SD_CS)
        
    # Show configuration and ask for confirmation
    popup.show(f"Your configuration:\nCLK: {SD_CLK}\nCS: {CS_TEXT}\nMOSI: {SD_MOSI}\nMISO: {SD_MISO}", "Info")
    confirmation = menus.menu("Is this correct?", [("Yes", 1), ("No", None)])
    if confirmation != 1:
        return
    
    # Check automount
    auto_mount = menus.menu("Auto mount SD Card?", [("Yes", 1), ("No", None)])
    if auto_mount == 1:
        auto_mount = 1
    else:
        auto_mount = 0

    # Save configuration
    nvs.set_int(n_settings, "sd_overwrite", 1)
    nvs.set_int(n_settings, "sd_clk", int(SD_CLK))
    if SD_CS == "99":
        nvs.set_int(n_settings, "sd_use_cs", 0)
    else:
        nvs.set_int(n_settings, "sd_use_cs", 1)
        nvs.set_int(n_settings, "sd_cs", int(SD_CS))
    nvs.set_int(n_settings, "sd_mosi", int(SD_MOSI))
    nvs.set_int(n_settings, "sd_miso", int(SD_MISO))
    nvs.set_int(n_settings, "sd_automount", auto_mount)
    popup.show("Config saved, go to settings to mount.", "Info")
    popup.show("If something bad happens go to recovery to disable custom SD. Hold button B (on stick), or G0 (on cardputer), just after you enable power.", "Info")
    