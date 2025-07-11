import hashlib
import binascii

def execute(args):
    if len(args) >= 2:
        try:
            h = hashlib.md5()
            with open(args[1], "rb") as f:
                while True:
                    chunk = f.read(512)
                    if not chunk:
                        break
                    h.update(chunk)
            digest = h.digest()
            return binascii.hexlify(digest).decode('utf-8')
        except Exception as e:
            return "Execution error:\n" + str(e)
    else:
        return "Usage: md5sum {filename}"