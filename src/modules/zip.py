"""
zipfile wrapper for Stick Firmware
"""

import gc

import modules.zipfile as zipfile
import modules.files as files

# Get file list of zip
def get_file_list(zip_path):
    """
    Gets file list of zip archive

    Args:
        zip_path (str): Full path to zip archive (ex. /usr/zip.zip)

    Returns:
        list[str]: List of files in zip archive
        
    Example:
        >>> get_file_list("/usr/zip.zip")
        ["super_secret_file.txt", "cat.png"]
    """
    with zipfile.ZipFile(zip_path, "r") as z:
        return z.namelist()
    
def unpack_safe(zip_path, folder, chunk_size=1024):
    """
    Unpacks zip archive

    Args:
        zip_path (str): Full path to zip archive (ex. /usr/zip.zip)
        folder (str): Full path to the folder where zip archive will be unpacked (doesn't need to exist)
        chunk_size (int, optional): Unpacking chunk size in bytes, default 1024
    """
    files.mkdir_recursive(folder)

    with zipfile.ZipFile(zip_path, "r") as z:
        for member in z.infolist():
            path = folder + "/" + member.filename
            if member.filename.endswith("/"):
                files.mkdir_recursive(path)
                continue

            with z.open(member, "r") as src, open(files.cleanup_path(path), "wb") as dst:
                while True:
                    chunk = src.read(chunk_size)
                    if not chunk:
                        break
                    dst.write(chunk)
                    gc.collect()