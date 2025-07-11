import gc

def execute(args):
    if len(args) >= 2:
        if args[1] == "collect":
            gc.collect()
            return "Garbage collector collected!"
        elif args[1] == "mem_free":
            return str(gc.mem_free() // 1024) + "KB"
        elif args[1] == "enable":
            gc.enable()
            return "Garbage collector enabled!"
        elif args[1] == "disable":
            gc.disable()
            return "Garbage collector disabled!"
        else:
            return "Unknown argument, available commands:\ncollect\nmem_free\nenable\ndisable"
    else:
        return "Usage: gc {args}"

