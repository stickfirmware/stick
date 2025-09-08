import modules.nvs as nvs
import modules.cache as cache
import modules.printer as printer

def check():
    n_boot = cache.get_nvs("boot")
    if nvs.get_int(n_boot, "firstBoot") == None:
        printer.log("Devices first boot, configuring NVS.")
    
        # Boot config
        printer.log("Configuring 'boot' NVS")
        nvs.set_int(n_boot, "firstBoot", 1)
        printer.log("boot:firstBoot:1")
        
        import apps.oobe as oobe
        oobe.createUserFolder()
        oobe.createConfig()