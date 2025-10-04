"""
Helper for colors in console
"""

class Fore:
    GRAY = "\033[90m"
    LIGHTBLUE = "\033[94m"
    YELLOW = "\033[93m"
    RED = "\033[31m"
"""Fore colors"""
    
class Style:
    RESET = "\033[0m"
"""Styles"""


def wrap_text(text: str, color: str):
    """
    Wrap text in color
    
    Args:
        text (str): Your string
        color (str): Color to wrap text in
        
    Returns:
        str: Your colored string
    """
    
    return f"{color}{text}{Style.RESET}"