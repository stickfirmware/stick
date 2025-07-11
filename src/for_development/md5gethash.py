# md5gethash.py
# By @Kitki30

# Gets md5 hash of specified file
# Can be slow on larger files,
# as hash is computed directly on microcontroller

# This is a part of Kitki30 Development kit

# Set the file path
FILEPATH = "/recovery/recovery.py"

print("md5gethash")
print("By @Kitki30")
print("File path: " + FILEPATH)
print("\nComputing file hash...\n")

import hashlib
import binascii

try:
    h = hashlib.md5()
    with open(FILEPATH, "rb") as f:
        while True:
            chunk = f.read(512)
            if not chunk:
                break
            h.update(chunk)
    digest = h.digest()
    print(binascii.hexlify(digest).decode('utf-8'))
except Exception as e:
    print("Execution error:\n" + str(e))

