import modules.files as files
from modules.printer import Levels as log_levels
from modules.printer import log

log("Factory reseting")

log("Delete usr", log_levels.DEBUG)
try:
    files.rmdir_recursive("/usr")
except Exception:
    log("Failed!", log_levels.DEBUG)

log("Delete temp", log_levels.DEBUG)
try:
    files.rmdir_recursive("/temp")
except Exception:
    log("Failed!", log_levels.DEBUG)

log("Delete user packages")
try:
    files.rmdir_recursive("/apps/thirdparty")
    files.rmdir_recursive("/modules/thirdparty")
except Exception:
    log("Failed!", log_levels.DEBUG)
    
log("Reset NVS, bye!", log_levels.DEBUG)

import scripts.reset_nvs # noqa