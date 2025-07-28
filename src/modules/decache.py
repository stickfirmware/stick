import sys
import gc

def decache(name):
        sys.modules.pop(name, None)
        gc.collect()