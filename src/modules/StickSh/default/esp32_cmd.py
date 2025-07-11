import esp32
import machine

def execute(args):
    if len(args) == 1:
        return "Usage: esp32 {args}\nArguments:\ntemp - Estimated temperature of esp32 chip\ntemp_raw - Raw temperature os esp32 chip\nuid - Get chip uid"
    else:
        if args[1] == "temp":
            temp_c = (esp32.raw_temperature() - 32) / 1.8
            return f"{temp_c:.1f}C"
        elif args[1] == "temp_raw":
            return str(esp32.raw_temperature())
        elif args[1] == "uid":
            uid = machine.unique_id()
            return "UID: " + "".join("{:02x}".format(b) for b in uid)
        else:
            return "Usage: esp32 {args}\nArguments:\ntemp - Estimated temperature of esp32 chip\ntemp_raw - Raw temperature os esp32 chip\nuid - Get chip uid"