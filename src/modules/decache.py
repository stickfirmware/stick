import sys
import gc

def dechache(name):
        sys.modules.pop(name, None)
        gc.collect()