import modules.StickSh.executor as texec
import time

def execute(args):
    if len(args) >= 2:
        args.pop(0)
        cmd_str = " ".join(args)
        start = time.ticks_us()
        texec.executep(cmd_str)
        end = time.ticks_us()
        delta_us = time.ticks_diff(end, start)
        delta_s = delta_us / 1_000_000
        return f"Execution time: {delta_s:.3f}s"
    else:
        return "Usage: time {command}"

