import os

import modules.menus as menus
import modules.popup as popup
import modules.io_manager as io_man

import fonts.def_8x8 as f8x8

tft = io_man.get('tft')

def run():
    while True:
        menu = menus.menu("Install optional app-pack?", [
            ("Yes (Recomended)", 1),
            ("See app list", 2),
            ("No", None)
        ])
        
        if menu == 1:
            import modules.handle_apps as apps
            
            pack_folder = os.listdir("/app-packs")
            
            i = 0
            
            for app in pack_folder:
                i += 1
                tft.text(f8x8, f"Installing... ({str(i)}/{len(pack_folder)})", 0, 0, 65535)
                apps.install("/app-packs/" + app, False)
            open("/usr/app-pack.installed", "w").close()
            break
        
        elif menu == 2:
            popup.show("Apps in app-pack:\nImage viever\n\nEstimated size: ~3KB", "Info")
        
        elif menu == None:
            menu = menus.menu("Are you sure?", [
                ("No", None),
                ("Yes", 1)
            ])
            open("/usr/app-pack.installed", "w").close()
            if menu == 1:
                break