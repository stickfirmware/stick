import esp32

def execute(args):
    if len(args) == 1:
        return "Usage: esp32 {args}\nArguments:\ntemp - Estimated temperature of esp32 chip\ntemp_raw - Raw temperature os esp32 chip"
    else:
        if args[1] == "temp":
            temp_c = (esp32.raw_temperature() - 32) / 1.8
            return f"{temp_c:.1f}°C"
        elif args[1] == "temp_raw":
            return str(esp32.raw_temperature())
        else:
            return "Usage: esp32 {args}\nArguments:\ntemp - Estimated temperature of esp32 chip\ntemp_raw - Raw temperature os esp32 chip"