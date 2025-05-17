import os

def execute(args):
    if len(args) != 1:
        try:
            os.chdir(args[1])
            return os.getcwd()
        except Exception as e:
            return "Execution error:\n" + str(e)