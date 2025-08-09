import random

def check_random_extra_functions():
    return hasattr(random, 'randrange') and hasattr(random, 'randint') and hasattr(random, 'choice')