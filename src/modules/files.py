"""
File helper for micropython devices
"""

import os
import re

# Create folders recursivly (ex. /usr/games/wordly)
def mkdir_recursive(path: str):
    """
    Create directory recursively
    
    Args:
        path (str): Path to folder you want to create (ex. /usr/games/wordly)
    """
    parts = path.split('/')
    if parts[0] == '':
        current = '/'
        parts = parts[1:]
    else:
        current = ''
    
    for part in parts:
        if not part:
            continue
        if current == '/' or current == '':
            current += part
        else:
            current += '/' + part

        try:
            os.mkdir(current)
        except OSError as e:
            if e.args[0] == 17:
                pass
            else:
                raise
            

def exists(path: str) -> bool:
    """
    Check if file/directory exists
    
    Args:
        path (str): Path to file/directory to check
        
    Returns:
        bool: True or False depending on file existence
    """
    try:
        os.stat(path)
        return True
    except OSError:
        return False

def rmdir_recursive(path: str):
    """
    Remove directory recursively
    
    Args:
        path (str): Path to directory you want to remove (ex. /usr/games/wordly)
    """
    for file in os.listdir(path):
        full_path = path_join(path, file)
        if is_file(full_path):
            os.remove(full_path)
        else:
            rmdir_recursive(full_path)
    os.rmdir(path)

def is_file(path: str) -> bool:
    """
    Check if path is file
    
    Args:
        path (str): Path to check
        
    Returns:
        bool: True or False depending on file type
    """
    if os.stat(path)[0] & 0x4000:
        return False
    else:
        return True

def path_join(*args) -> str:
    """
    Joins paths together
    """
    parts = [s.strip("/") for s in args if s != "/"]
    return "/" + "/".join(parts) if parts else "/"


def parent_path(path: str) -> str:
    """
    Checks parent path of file
    
    Args:
        path (str): Path to file
        
    Returns:
        str: File parent path
    """
    if path == "/" or path == "":
        return "/"
    if path.endswith("/") and path != "/":
        path = path[:-1]
    last_slash = path.rfind("/")
    if last_slash == 0:
        return "/"
    elif last_slash > 0:
        return path[:last_slash]
    else:
        return "/"
    
def cleanup_path(path: str) -> str:
    """
    Clean up path from bad characters
    
    Args:
        path (str): Path to file/directory
        
    Returns:
        str: Cleaned up path
    """
    parts = path.split('/')
    clean_parts = []
    for p in parts:
        clean = re.sub(r'[^A-Za-z0-9 ._-]', '_', p)
        clean_parts.append(clean)
    return '/'.join(clean_parts)