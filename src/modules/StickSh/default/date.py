import time

def execute(args):
    tm = time.localtime()
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(tm[0], tm[1], tm[2], tm[3], tm[4], tm[5])