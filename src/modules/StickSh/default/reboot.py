import machine

def execute(args):
    machine.freq(80000000)
    os.sync()
    machine.reset()
    return "Rebooting"

