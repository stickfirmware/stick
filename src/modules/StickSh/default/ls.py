import os

def execute(args):
    if len(args) == 1:
        try:
            return str(os.listdir())
        except Exception as e:
            return "Execution error:\n" + str(e)
    else:
        try:
            return str(os.listdir(args[1]))
        except Exception as e:
            return "Execution error:\n" + str(e)