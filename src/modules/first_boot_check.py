import esp32
import machine

import modules.nvs as nvs

import fonts.def_8x8 as f8x8
import fonts.def_16x16 as f16x16

import modules.printer as printer

def check(tft):
    import fonts.def_8x8 as f8x8
    n_boot = esp32.NVS("boot")
    if nvs.get_int(n_boot, "firstBoot") == None:
        n_settings = esp32.NVS("settings")
        printer.log("Devices first boot, configuring NVS.")
        tft.fill(0)
        tft.text(f16x16, "Stick firmware",0,0,65535,0)
        tft.text(f8x8, "First boot configuration!",0,16,65535,0)
        tft.text(f8x8, "Please wait...",0,24,65535,0)
    
        # Boot config
        printer.log("Configuring 'boot' NVS")
        nvs.set_int(n_boot, "firstBoot", 1)
        printer.log("boot:firstBoot:1")
        tft.text(f8x8, "boot:firstBoot:1",0,34,65535,0)
        
        import apps.oobe as oobe
        oobe.createUserFolder()
        oobe.createConfig()
    
        printer.log("Doing soft reset")
        tft.text(f8x8, "Doing soft reset. Bye!",0,127,65535,0)
        machine.soft_reset()