import os

def execute(args):
    if len(args) >= 2:
        try:
            os.mkdir(args[1])
            return ""
        except Exception as e:
            return "Execution error:\n" + str(e)
    else:
        return "Usage: mkdir {filename}"
