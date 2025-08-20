import time

import modules.api as api
import modules.wifi_master as wifi_master
import modules.io_manager as io_man
import modules.os_constants as osc

# Link account to the device, for now doesnt work
# will be replaced with a proper module in the future
def link():
    import modules.menus as menus
    import modules.button_combos as button_combos
    
    import fonts.def_8x8 as f8x8
    import fonts.def_16x16 as f16x16
    
    tft = io_man.get("tft")
    
    # Wifi checker / Popup if no wifi
    if wifi_master.is_connected() == False:
        tft.fill(0)
        tft.text(f16x16, "Wifi", 0, 0, 65535)
        tft.text(f8x8, "Please connect to wifi first!", 0, 16, 65535)
        tft.text(f8x8, "You can return here by going:", 0, 24, 65535)
        tft.text(f8x8, "Settings > Account > Link", 0, 32, 65535)
        tft.text(f8x8, "Press any button to continue", 0, 40, 65535)

        while button_combos.any_btn(['a', 'b', 'c']) == False:
            time.sleep(osc.LOOP_WAIT_TIME)
        return
    
    menu = menus.menu("Link Account", [("Link through browser", 1), ("Link from device", 2), ("Cancel", None)])
    if menu == 1:
        import modules.qr_codes as qr
        link_url = api.link_url
        tft.fill(0)
        tft.text(f8x8, "Go to this link or scan qr:", 0, 0, 65535)
        tft.text(f8x8, link_url, 0, 8, 65535)
        tft.text(f8x8, "Press any button to continue", 0, 16, 65535)
        # Render QR code with link, 2x scale
        qr.make_qr(tft, link_url, 0, 24, 2)
        
        while button_combos.any_btn(['a', 'b', 'c']) == False:
            time.sleep(osc.LOOP_WAIT_TIME)
        
        link_menu = menus.menu("Link menu", [("Enter code", 1), ("Cancel", None)])
        if link_menu == 1:
            import modules.numpad as numpad
            code = numpad.numpad("Enter code", 6)
            api.link(code, True)