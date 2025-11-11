"""
Update system from update package


Note:
    As ESP32 has low RAM, update packages need to include only changed files.
    So it will need ex. 2.2.1 before 2.2.2, this saves us RAM as it only reads few files instead of 200+
"""

import gc

import fonts.def_8x8 as f8x8
import modules.files as files
import modules.io_manager as io_man
import modules.json as json
import modules.menus as menus
import version
from modules.decache import decache
from modules.printer import Levels as log_levels
from modules.printer import log
from modules.translate import get as l_get

class VersionCompatibilityError(Exception):
    pass

class CriticalUpdateFail(Exception):
    pass

class InvalidFilePath(Exception):
    pass

class ManifestReadFailed(Exception):
    pass

class AbortedByUser(Exception):
    pass

def update(path: str, gui: bool = True):
    """
    Updates Stick Firmware from zip update package
    
    Args:
        path (str): Path to update package
        gui (bool, optional): True to allow GUI, will show changelogs and status.
    """
    
    log("Update started!")
    log("Checking for invalid file paths", log_levels.DEBUG)
    if not path or path == "":
        raise InvalidFilePath(f"Invalid update package path: {path}")
    
    if gui:
        log("GUI Mode!")
        tft = io_man.get("tft")
        tft.fill(0)
        tft.text(f8x8, l_get("apps.settings.update.update_process_messages.updating"), 0, 0)
        tft.text(f8x8, l_get("apps.settings.update.update_process_messages.reading_package"), 0, 8)
    
    # Unpack json manifest
    gc.collect()
    log("Extract manifest...", log_levels.DEBUG)
    import modules.handle_apps as h_apps  # It contains some zip functions that update needs
    data = h_apps.get_packed_file_bytes(path, "update.json")
    if data is None:
        raise ManifestReadFailed("update.json not found in package, is this really an update package?")
    log("Jsonize manifest...", log_levels.DEBUG)
    manifest = json.read_from_string(data)
    del data
    decache("modules.handle_apps")
    gc.collect()
    
    # Read manifest
    log("Reading manifest", log_levels.DEBUG)
    if not manifest:
        raise ManifestReadFailed("Could not read update.json, please check for corruption.")
    
    try:
        required_sys_ver = manifest["required_sys_ver"]
        changelog = manifest["changelog_path"]
        root_folder = manifest["update_root"]
    except (KeyError, ValueError):
        raise ManifestReadFailed("Update manifest could not be read, is this really an update package?")
    finally:
        del manifest
    
    # Check system version
    log("Compare system and update version", log_levels.DEBUG)
    if gui:
        tft.text(f8x8, l_get("apps.settings.update.update_process_messages.check_version"), 0, 16)
    sys_ver = version.get_parsed_version()
    if version.version_parser(required_sys_ver) != sys_ver:
        raise VersionCompatibilityError(f"Version compatibility error! Required version {required_sys_ver}, system version {sys_ver}")
    
    # Unpack changelog and show
    gc.collect()
    files.mkdir_recursive("/temp/os_update")
    if gui:
        import modules.zip as zip
        import modules.open_file as o_file
        log("Show changelog", log_levels.DEBUG)
        tft.text(f8x8, l_get("apps.settings.update.update_process_messages.get_changelog"), 0, 24)
        try:
            ch_unp_path = "/temp/os_update/changelog.txt"
            zip.unpack_file(path, changelog, ch_unp_path)
            o_file.open_in("com.kitki30.filereader", ch_unp_path)
        except Exception:
            pass
        decache("modules.open_file")
        tft.fill(0)
        tft.text(f8x8, l_get("apps.settings.update.update_process_messages.updating"), 0, 0)
    decache("modules.zip")
    gc.collect()
        
    # Ask user for confirmation
    confirmation = True
    if gui:
        log("Ask user for confirmation", log_levels.DEBUG)
        confirmation = menus.menu(l_get("apps.settings.update.update_process_messages.update_confirmation"),
                            [(l_get("menus.yes"), True),
                            (l_get("menus.no"), False)])
        tft.fill(0)
        tft.text(f8x8, l_get("apps.settings.update.update_process_messages.updating"), 0, 0)
        
    if not confirmation:
        raise AbortedByUser("Update was aborted by user")
    
    # Real update process (Extract system)
    gc.collect()
    log("Extract files from update package", log_levels.DEBUG)
    import modules.zipfile as zipfile
    try:
        with zipfile.ZipFile(path, "r") as z:
            root_prefix = root_folder.rstrip("/") + "/"

            for member in z.infolist():
                # Skip outside zip root
                if not member.filename.startswith(root_prefix):
                    continue

                rel_path = member.filename[len(root_prefix):]  # Relative file path
                if not rel_path:
                    continue

                abs_path = "/" + rel_path
                abs_path = files.cleanup_path(abs_path)

                # If its firectory make it
                if member.is_dir() or member.filename.endswith("/"):
                    files.mkdir_recursive(abs_path)
                    continue

                # Unpack file
                log(f"Extracting {abs_path}", log_levels.DEBUG)
                files.mkdir_recursive("/".join(abs_path.split("/")[:-1]))
                with z.open(member, "r") as src, open(abs_path, "wb") as dst:
                    while True:
                        chunk = src.read(1024)
                        if not chunk:
                            break
                        dst.write(chunk)
                        gc.collect()
    except Exception:
        raise CriticalUpdateFail("Critical update fail! Update from recovery with recovery package.")
    finally:
        decache("modules.zipfile")
        gc.collect()
            
    log("Update finished!")
                    
    # Change postinstall registry
    import modules.cache as cache
    import modules.nvs as nvs
    
    log("Change postinstall values", log_levels.DEBUG)
    n_updates = cache.get_nvs('updates')
    nvs.set_int(n_updates, "postinstall", 1)
    
    # Reboot
    log("Show popup and reboot", log_levels.DEBUG)
    import modules.popup as popup
    popup.show(l_get("apps.settings.update.update_process_messages.reboot_popup"), l_get("popups.info"), 15)
    
    import modules.power as power
    power.soft_reboot()
    
def update_interactive():
    """
    Update system with user GUI, user selects file with file explorer
    """
    import modules.file_explorer as file_ex
    import modules.popup as popup
    file = file_ex.run(True)
    try:
        update(file)
    except VersionCompatibilityError as e:
        log(f"Update process got VersionCompatibilityError: {e}", log_levels.ERROR)
        popup.show(l_get("apps.settings.update.interactive_mode.ver_not_compatible"), l_get("crashes.error"))
    except InvalidFilePath:
        log("Invalid file selected during update process", log_levels.WARNING)
        popup.show(l_get("apps.settings.update.interactive_mode.invalid_file"), l_get("crashes.error"))
    except AbortedByUser:
        log("Update aborted by user.", log_levels.WARNING)
        popup.show(l_get("apps.settings.update.interactive_mode.aborted"), l_get("crashes.error"))
    except ManifestReadFailed as e:
        log(f"Update process got ManifestReadFailed: {e}", log_levels.ERROR)
        popup.show(l_get("apps.settings.update.interactive_mode.manifest_read_error"), l_get("crashes.error"))
    except (CriticalUpdateFail, Exception) as e:
        log(f"Update critical error: {e}", log_levels.ERROR)
        popup.show(l_get("apps.settings.update.interactive_mode.critical"), l_get("crashes.error"))