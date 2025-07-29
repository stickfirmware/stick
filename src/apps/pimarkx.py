import time
import machine
import os
import modules.menus as menus
import fonts.def_8x8 as f8x8
import modules.os_constants as osc
import modules.printer as printer

frequencies = [osc.ULTRA_SLOW_FREQ, osc.SLOW_FREQ, osc.BASE_FREQ, osc.FAST_FREQ, osc.ULTRA_FREQ]
testingTime = 15
resultpath = "/temp/benchmark_results.txt"

result = ""

import modules.io_manager as io_man

button_a = io_man.get_btn_a()
button_b = io_man.get_btn_b()
button_c = io_man.get_btn_c()
tft = io_man.get_tft()

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
    result += "Frequency: {} MHz\n".format(freq // 1000000)
    result += "Iterations: {}\n".format(count)
    result += "it per MHz: {:.2f}\n".format(count / (freq / 1_000_000))
    result += "Pi ~= {}\n".format(pi)
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
    result += "Settings:\n"
    result += "Testing time (Per freq): {}s\n".format(testingTime)
    result += "Frequencies: {}\n".format(frequencies)
    result += "-" * 20 + "\n"
    result += "Tip:\n"
    result += "Results may be different when running in Stick firmware or standalone, when comparing platforms it is recomended to run PiMarkX in the same way or it can be inaccurate.\n"
    result += "-" * 20 + "\n"
    
def saveResult():
    with open(resultpath, "w") as f:
        f.write(result)
        f.close()

def run():
    global button_c, button_a, button_b, tft
    button_a = io_man.get_btn_a()
    button_b = io_man.get_btn_b()
    button_c = io_man.get_btn_c()
    tft = io_man.get_tft()
    
    render = menus.menu("Do you want to run it?", [("Yes", 1), ("No", None)])
    if render == None:
        return
    pre_res()
    tft.fill(0)
    tft.text(f8x8, "PiMarkX",0,0,2016)
    tft.text(f8x8, "Prepairing...",0,8,65535)
    seconds = len(frequencies) * testingTime
    tft.text(f8x8, "Estimated testing time: " + format_duration(seconds),0,20,65535)
    textpos = 28
    for freq in frequencies:
        tft.text(f8x8, "Testing on " + str(freq // 1000000) + " MHz",0,textpos,65535)
        machine.freq(freq)
        time.sleep(1)
        count, pi = pi_benchmark(testingTime * 1000)
        res_add(freq, count, pi)
        textpos += 8
    tft.fill(0)
    tft.text(f8x8, "Benchmark finished", 0, 0, 65535)
    time.sleep(1)
    saveResult()
    import modules.open_file as open_file
    open_file.openMenu(resultpath)
    
def run_no_gui():
    printer.log("\nPiMarkX")
    pre_res()
    for freq in frequencies:
        tft.text(f8x8, "Testing on " + str(freq // 1000000) + " MHz",0,textpos,65535)
        machine.freq(freq)
        time.sleep(1)
        count, pi = pi_benchmark(testingTime * 1000)
        res_add(freq, count, pi)
    saveResult()

    printer.log("Result saved to: " + resultpath)
    