"""
Logging helper for Stick firmware
"""

import modules.os_constants as osc
import modules.console_colors as console_colors

class Levels():
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    
LEVEL_MAP = {
    Levels.DEBUG:  ("DEBUG", console_colors.Fore.GRAY),
    Levels.INFO:   ("INFO", console_colors.Fore.LIGHTBLUE),
    Levels.WARNING:("WARNING", console_colors.Fore.YELLOW),
    Levels.ERROR:  ("ERROR", console_colors.Fore.RED),
}

def log(msg: any, log_level: int = 2):
    """
    Prints message to console if ENABLE_DEBUG_PRINTS is True

    Args:
        msg (any): Message to display in console
        log_level (int, optional): Level of the message
    """
    if log_level >= osc.LOG_LEVEL:
        level_name, color = LEVEL_MAP.get(log_level, ("INFO", console_colors.Fore.LIGHTBLUE))
        msg_str = str(msg)
        print(console_colors.wrap_text(f"[{level_name}] {msg_str}", color))  
        
def log_cleaner(msg: any):
    """
    Prints ram cleaner output to console if ENABLE_DEBUG_PRINTS and LESS_RAM_CLEANER_OUTPUT is True

    Args:
        msg (any): Message to display in console
    """
    if osc.ENABLE_DEBUG_PRINTS and not osc.LESS_RAM_CLEANER_OUTPUT:
        print(str(msg))