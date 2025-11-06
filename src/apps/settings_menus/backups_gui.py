"""
Backups GUI for settings
"""

import os
import time

import fonts.def_8x8 as f8x8
import modules.io_manager as io_man
import modules.menus as menus
import modules.popup as popup
import modules.powersaving as ps
import modules.printer as printer
from modules.printer import Levels as log_levels
from modules.translate import get as l_get


def run():
    """Show backups GUI"""
    tft = io_man.get("tft")
    
    import modules.backups as backups
    import modules.files as files
    
    while True:
        backup_menu = menus.menu(l_get("apps.settings.backups.title"), [
            (l_get("apps.settings.backups.create_backup"), 1),
            (l_get("apps.settings.backups.restore_backup"), 2),
            (l_get("menus.menu_close"), None)
        ])
        
        # Create
        if backup_menu == 1:
            location = menus.menu(l_get("apps.settings.backups.backup_to"), [
                (l_get("apps.settings.backups.internal_storage"), f"/usr/backups/backup_{time.time()}.bak"),
                (l_get("apps.settings.backups.sd_card"), f"/sd/backups/backup_{time.time()}.bak"),
                (l_get("menus.menu_close"), None)
            ])
            
            if location is None:
                return
            
            # Boost freq for faster backup
            ps.boost_allowing_state(True)
            ps.boost_clock()
            
            # Create folders
            files.mkdir_recursive("/usr/backups")
            if "sd" in os.listdir("/"):
                files.mkdir_recursive("/sd/backups")
            
            # Backup screen
            tft.fill(0)
            tft.text(f8x8, l_get("apps.settings.backups.creating_backup"), 0, 0, 65535)
            
            result_ok = False
            
            try:
                result = backups.backup_all(location)
                result_ok = result
            except Exception as e:
                printer.log(f"Backup creation error: {e}", log_levels.ERROR)
                result_ok = False

            ps.boost_allowing_state(False) # Disable boosts
            ps.loop()
                
            if result_ok:
                popup.show(l_get("apps.settings.backups.backup_created").replace("%path%", location), l_get("popups.info"), 10)
                return
            else:
                popup.show(l_get("apps.settings.backups.error_occurred"), l_get("crashes.error"), 10)
                return
        
        # Restore
        elif backup_menu == 2:
            import modules.file_explorer as file_explorer
            location = file_explorer.run(True)
            if location is None:
                return
            
            # Confirm restore
            confirm_restore = menus.menu(l_get("apps.settings.backups.restore_ask"), [
                (l_get("menus.no"), None),
                (l_get("menus.yes"), 1)
            ])
            
            if confirm_restore is None:
                return
            
            # Restore screen
            tft.fill(0)
            tft.text(f8x8, l_get("apps.settings.backups.restoring_backup"), 0, 0, 65535)
            
            # Backup to temp in case of failure
            ps.boost_allowing_state(True)
            ps.boost_clock()
            temp_backup_path = f"/temp/backups/temp_restore_backup_{time.time()}.bak"
            files.mkdir_recursive("/temp/backups")
            backup_ok = backups.backup_all(temp_backup_path)
            if not backup_ok:
                ps.boost_allowing_state(False)
                popup.show(l_get("apps.settings.backups.restore_temp_error"), l_get("crashes.error"), 10)
                return
            
            ps.boost_allowing_state(False) # Disable boosts
            ps.loop()
            
            # Restore
            result_ok = False
            try:
                result_ok = backups.restore_all(location)
            except Exception as e:
                printer.log(f"Backup restore error: {e}", log_levels.ERROR)
                result_ok = False
                
            if result_ok:
                # Delete temp file
                try:
                    os.remove(temp_backup_path)
                except OSError:
                    pass
                
                popup.show(l_get("apps.settings.backups.backup_restored"), l_get("popups.info"), 10)
                # Restart ask
                restart_ask = menus.menu(l_get("apps.settings.backups.restart_now"), [
                    (l_get("menus.no"), None),
                    (l_get("menus.yes"), 1)
                ])
                if restart_ask == 1:
                    import modules.power as power
                    power.soft_reboot()
                return
            else:
                try:
                    backups.restore_all(temp_backup_path)
                except Exception:
                    pass
                popup.show(l_get("apps.settings.backups.error_occurred"), l_get("crashes.error"), 10)
                return
            
        else:
            break