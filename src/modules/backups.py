"""
Backups for stick firmware

Saves system values to json file
"""

import modules.cache as cache
import modules.json as json
import modules.nvs as nvs
import modules.os_constants as osc
import version
from modules.decache import decache


class CannotOpenBackup(Exception):
    pass

class UnknownVariableType(Exception):
    pass

class DeviceCompatibilityError(Exception):
    pass

class KeylistVersionMismatch(Exception):
    pass

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
            raise UnknownVariableType(f"Unknown variable type: {args[1]}")

        backup_dict["keys"][key] = value
    
    del backup_keys
    decache("modules.backup_keylist")

    return json.write(filename, backup_dict)

def restore_all(filename: str, verify: bool = True):
    """
    Restores NVS values from backup

    Note:
        This will only restore values that match keys in keylist!
    
    Args:
        filename (str): Path where to read backup file
        verify (bool, optional): If true (default) it will check backup compatibility with device and OS
        
    Returns:
        bool: True if success, False otherwise
    """

    backup_dict = json.read(filename)
    if backup_dict is None:
        raise CannotOpenBackup(f"Cannot open backup, {filename}!")

    # Check if device is the same
    backup_device = backup_dict["manifest"]["device_name"]
    release_device = osc.RELEASE_NAME
    if verify and backup_device != release_device:
        raise DeviceCompatibilityError(f"Backup device {backup_device}, is different than current device {release_device}!")
    del release_device, backup_device
    
    # Check if keylist in backup matches system keylist
    import modules.backup_keylist as backup_keys
    list_ver_system = backup_keys.LIST_VERSION
    list_ver_backup = backup_dict["manifest"]["backup_version"]

    if verify and list_ver_system != list_ver_backup:
        raise KeylistVersionMismatch(f"Backup keylist version {list_ver_backup}, is different than system {list_ver_system}!")
    del list_ver_backup, list_ver_system

    # Backup keys specified in keylist
    for key in backup_dict["keys"]:
        # Skip unknown keys to prevent erasing app data with malicious backups.
        if key not in backup_keys.KEYS:
            continue

        args = key.split(";")
        namespace = cache.get_nvs(args[0])

        value = backup_dict["keys"][key]
        if isinstance(value, int):
            nvs.set_int(namespace, args[1], value)
        elif isinstance(value, float):
            nvs.set_float(namespace, args[1], value)
        elif isinstance(value, str):
            nvs.set_string(namespace, args[1], value)
        else:
            raise UnknownVariableType(f"Unknown variable type: {type(value)}")
    
    del backup_keys
    decache("modules.backup_keylist")

    return True