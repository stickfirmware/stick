# Stick firmware Version module

import modules.json as json
from modules.printer import log
from modules.printer import Levels as log_levels

_COMPONENTS_PATH = '/modules/components.json'
_COMPONENTS_CACHED = None

def load():
    """
    Gets version from components.json
    
    Returns:
        bool: True if loaded, False if error
    """
    global _COMPONENTS_CACHED, _COMPONENTS_CACHE_TIME, MAJOR, MINOR, PATCH, LANG_VER, is_beta
    
    components = json.read(_COMPONENTS_PATH)
    
    if components is None:
        return False
    
    # Load compatibility variables
    try:
        MAJOR = components['core'][0]
        MINOR = components['core'][1]
        PATCH = components['core'][2]
        LANG_VER = components['lang_ver']
        is_beta = components.get('is_core_beta', False)
    except (KeyError, ValueError):
        return False
    
    _COMPONENTS_CACHED = components
    return True

def get_version(component: str = "core") -> any:
    """
    Get version or feature set of component
    
    Note:
        This function work only after load() is called
        Please check /modules/components.json for available components, and their types

    Args:
        component (str, optional): Component name (Default is "core").

    Returns:
        any: Component from components.json or None if error
    """
    global _COMPONENTS_CACHED
    
    if _COMPONENTS_CACHED is None:
        if not load():
            return None
    
    return _COMPONENTS_CACHED.get(component, None)

def get_parsed_version(component: str = "core") -> tuple:
    """
    Get parsed version of component
    
    Note:
        This function work only after load() is called
        Please check /modules/components.json for available components, and their types

    Args:
        component (str, optional): Component name (Default is "core").

    Returns:
        tuple: Parsed version or (0,0,0) if error
    """
    ver = get_version(component)
    if ver is None:
        return (0,0,0)
    return version_parser(ver)

def version_parser(ver: any) -> tuple:
    """
    Parse version to tuple
    
    Note:
        This converts versions to tuple
        str: "1.2.3" -> (1,2,3)
        list: [1,2,3] -> (1,2,3)
        tuple: (1,2,3) -> (1,2,3)
        
        str only supports dot (.) as separator
    
    Args: 
        ver: Version to parse (Compatible types: see Note)
        
    Returns:
        tuple: Parsed version or (0,0,0) if error
    """
    
    # Get type
    ver_type = type(ver)
    
    # String parser
    if ver_type is str:
        split = ver.split(".")
        list_ver = []
        for i in split:
            if not i.isdigit():
                return (0,0,0)
            list_ver.append(int(i))
        return tuple(list_ver)
    
    # List parser
    elif ver_type is list:
        return tuple(ver)
    
    # Tuple parser
    elif ver_type is tuple:
        return ver
    
    # Unknown
    return (0,0,0)

def version_to_str(ver: any, add_prefix: bool = False, separator: str = ".") -> str:
    """
    Format version to string
    
    Note:
        This converts versions to string
        list: [1,2,3] -> "1.2.3"
        tuple: (1,2,3) -> "1.2.3"
        str: "1.2.3" -> "1.2.3"
    
    Args:
        ver: Version to format (Compatible types: see Note)
        add_prefix (bool, optional): Add 'v' prefix to version
        separator (str, optional): Separator to use between version numbers (Default is '.')
        
    Returns:
        str: Formatted version or "0.0.0" if error
    """
    
    def add_prefix(ver_str: str):
        if add_prefix:
            return "v" + ver_str
        else:
            return ver_str
    
    parse_ver = version_parser(ver)
    if parse_ver == (0,0,0):
        return add_prefix("0.0.0")
    
    ver_temp = ""
    for i in parse_ver:
        ver_temp += str(i) + separator
    ver_temp = ver_temp[:-1]
    return add_prefix(ver_temp)

# Proxy to fix compatibility issues, devs please use newer apis
def __getattr__(name):
    if name in ("MAJOR", "MINOR", "PATCH", "LANG_VER", "is_beta"):
        log(f"You are using deprecated version api ({name}), please use get_version() to get version info", log_levels.WARNING)
        if name == "is_beta": 
            return get_version("is_core_beta")
        if name == "LANG_VER": 
            return get_version("lang_ver")
        if name == "MAJOR": 
            return get_version("core")[0]
        if name == "MINOR": 
            return get_version("core")[1]
        if name == "PATCH": 
            return get_version("core")[2]
    raise AttributeError(f"module {__name__} has no attribute {name}")

# Auto loader
load()