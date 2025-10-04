"""
Logging helper for Stick firmware
"""

import modules.os_constants as osc

def log(msg: any):
    """
    Prints message to console if ENABLE_DEBUG_PRINTS is True

    Args:
        msg (any): Message to display in console
    """
    if osc.ENABLE_DEBUG_PRINTS:
        print(str(msg))
        
def log_cleaner(msg: any):
    """
    Prints ram cleaner output to console if ENABLE_DEBUG_PRINTS and LESS_RAM_CLEANER_OUTPUT is True

    Args:
        msg (any): Message to display in console
    """
    if osc.ENABLE_DEBUG_PRINTS and not osc.LESS_RAM_CLEANER_OUTPUT:
        print(str(msg))