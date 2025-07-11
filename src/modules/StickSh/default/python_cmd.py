import modules.StickSh.executor as texec

def execute(args):
    if len(args) >= 2:
        exec(open(args[1]).read())
    else:
        return "Usage: python {file}\nWarning: python command doesn't output print() to terminal, just does exec(), also it needs to be compatible with MicroPython."