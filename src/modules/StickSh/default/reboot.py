import machine

def execute(args):
    machine.freq(80000000)
    machine.reset()
    return "Rebooting"

