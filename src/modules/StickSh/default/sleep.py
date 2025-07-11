import time

def execute(args):
    if len(args) >= 2:
        try:
            time.sleep(float(args[1]))
            return ""
        except Exception as e:
            return "Execution error:\n" + str(e)
    else:
        return "Usage: sleep {seconds}"

