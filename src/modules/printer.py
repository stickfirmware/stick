import modules.osconstants as osc

def log(msg):
    if osc.ENABLE_DEBUG_PRINTS == True:
        print(str(msg))