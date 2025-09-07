"""
Global hardware class store
"""

_HW = {}

def get(name: str) -> any:
    """
    Get device
    
    Args:
        name (str): Name of the device in registry
        
    Returns:
        any: Device class (Make sure to handle it properly according to device)
    """
    return _HW.get(name)

def set(name: str, value: any):
    """
    Set device in IO Managers registry
    
    Args:
        name (str): Name of device you want to set
        value (any): Value you want to set as device 
    """
    _HW[name] = value

def clear():
    """
    Clears IO Managers registry
    """
    _HW.clear()