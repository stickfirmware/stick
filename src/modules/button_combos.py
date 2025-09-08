"""
Button combo helper for Stick firmware
"""

import modules.io_manager as io_man

# Gets button by name (ex. "a")
def get_button(name: str) -> any | None:
    """
    Gets button by name from IO Manager
    
    Args:
        name (str): Button name (ex. a)
    
    Returns:
        any | None: Button object, None if not found  
    """
    return io_man.get("button_" + name.lower())

# Check if button combo is pressed/released
def combo(buttons: list[str], pressed: bool = True):
    """
    Check if button combo pressed/released
    
    Args:
        buttons (list[str]): Button names (ex. ["a", "c"])
        pressed (bool, optional): Does button combo needs to be pressed (True), or released (False) to meet requirements.
    
    Returns:
        bool: True if requirements were met, False if not
    """
    buttons = [get_button(b) for b in buttons]
    if pressed:
        return all(b.value() == 0 for b in buttons)
    else:
        return all(b.value() == 1 for b in buttons)
    
# Check if any button in list is pressed/released
def any_btn(buttons, pressed=True):
    """
    Check if any button in list is pressed/released
    
    Args:
        buttons (list[str]): Button names (ex. ["a", "c"])
        pressed (bool, optional): Does button need to be pressed (True), or released (False) to meet requirements.
    
    Returns:
        bool: True if requirements were met, False if not
    """
    buttons = [get_button(b) for b in buttons]
    if pressed:
        return any(b.value() == 0 for b in buttons)
    else:
        return any(b.value() == 1 for b in buttons)