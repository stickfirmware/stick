import modules.StickSh.executor as texec

def try_convert(value):
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            if value.lower() in ["true", "false"]:
                return value.lower() == "true"
            return value

def execute(args):
    if len(args) >= 2:
        if len(args) == 2:
            return texec.variables[args[1]]
        if len(args) >= 3:
            if len(args) == 3:
                texec.variables[args[1]] = try_convert(args[2])
                return texec.variables[args[1]]
            else:
                if args[3] == "string":
                    texec.variables[args[1]] = str(args[2])
                elif args[3] == "bool":
                    texec.variables[args[1]] = args[2].lower() == "true"
                elif args[3] == "int":
                    texec.variables[args[1]] = int(args[2])
                elif args[3] == "float":
                    texec.variables[args[1]] = float(args[2])
                else:
                    texec.variables[args[1]] = try_convert(args[2])
                return texec.variables[args[1]]
    else:
        return "Usage: var {var_name} (new_value) (value_type)\nGets or sets variable.\nvar_name - Name of variable\nnew_walue - Optional. New value\nvalue_type - Optional. string, int, float or bool. Default - auto check."
