"""
Backups for stick firmware

Saves system values to json file
"""

import modules.cache as cache
from modules.decache import decache
import modules.json as json
import modules.nvs as nvs
import modules.os_constants as osc
import version

def backup_all(filename: str):
    """
    Backups all known system values
    
    Args:
        filename (str): Path where to write backup file
        
    Returns:
        bool: True if success, False otherwise
    """

    import modules.backup_keylist as backup_keys

    backup_dict = {}

    # Gather data about system,
    # device and keylist to ensure compatibility.
    manifest = {
        "backup_version": backup_keys.LIST_VERSION,
        "system_version": version.get_parsed_version(),
        "device_name": osc.RELEASE_NAME
    }

    backup_dict["manifest"] = manifest
    backup_dict["keys"] = {}
    del manifest

    # Backup keys specified in keylist
    for key in backup_keys.KEYS:
        args = key.split(";")
        namespace = cache.get_nvs(args[0])

        value = None
        if args[2] == "int":
            value = nvs.get_int(namespace, args[1])
        elif args[2] == "float":
            value = nvs.get_float(namespace, args[1])
        elif args[2] == "string":
            value = nvs.get_string(namespace, args[1])
        else:
            return False

        backup_dict["keys"][key] = value
    
    del backup_keys
    decache("modules.backup_keylist")

    return json.write(filename, backup_dict)