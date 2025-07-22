import time

uptime = time.ticks_ms()
uptime_bootloader = None
uptime_loaded = None

def get_formated(value):
    elapsed_ms = time.ticks_diff(time.ticks_ms(), value)
    total_seconds = elapsed_ms // 1000

    d = total_seconds // 86400
    h = (total_seconds % 86400) // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60

    return f"{d}d {h}h {m}m {s}s"

def get_diff_seconds(first, second):
    elapsed_ms = time.ticks_diff(first, second)
    total_seconds = elapsed_ms / 1000
    return total_seconds