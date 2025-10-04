"""
NVS wrapper for ESP32
Part of Stick firmware
"""

# This was written in 50% by AI

import struct

from modules.printer import log
from modules.printer import Levels as log_levels

def set_string(nvs, key, value, max_length=1984):
    """
    Sets string in nvs namespace

    Args:
        nvs (esp32.NVS): NVS namespace
        key (str): key (ex. "ssid")
        value (str): value (ex. "PublicBathroomFreeWi-Fi")

    Returns:
        bool: True if operation success, False if failed
    """
    if not value or not isinstance(value, str):
        log("Error: Invalid string value", log_levels.WARNING)
        return False
    
    if len(key) > 15:
        log("Error: Key too long (max 15 chars)", log_levels.WARNING)
        return False
    
    if len(value) > max_length:
        log(f"Error: String exceeds max length {max_length}", log_levels.WARNING)
        return False
    
    try:
        encoded = value.encode('utf-8')
        nvs.set_blob(key, encoded)
        nvs.commit()
        return True
    except Exception as e:
        log(f"NVS write error: {str(e)}", log_levels.WARNING)
        return False


def get_string(nvs, key):
    """
    Gets strings in nvs namespace

    Args:
        nvs (esp32.NVS): NVS namespace
        key (str): key (ex. "ssid")

    Returns:
        str | None: Stored string or None if operation failed
    """
    if not key or len(key) > 15:
        return None
    
    try:
        size = nvs.get_blob(key, bytearray(0))
        if size is None:
            return None

        buffer = bytearray(size)
        result_size = nvs.get_blob(key, buffer)
        if result_size != size:
            log(f"Warning: Expected {size} bytes, got {result_size}", log_levels.WARNING)
            return None
            
        return buffer.decode('utf-8')
    except Exception as e:
        log(f"NVS read error: {str(e)}")
        return None

def set_int(nvs, key, value):
    """
    Sets int in nvs namespace

    Args:
        nvs (esp32.NVS): NVS namespace
        key (str): key (ex. "autoconnect")
        value (int): value (ex. 1)
    """
    nvs.set_i32(key, int(value))
    nvs.commit()

def get_int(nvs, key):
    """
    Gets int in nvs namespace

    Args:
        nvs (esp32.NVS): NVS namespace
        key (str): key (ex. "autoconnect")

    Returns:
        int | None: Stored int or None if operation failed
    """
    try:
        return nvs.get_i32(key)
    except OSError:
        return None
    
def set_float(nvs, key, value):
    """
    Sets float in nvs namespace

    Args:
        nvs (esp32.NVS): NVS namespace
        key (str): key (ex. "volume")
        value (float): value (ex. 1.0)
    """
    b = struct.pack('f', value)
    nvs.set_blob(key, b)
    nvs.commit()

def get_float(nvs, key):
    """
    Gets float in nvs namespace

    Args:
        nvs (esp32.NVS): NVS namespace
        key (str): key (ex. "volume")

    Returns:
        float | None: Stored float or None if operation failed
    """
    try:
        b = bytearray(4)
        nvs.get_blob(key, b)
        return struct.unpack('f', b)[0]
    except Exception:
        return None