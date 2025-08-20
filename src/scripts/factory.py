import modules.files as files
from modules.printer import log

log("Factory reseting")

log("Delete usr")
try:
    files.rmdir_recursive("/usr")
except:
    log("Failed!")

log("Delete temp")
try:
    files.rmdir_recursive("/temp")
except:
    log("Failed!")
    
log("Reset NVS, bye!")

import scripts.reset_nvs