import os
import gc

import modules.menus as menus
import modules.popup as popup
import modules.io_manager as io_man
from modules.translate import get as l_get

import fonts.def_8x8 as f8x8

tft = io_man.get('tft')

def run():
    while True:
        menu = menus.menu(l_get("apps.pack_installer.optional_prompt"), [
            (l_get("apps.pack_installer.yes_recommend"), 1),
            (l_get("apps.pack_installer.see_list"), 2),
            (l_get("menus.no"), None)
        ])
        
        if menu == 1:
            import modules.handle_apps as apps
            
            pack_folder = os.listdir("/app-packs")
            
            i = 0
            failed_counter = 0
            
            for app in pack_folder:
                i += 1
                tft.text(f8x8, f"{l_get("apps.app_installer.installing")} ({str(i)}/{len(pack_folder)})", 0, 0, 65535)
                try:
                    apps.install("/app-packs/" + app, False)
                    gc.collect()
                except Exception:
                    failed_counter += 1
            open("/usr/app-pack.installed", "w").close()
            
            popup.show(l_get("apps.pack_installer.success_popup").replace("%total%", str(len(pack_folder))).replace("%failed%", str(failed_counter)), l_get("popups.info"))
            break
        
        elif menu == 2:
            size_estimate = "~3KB"
            apps_list = "Image viewer"
            popup.show(l_get("apps.pack_installer.app_list").replace("%apps%", apps_list).replace("%size%", size_estimate), l_get("popups.info"))
        
        elif menu is None:
            menu = menus.menu(l_get("menus.are_sure"), [
                (l_get("menus.no"), None),
                (l_get("menus.yes"), 1)
            ])
            open("/usr/app-pack.installed", "w").close()
            if menu == 1:
                break