import time

import modules.io_manager as io_man

def run():
    tft = io_man.get("tft")
    
    tft.fill(4000)
    
    time.sleep(5)