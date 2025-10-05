"""
ujson wrapper for micropython, part of Stick firmware
"""

import ujson as json


def read(filename: str) -> dict | None:
    """
    Parse json from file

    Args:
        filename (str): Path to json file

    Returns:
        dict | None: Json dictionary or None if failed
    """
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            file.close()
        return data
    except Exception:
        return None
    
def read_gzipped(filename: str) -> dict | None:
    """
    Parse json from gzipped file

    Args:
        filename (str): Path to gzipped json file

    Returns:
        dict | None: Json dictionary or None if failed
    """
    import deflate
    with open(filename, "rb") as f:
        with deflate.DeflateIO(f, deflate.AUTO) as f:
            data = json.load(f)
            f.close()
            return data

def write(filename: str, data: dict) -> bool:
    """
    Write json to file

    Args:
        filename (str): Path to json file
        data (dict): Data to write to file

    Returns:
        bool: True if success, False if failed
    """
    try:
        with open(filename, 'w') as file:
            json.dump(data, file)
            file.close()
        return True
    except Exception:
        return False
        
def read_from_string(data: str) -> dict | None:
    """
    Parse json from string

    Args:
        data (str): Json string data

    Returns:
        dict | None: Json dictionary or None if failed
    """
    try:
        return json.loads(data)
    except Exception:
        return None

def to_string(data: dict) -> str | None:
    """
    Convert dictionary to json string

    Args:
        data (dict): Data to convert

    Returns:
        str | None: Json string or None if failed
    """
    try:
        return json.dumps(data)
    except Exception:
        return None