import modules.os_constants as osc

def log(msg):
    if osc.ENABLE_DEBUG_PRINTS == True:
        print(str(msg))