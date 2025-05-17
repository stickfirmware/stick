import os, sys
import network

def execute(args):
    try:
        implementation = str(sys.implementation.name)
    except:
        implementation = "unknown / custom"
    if len(args) == 1:
        return implementation
    else:
        if args[1] == "-s":
            return implementation
        elif args[1] == "-a":
            try:
                return str(sys.implementation.name) + "@" + network.hostname()  + " " + str(os.uname().version) + "; " + str(os.uname().machine)
            except:
                return "unknown / custom"
        elif args[1] == "-n":
            return network.hostname()
        elif args[1] == "-r":
            return os.uname().version
        elif args[1] == "-m":
            return os.uname().machine
        else:
            return "Usage: uname (args)\nUsage almost like on linux!"