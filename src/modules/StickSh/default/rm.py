import os

def execute(args):
    if len(args) != 1:
        try:
            os.remove(args[1])
            return ""
        except Exception as e:
            return "Execution error:\n" + str(e)
    else:
        return "Usage: rm {filename}"


