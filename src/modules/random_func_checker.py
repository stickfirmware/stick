"""
Check if micropython port supports RANDOM_EXTRA_FUNC"""

import random


def check_random_extra_functions() -> bool:
    """
    Check if micropython port supports RANDOM_EXTRA_FUNC
    
    Returns:
        bool: True if supports, False if not supported
    """
    return hasattr(random, 'randrange') and hasattr(random, 'randint') and hasattr(random, 'choice')