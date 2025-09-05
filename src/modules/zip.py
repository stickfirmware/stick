"""
zipfile wrapper for Stick Firmware

License: Apache 2.0
"""

import gc

import modules.zipfile as zipfile
import modules.files as files

# Get file list of zip
def get_file_list(zip_path):
    with zipfile.ZipFile(zip_path, "r") as z:
        return z.namelist()
    
def unpack_safe(zip_path, folder, chunk_size=1024):
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