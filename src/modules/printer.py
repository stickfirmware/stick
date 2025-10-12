"""
Logging helper for Stick firmware
"""

import modules.cache as cache
import modules.console_colors as console_colors
import modules.os_constants as osc


class Levels():
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5
    
LEVEL_MAP = {
    Levels.DEBUG:  ("DEBUG", console_colors.Fore.GRAY),
    Levels.INFO:   ("INFO", console_colors.Fore.LIGHTBLUE),
    Levels.WARNING:("WARNING", console_colors.Fore.YELLOW),
    Levels.ERROR:  ("ERROR", console_colors.Fore.RED),
    Levels.CRITICAL: ("CRITICAL", console_colors.Fore.BOLD_RED)
}

def log(msg: any, log_level: int = 2):
    """
    Prints message to console if ENABLE_DEBUG_PRINTS is True

    Args:
        msg (any): Message to display in console
        log_level (int, optional): Level of the message
    """
    
    if log_level >= osc.LOG_LEVEL:
        try:
            level_name, color = LEVEL_MAP.get(log_level, ("INFO", console_colors.Fore.LIGHTBLUE))
            msg_str = str(msg)
            print(console_colors.wrap_text(f"[{level_name}] {msg_str}", color))
            
            if cache.get("allow_xp_levelling"):
                import modules.xp_leveling as xp_levels
                if log_level == Levels.ERROR:
                    xp_levels.remove_mood(5)
                elif log_level == Levels.WARNING:
                    xp_levels.remove_mood(2)
        except Exception:
            print(str(msg))
        
def log_cleaner(msg: any):
    """
    Prints ram cleaner output to console if ENABLE_DEBUG_PRINTS and LESS_RAM_CLEANER_OUTPUT is True

    Args:
        msg (any): Message to display in console
    """
    if not osc.LESS_RAM_CLEANER_OUTPUT:
        print(str(msg))