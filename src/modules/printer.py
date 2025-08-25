import modules.os_constants as osc

def log(msg):
    if osc.ENABLE_DEBUG_PRINTS == True:
        print(str(msg))
        
def log_cleaner(msg):
    if osc.ENABLE_DEBUG_PRINTS and osc.LESS_RAM_CLEANER_OUTPUT == False:
        print(str(msg))