import os

def execute(args):
    if len(args) >= 2:
        try:
            if os.path.exists(args[1]):
                return "File" + args[1] + "already exists!"
            else:
                open(args[1], "w").close()
            return args[1]
        except Exception as e:
            return "Execution error:\n" + str(e)
    else:
        return "Usage: touch {filename}"
    

