import modules.StickSh.executor as texec

def try_convert(value):
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            try:
                return bool(value)
            except ValueError:
                return value

def execute(args):
    if len(args) >= 3:
        # Parse condition
        cond = args[1].split(";")
        
        var1 = try_convert(cond[0])
        condit = cond[1]
        var2 = try_convert(cond[2])
        
        # Pop condition leave only the command
        args.pop(0)
        args.pop(0)
        
        # Test condition
        if condit == "==":
            if var1 == var2:
                return texec.execute(" ".join(args))
        elif condit == ">=":
            if var1 >= var2:
                return texec.execute(" ".join(args))
        elif condit == "<=":
            if var1 <= var2:
                return texec.execute(" ".join(args))
        elif condit == "!=":
            if var1 != var2:
                return texec.execute(" ".join(args))
        elif condit == ">":
            if var1 > var2:
                return texec.execute(" ".join(args))
        elif condit == "<":
            if var1 < var2:
                return texec.execute(" ".join(args))
        else:
            return "Unknown operator: " + condit
    else:
        return "Usage: if {condition} {command}"

