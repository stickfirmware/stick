"""
File helper for micropython devices
"""

import os
import re

# Create folders recursivly (ex. /usr/games/wordly)
def mkdir_recursive(path):
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
            

def exists(path):
    try:
        os.stat(path)
        return True
    except OSError:
        return False

def rmdir_recursive(path):
    for file in os.listdir(path):
        full_path = path_join(path, file)
        if is_file(full_path):
            os.remove(full_path)
        else:
            rmdir_recursive(full_path)
    os.rmdir(path)

def is_file(path):
    if os.stat(path)[0] & 0x4000:
        return False
    else:
        return True

def path_join(*args):
    parts = [s.strip("/") for s in args if s != "/"]
    return "/" + "/".join(parts) if parts else "/"


def parent_path(path):
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
    
def cleanup_path(path):
    parts = path.split('/')
    clean_parts = []
    for p in parts:
        clean = re.sub(r'[^A-Za-z0-9 ._-]', '_', p)
        clean_parts.append(clean)
    return '/'.join(clean_parts)