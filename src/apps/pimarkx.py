import time
import machine
import os
import modules.menus as menus
import fonts.def_8x8 as f8x8

frequencies = [20000000, 40000000, 80000000, 160000000, 240000000]
testingTime = 15
resultpath = "/temp/benchmark_results.txt"

button_a = None
button_b = None
button_c = None
tft = None

def set_btf(bta, btb, btc, ttft):
    global button_a
    global button_b
    global button_c
    global tft
    
    button_a = bta
    button_b = btb
    button_c = btc
    tft = ttft

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

def save_result(freq, count, pi):
    try:
        with open(resultpath, "a") as f:
            f.write("Frequency: {} MHz\n".format(freq // 1000000))
            f.write("Iterations: {}\n".format(count))
            f.write("it per MHz: {:.2f}\n".format(count / (freq / 1_000_000)))
            f.write("Pi ~= {}\n".format(pi))
            f.write("-" * 20 + "\n")
    except Exception as e:
        print("Saving error:", e)

def presave():
    try:
        listd = os.listdir("/")
        if "temp" not in listd:
            os.mkdir("/temp")
        with open(resultpath, "w") as f:
            f.write("-" * 20 + "\n")
            f.write("PiMarkX\n")
            f.write("A part of Kitki30 Stick Software\n")
            f.write("-" * 20 + "\n")
            f.write("Settings:\n")
            f.write("Testing time (Per freq): {}s\n".format(testingTime))
            f.write("Frequencies: {}\n".format(frequencies))
            f.write("-" * 20 + "\n")
    except Exception as e:
        print("Saving error:", e)

def run():
    print("\nPiMarkX")
    
    presave()
    render = menus.menu("Do you want to run it?", [("Yes", 1), ("No", None)])
    if render == None:
        return
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
        save_result(freq, count, pi)
        textpos += 8
    import modules.openFile as openfile
    openfile.openMenu(resultpath)