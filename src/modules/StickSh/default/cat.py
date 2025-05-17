import os

def execute(args):
    if len(args) != 1:
        try:
            with open(args[1], 'r') as file:
                data = file.read()
            return data
        except Exception as e:
            return "Execution error:\n" + str(e)
    else:
        return "Usage: cat {filename}"


