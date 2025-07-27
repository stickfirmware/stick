import modules.nvs as nvs
import modules.error_db as error_db
import fonts.def_16x32 as f16x32
import fonts.def_8x8 as f8x8
import time

def run_check(tft, n_crash):
    latest = nvs.get_int(n_crash, "latest")
    if latest != 0 and latest != None:
        print("It looks like device has crashed recently, showing prompt!")
        code = nvs.get_int(n_crash, "latest")
        tft.fill(7003)
        tft.text(f16x32, "Info",0,0,65535,7003)
        tft.text(f8x8, "It seems like your device has",0,32,65535,7003)
        tft.text(f8x8, "crashed recently!",0,40,65535,7003)
        tft.text(f8x8, "Log path:",0,84,7971,7003)
        tft.text(f8x8, nvs.get_string(n_crash, "latestPath"),0,92,65535,7003)
        tft.text(f8x8, "Error code: " + str(code),0,100,7971,7003)
        print("Checking error code in error_db")
        tft.text(f8x8, error_db.check_code(code),0,108,7971,7003)
        tft.text(f8x8, "Booting in around 8s",0,127,65535,7003)
        tft.text(f8x8, str(nvs.get_int(n_crash, "crashCount")),0,116,65535,7003)
        time.sleep(8)
        nvs.set_int(n_crash, "latest", 0)