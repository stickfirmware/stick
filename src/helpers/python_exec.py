import fonts.def_8x8 as f8x8

import modules.io_manager as io_man
from modules.translate import get as l_get

tft = io_man.get('tft')
    
def open_file(path):
    tft.text(f8x8, l_get("apps.python_executor.name"),0,0,2016)
    tft.text(f8x8, l_get("apps.python_executor.file") + path,0,8,65535)
    tft.text(f8x8, l_get("apps.python_executor.in_progress"),0,16,65535)
    exec(open(path).read())
