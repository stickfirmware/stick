import time
import os

import fonts.def_8x8 as f8x8

import modules.menus as menus
import modules.os_constants as osc
import modules.printer as printer
import modules.powersaving as ps
import modules.io_manager as io_man
from modules.translate import get as l_get

frequencies = [osc.ULTRA_SLOW_FREQ, osc.SLOW_FREQ, osc.BASE_FREQ, osc.FAST_FREQ, osc.ULTRA_FREQ]
testingTime = 15
resultpath = "/temp/benchmark_results.txt"

result = ""

button_a = io_man.get('button_a')
button_b = io_man.get('button_b')
button_c = io_man.get('button_c')
tft = None

def format_duration(seconds):
    m = seconds // 60
    s = seconds % 60
    return f"{m}m {s}s"

def pi_benchmark(duration_ms=15000):
    start = time.ticks_ms()
    i = 0
    pi = 0.0
    sign = 1.0

    while time.ticks_diff(time.ticks_ms(), start) < duration_ms:
        pi += sign / (2.0 * i + 1.0)
        sign *= -1
        i += 1

    return i, 4 * pi

def res_add(freq, count, pi):
    global result
    result += "{} {} MHz\n".format(l_get("apps.pimarkx.frequency"), freq // 1000000)
    result += "{} {}\n".format(l_get("apps.pimarkx.iterations"), count)
    result += "{} {:.2f}\n".format(l_get("apps.pimarkx.it_per_mhz"), count / (freq / 1_000_000))
    result += "{} ~= {}\n".format(l_get("apps.pimarkx.pi"), pi)
    result += "-" * 20 + "\n"

def pre_res():
    global result
    listd = os.listdir("/")
    if "temp" not in listd:
        os.mkdir("/temp")
    result += "-" * 20 + "\n"
    result += "PiMarkX\n"
    result += "A part of Stick firmware\n"
    result += "-" * 20 + "\n"
    result += f"{l_get("apps.pimarkx.settings")}\n"
    result += "{} {}s\n".format(l_get("apps.pimarkx.test_time"), testingTime)
    result += "{} {}\n".format(l_get("apps.pimarkx.frequencies"), frequencies)
    result += "-" * 20 + "\n"
    result += f"{l_get("apps.pimarkx.tip")}\n"
    result += f"{l_get("apps.pimarkx.different")}\n"
    result += "-" * 20 + "\n"
    
def saveResult():
    with open(resultpath, "w") as f:
        f.write(result)
        f.close()

def run():
    global button_c, button_a, button_b, tft
    button_a = io_man.get('button_a')
    button_b = io_man.get('button_b')
    button_c = io_man.get('button_c')
    tft = io_man.get('tft')
    
    render = menus.menu(l_get("apps.pimarkx.do_you_want_to_run"), 
                        [(l_get("menus.yes"), 1),
                         (l_get("menus.no"), None)])
    if render is None:
        return
    pre_res()
    tft.fill(0)
    tft.text(f8x8, "PiMarkX",0,0,2016)
    tft.text(f8x8, l_get("apps.pimarkx.preparing"),0,8,65535)
    textpos = 28
    for freq in frequencies:
        tft.text(f8x8, f"{l_get("apps.pimarkx.test_on")} " + str(freq // 1000000) + " MHz",0,textpos,65535)
        ps.set_freq(freq)
        time.sleep(1)
        count, pi = pi_benchmark(testingTime * 1000)
        res_add(freq, count, pi)
        textpos += 8
    tft.fill(0)
    tft.text(f8x8, l_get("apps.pimarkx.benchmark_finish"), 0, 0, 65535)
    time.sleep(1)
    saveResult()
    import modules.open_file as open_file
    open_file.openMenu(resultpath)
    
def run_no_gui():
    printer.log("\nPiMarkX")
    pre_res()
    for freq in frequencies:
        ps.set_freq(freq)
        time.sleep(1)
        count, pi = pi_benchmark(testingTime * 1000)
        res_add(freq, count, pi)
    saveResult()

    printer.log("Result saved to: " + resultpath)
    