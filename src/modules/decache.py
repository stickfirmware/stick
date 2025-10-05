"""
Helper for ram cleaner to delete modules from ram
"""
import gc

import modules.ram_cleaner as r_cleaner


def decache(name: str):
    """
    Deletes module from ram

    Args:
        name (str): module name (ex. "modules.json")
    """
    r_cleaner.deep_clean_module(name)
    gc.collect()