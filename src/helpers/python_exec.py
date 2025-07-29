import fonts.def_8x8 as f8x8

import modules.io_manager as io_man

tft = io_man.get_tft()
    
def open_file(path):
    tft.text(f8x8, "Python executor",0,0,2016)
    tft.text(f8x8, "File: " + path,0,8,65535)
    tft.text(f8x8, "Script execution in progress",0,16,65535)
    exec(open(path).read())
