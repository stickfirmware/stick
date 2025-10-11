"""
Module that helps developer to manage licenses. Without taking more flash space.
"""

import time

import modules.files as files
import modules.json as json
from modules.printer import Levels as log_levels
from modules.printer import log
from modules.translate import get as l_get

_SUPPORTED = ["mit", "apache_2_0"]
_MAPPING = {
    "mit": "MIT License",
    "apache_2_0": "Apache 2.0 License"
}
_LICENSING_CONFIG = "/usr/config/licensing.json"

_LICENSING_COMMENT = (
    "This is licensing file for Stick firmware, "
    "every license, accepted or not, "
    "requested by any app, "
    "will appear here, "
    "you can manage them here."
)

# Custom exceptions
class DuplicateLicenseFound(Exception):
    pass

class LicenseNotFound(Exception):
    pass

class LicenseNotSupported(Exception):
    pass

def get_license(license_name, author, year):
    if license_name not in _SUPPORTED:
        log(f"License '{license_name}' is not supported", log_levels.WARNING)
        raise LicenseNotSupported(f"License not supported ('{license_name}')")
    
    log(f"Opening license '{license_name}'", log_levels.DEBUG)
    with open(f"/licenses/{license_name}", "r") as f:
        license_text = f.read()
        license_text = license_text.replace("%year%", str(year)).replace("%author%", str(author))
        
    return license_text

def check_license(id: str):
    """
    Get license object from licenses config
    
    Args:
        id (str): License ID
        
    Returns:
        dict | None: Either license dictionary or None if not found"""
    
    if not files.exists(_LICENSING_CONFIG):
        log("License config not created yet, making new one")
        json.write(_LICENSING_CONFIG, {"__info": _LICENSING_COMMENT, "licenses": []})
        return None
    
    try:
        config = json.read(_LICENSING_CONFIG)
        for i in config["licenses"]:
            if i["id"] == id:
                return i
        return None
    except (ValueError, KeyError):
        return None
    
def add_license(id: str, name: str, lic_name: str, author: str, year: str, type: str = "free"):
    """
    Add license to registry
    
    Args:
        id (str): Unique ID for your app
        name (str): License/App name
        lic_name (str): License type (mit or apache_2_0)
        author (str): Your name, will be replaced in license prompts
        year (str): License date, will be replaced
        type (str): License type (free or restricted)
        
    Returns:
        bool: True if success, False (or LicenseNotSupported or DuplicateLicenseFound) if failed
    """
    
    if not files.exists(_LICENSING_CONFIG):
        log("License config not created yet, making new one")
        json.write(_LICENSING_CONFIG, {"__info": _LICENSING_COMMENT, "licenses": []})
        
    if lic_name not in _SUPPORTED:
        log(f"License '{lic_name}' is not supported", log_levels.WARNING)
        raise LicenseNotSupported(f"License not supported ('{lic_name}')")
    
    licenses_config = json.read(_LICENSING_CONFIG)
    licenses = licenses_config.get("licenses", [])
    
    new_license = {
        "id": id,
        "name": name,
        "lic_name": lic_name,
        "type": type,
        "author": author,
        "year": year,
        "date_created": time.time(),
        "accepted": False,
        "date_accepted": None
    }
    
    # Anti duplicate
    if any(l.get("id") == new_license.get("id") for l in licenses): # noqa
        raise DuplicateLicenseFound("Other license with the same ID was found.")
    
    licenses.append(new_license)
    licenses_config["licenses"] = licenses
    json.write(_LICENSING_CONFIG, licenses_config)
    return True

def prompt_license(id: str):
    """
    Prompt user to accept license
    
    Args:
        id (str): Your license ID
        
    Return:
        bool: True if license accepted, False if not
    """
    
    license = check_license(id)
    
    if license is None:
        log(f"Could not find license of id '{id}', please use add_license() to add it, and then try again", log_levels.WARNING)
        raise LicenseNotFound(f"License with ID '{id}' was not found, use add_license() first")
    
    if license.get("accepted"):
        log("License was already accepted! No need to show user prompt.")
        return True
    
    import modules.menus as menus
    import modules.popup as popup
    log(f"License '{id}' was not accepted, requesting user input")
    
    popup.show(l_get("licensing_service.ask_popup")
                .replace("%license_name%", license.get('name'))
                .replace("%license_type%", _MAPPING[license.get('lic_name')])
                .replace("%license_author%", license.get('author')), 
               l_get("licensing_service.name"), 60)
    
    acceptation = menus.menu(l_get("licensing_service.ask_menu_title"), 
                             [(l_get("menus.yes"), 1),
                              (l_get("menus.no"), None)])
    
    if acceptation == 1:
        license["accepted"] = True
        license["date_accepted"] = time.time()

        config = json.read(_LICENSING_CONFIG)
        licenses = config.get("licenses", [])
        for i, l in enumerate(licenses): # noqa
            if l.get("id") == id:
                licenses[i] = license
                break
        config["licenses"] = licenses
        json.write(_LICENSING_CONFIG, config)
        popup.show(l_get("licensing_service.popup_success"),
                   l_get("licensing_service.name"), 10)
        return True

    return False