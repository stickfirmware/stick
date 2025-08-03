import os

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