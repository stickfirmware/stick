import os
import random

import modules.cache as cache

def seed():
    random.seed(int.from_bytes(os.urandom(64), "little"))
    cache.set('random_seeded', True)