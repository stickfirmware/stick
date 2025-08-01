import sys
import gc
import modules.ram_cleaner as r_cleaner

def decache(name):
        r_cleaner.deep_clean_module(name)
        gc.collect()