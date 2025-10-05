"""
SD Card handler for esp32/Stick firmware
"""

import gc
import os

import machine

from modules.printer import Levels as log_levels
from modules.printer import log

sd = None
mntpoint = "/sd"

def init(slot=2, sck=40, cs=12, miso=39, mosi=14, freq=10_000_000):
    """
    Init SD card

    Args:
        slot (int, optional): ESP32 SD Slot, default 2
        sck (int, optional): SPI SCK, default 20
        cs (int, optional): SPI CS, default 12
        miso (int, optional): SPI MISO, default 39
        mosi (int, optional): SPI MOSI, default 14
        freq (int, optional): SPI Frequency, default 10_000_000

    Returns:
        bool: True if success, False if failed
    """
    global sd
    try:
        gc.collect()
        sd = machine.SDCard(slot=slot, sck=sck, cs=cs, miso=miso, mosi=mosi, freq=freq)
        return True
    except Exception as e:
        log("Error initializing SD Card", log_levels.ERROR)
        log(e, log_levels.ERROR)
        return False
        
    
def mount(mountpoint="/sd"):
    """
    Mount SD Card (requires init() first)

    Args:
        mountpoint (str): SD Card mountpoint, default is "/sd"

    Returns:
        bool: True if success, False if failed
    """
    try:
        os.sync()
        gc.collect()
        vfs=os.VfsFat(sd)
        os.mount(vfs, mountpoint)
        os.sync()
        return True
    except Exception as e:
        log("Error mounting SD Card", log_levels.ERROR)
        log(e, log_levels.ERROR)
        return False
    
def umount(mountpoint=mntpoint):
    """
    Unmounts SD Card

    Args:
        mountpoint (str): SD Card mountpoint, default is "/sd"

    Returns:
        bool: True if success, False if failed
    """
    global sd
    try:
        os.sync()
        os.umount(mountpoint)
        os.sync()
        return True
    except Exception as e:
        log("Error unmounting SD Card", log_levels.ERROR)
        log(e, log_levels.ERROR)
        return False