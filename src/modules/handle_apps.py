"""
Stick firmware package handler
"""

import os
import gc

import modules.json as json
from modules.printer import log
import modules.files as files

_MAX_PACKAGE_SIZE = 128 * 1024 # Allowed pack size, default is 128KB, install() will fail if bigger than this
_FLASH_FREE_SPACE_MULTI = 2.5 # Free space requirement multiplier for formula (install() requires free space to be more than zip_size * multi)

# Custom exceptions
class PackageReadFailed(Exception):
    pass

class ManifestParseError(Exception):
    pass

class UnknownManifestVersion(Exception):
    pass

class NotEnoughFlash(Exception):
    pass

class PackageSizeTooHigh(Exception):
    pass

# Manifests classes
class ManifestV1App:
    """Manifest V1 Class"""
    def __init__(self):
        self.ver = 1
        self.app_name = "N/A"
        self.app_description = "N/A"
        self.app_ver = 0
        self.install_dependencies = False
        self.entrypoint = None
        self.app_type = 0 # 0 - Standard app with user interface, 1 - Dependency install package
        self.pack_id = ""
        self.did_init = False
        
    # Validate manifest, check if all fields are in it
    @staticmethod
    def validate_manifest(manifest: dict):
        """
        Manifest validation helper, returns ManifestParseError if manifest has missing fields
        
        Args:
            manifest (dict): Manifest json dictionary
        """
        
        if "version" not in manifest:
            raise ManifestParseError("Missing 'version' field in manifest")
        
        manifest_ver = manifest["version"]
        if manifest_ver != 1:
            raise ManifestParseError(f"Class ManifestV1App was created, but version of provided manifest was different ({manifest_ver})")
        
        if "name" not in manifest:
            raise ManifestParseError("Missing 'name' field in manifest")
        if "description" not in manifest:
            raise ManifestParseError("Missing 'description' field in manifest")
        if "pack_id" not in manifest:
            raise ManifestParseError("Missing 'pack_id' field in manifest")
        if "app_ver" not in manifest:
            raise ManifestParseError("Missing 'app_ver' field in manifest")
        if "install_dependencies" not in manifest:
            raise ManifestParseError("Missing 'install_dependencies' field in manifest")
        if "app_type" not in manifest:
            raise ManifestParseError("Missing 'app_type' field in manifest")
        
    # Get stringified version of app_type
    def type_stringified(self) -> str:
        """
        Get stringified type of app (Need to call handle_manifest first)
        
        Returns:
            str: Stringified type of app (ex. "Dependency package")
        """
        
        a_type = self.app_type
        
        if a_type == 0:
            return "Standard app with UI"
        elif a_type == 1:
            return "Dependency package"
        else:
            return "Unknown app_type"
    
    # Handle manifest, set variables correctly
    def handle_manifest(self, manifest: dict):
        """
        Handle manifest from json dictionary
        
        Args:
            manifest (dict): Manifest dictionary
        """
        
        if self.did_init == True:
            return
        
        self.validate_manifest(manifest)
        self.app_name = manifest["name"]
        self.app_description = manifest["description"]
        self.app_ver = manifest["app_ver"]
        self.ver = manifest["version"]
        self.install_dependencies = manifest["install_dependencies"]
        self.app_type = manifest["app_type"]
        self.pack_id = files.cleanup_path(manifest["pack_id"])
        
        if "entrypoint" not in manifest:
            self.entrypoint = None
        else:
            self.entrypoint = files.cleanup_path(manifest["entrypoint"])
            
        self.did_init = True
                

# Do not use it for large files,
# please unpack them using the zip module to save ram
def get_packed_file(zip_path, filename):
    """
    Gets file from zip archive
    
    Args:
        zip_path (str): Path to zip archive
        filename (str): Path to file in zip archive (were / is the root of zip archive)
        
    Return:
        str | None: File content or None if failed to unpack
    """
    gc.collect()
    import modules.zipfile as zipfile

    with zipfile.ZipFile(zip_path, "r") as z:
        if filename not in z.namelist():
            return None
        with z.open(filename) as f:
            return f.read()
    gc.collect()
    
# Slightly better unpacker, still eats ram
def get_packed_file_bytes(zip_path, filename, chunk_size=1024):
    """
    Slightly better file getter
    
    Args:
        zip_path (str): Path to zip archive
        filename (str): Path to file in zip archive (were / is the root of zip archive)
        
    Return:
        str | None: File content or None if failed to unpack
    """
    import modules.zipfile as zipfile
    import gc

    gc.collect()
    with zipfile.ZipFile(zip_path, "r") as z:
        if filename not in z.namelist():
            return None
        with z.open(filename) as f:
            buf = bytearray()
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                buf.extend(chunk)
                gc.collect()
            return bytes(buf)
        
# Clean pack file to not start with dot or slash
def clean_pack_file(path: str) -> str:
    """
    Cleans pack file to not start with dot (.) or slash (/)
    
    Args:
        path (str): Path
        
    Return:
        str: Cleaned up path
    """
    while path.startswith(('/', '.')):
        path = path[1:]
    return path
        
# Get manifest class from zip package
def get_manifest(zip_package: str) -> any:
    """
    Gets manifest class from zip package
    
    Args:
        zip_package (str): Path to app archive
        
    Return:
        any: Manifest class
    """
    log("get_manifest()")
    
    try:
        log("Extract manifest..")
        data = get_packed_file_bytes(zip_package, "manifest.json")
        if data is None:
            raise PackageReadFailed("manifest.json not found in package, is this really an app package?")
        log("Jsonize manifest...")
        manifest = json.read_from_string(data)
    except OSError:
        raise PackageReadFailed("Cannot open zip package: " + str(zip_package))
    except ValueError:
        raise ManifestParseError("manifest.json is not valid JSON")

    log("Parse manifest...")
    if "version" not in manifest:
        raise ManifestParseError("Missing 'version' field in manifest")

    manifest_ver = manifest["version"]
    
    if manifest_ver == 1:
        manifest_class = ManifestV1App()
        manifest_class.handle_manifest(manifest)
        return manifest_class
    else:
        raise UnknownManifestVersion(f"This manifest version ({manifest_ver}) is not currently supported, is your app setup properly?")
    
# Get version (int) from class (ex. ManifestV1App)
def check_version_from_class(obj) -> int:
    """
    Get manifest version from class
    
    Args:
        obj (any): Manifest class
        
    Return:
        int: Manifest version or 0 if unknown
    """
    if isinstance(obj, ManifestV1App):
        return 1
    else:
        return 0
    
# Install app
def install(zip_package, delete_app_package=True):
    """
    Install app package
    
    Args:
        zip_package (str): Path to app package
        delete_app_package (bool, optional): True if you want to delete app package after successful install
        
    Return:
        bool: True if success, False if failed
    """
    log("App installer")
    
    # Check how much free space, app requires: zip_size * _FLASH_FREE_SPACE_MULTI of free storage space
    log("Check flash space")
    stat_vfs = os.statvfs("/")
    free_flash = stat_vfs[0] * stat_vfs[3]
    log(f"{free_flash}B")
    
    log("Check pack size")
    zip_size = os.stat(zip_package)[6]
    log(f"{zip_size}B")
    
    if zip_size > _MAX_PACKAGE_SIZE:
        raise PackageSizeTooHigh(f"Package size expected to be lower than {_MAX_PACKAGE_SIZE}B but got {zip_size}B")
    
    zip_size_formula = zip_size * _FLASH_FREE_SPACE_MULTI
    
    if zip_size_formula > free_flash:
        raise NotEnoughFlash(f"Expected free flash size to be more than {zip_size_formula}B but free space was {free_flash}B")
    
    # Check manifest
    gc.collect()
    log("Identify manifest version")
    manifest = get_manifest(zip_package)
    manifest_ver = check_version_from_class(manifest)
    
    if manifest_ver == 1:
        log("Manifest version 1 detected")
        
        if manifest.did_init != True:
            raise PackageReadFailed("Manifest class was not init in installer (Code error?), you can try opening github issue!")
        
        app_name = manifest.app_name
        app_desc = manifest.app_description
        app_ver = manifest.app_ver
        app_type = manifest.app_type
        entrypoint = manifest.entrypoint
        dependencies = manifest.install_dependencies
        pack_id = manifest.pack_id
        
        is_dependency = False
        hidden = False
        
        log(f"""
            Name: {app_name}
            PackageID: {pack_id}
            Description: {app_desc}
            Version: {app_ver}
            Type: {app_type} ({manifest.type_stringified()})
            Entrypoint: {entrypoint} (Can be none if not a standard app)
            Install dependencies: {str(dependencies)}
            """)
        
        # Unpack app
        log("Unpacking app")
        gc.collect()
        import modules.zip as zip
        if app_type == 0:
            package_folder = "/apps/thirdparty/" + pack_id.replace(".", "_")
            zip.unpack_safe(zip_package, package_folder)
            hidden = False
            is_dependency = False
            
        # Cleanup
        log("Cleaning up...")
        import modules.ram_cleaner as rclean
        rclean.deep_clean_module("modules.zip")
        rclean.deep_clean_module("modules.zipfile")
            
        # Registry
        log("Add to registry")
        gc.collect()
        import apps.oobe as oobe
        
        oobe.edit_app(
            pack_id,
            name=app_name,
            handleExtensions=[""],
            hidden=hidden,
            is_system_app=False,
            dependency=is_dependency,
            main_folder=package_folder,
            file=f"{clean_pack_file(package_folder)}/{entrypoint}".replace("/", ".") if entrypoint else None
        )

        # Delete app package
        if delete_app_package == True:
            log("Delete app pack")
            try:
                os.remove(zip_package)
            except OSError:
                pass
            
        log("Done!")
        return True
    else:
        raise UnknownManifestVersion("Unknown manifest, maybe its corrupt, or system firmware is outdated? App installer failed!")
    
    log("App installer failed, code got to a point where it should not be!")
    return False

# Gui installer context menu (File explorer)
def open_file(path):
    """
    Context menu gui installer
    
    Args:
        path (str): Path to app package
    """
    import modules.menus as menus
    from modules.popup import show as popup
    import modules.io_manager as io_man
    from modules.translate import get as l_get
    
    tft = io_man.get("tft")
    
    import fonts.def_16x32 as f16x32
    import fonts.def_8x8 as f8x8
    
    tft.fill(0)
    tft.text(f16x32, l_get("apps.app_installer.app_installer_short"),0,0,65335)
    
    delete = False
    if menus.menu(l_get("apps.app_installer.delete_after_install"),
                  [(l_get("menus.yes"), 1),
                  (l_get("menus.no"), None)]) == 1:
        delete = True
        
    tft.fill(0)
    tft.text(f16x32, l_get("apps.app_installer.app_installer_short"),0,0,65335)
    tft.text(f8x8, l_get("apps.app_installer.installing"),0,127,65335)
    
    try:
        if install(path, delete) == True:
            popup(l_get("apps.app_installer.popups.success"), l_get("popups.info"))
    except MemoryError:
        popup(l_get("apps.app_installer.popups.memory_error"), l_get("crashes.error"))
    except UnknownManifestVersion:
        popup(l_get("apps.app_installer.popups.unknown_manifest_ver"), l_get("crashes.error"))
    except PackageSizeTooHigh:
        popup(l_get("apps.app_installer.popups.package_size_too_high"), l_get("crashes.error"))
    except PackageReadFailed:
        popup(l_get("apps.app_installer.popups.package_read_failed"), l_get("crashes.error"))
    except NotEnoughFlash:
        popup(l_get("apps.app_installer.popups.not_enough_flash"), l_get("crashes.error"))
    except ManifestParseError:
        popup(l_get("apps.app_installer.popups.manifest_parse_error"), l_get("crashes.error"))