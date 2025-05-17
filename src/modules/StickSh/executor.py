import modules.json as json
import fonts.def_8x8 as f8x8
import gc
import os
import sys

PATH = None
tft = None



def set_tft(tft_o):
    global tft
    tft = tft_o
    
def to_chunks(string, chunk_size=28):
    return [string[i:i+chunk_size] for i in range(0, len(string), chunk_size)]

current_in_minus = 0
display = []

def term_up():
    global current_in_minus
    max_scroll = max(0, len(display) - 12)
    if current_in_minus < max_scroll:
        current_in_minus += 1

def term_down():
    global current_in_minus
    if current_in_minus > 0:
        current_in_minus -= 1

def term_render(arr):
    # 12 lines
    # Start from 4x, 20y
    
    # Clear LCD (without top bar)
    tft.fill_rect(0, 0, 240, 3, 65535)
    tft.fill_rect(0, 16, 240, 3, 65535)
    tft.fill_rect(0, 132, 240, 3, 65535)
    tft.fill_rect(0, 0, 3, 135, 65535)
    tft.fill_rect(237, 0, 3, 135, 65535)
    tft.fill_rect(3, 19, 234, 113, 0)
    
    total = len(arr)
    start = total - 12 - current_in_minus
    
    if start < 0:
        start = 0
    
    # Render
    curr_line = 0
    for i in arr[start:start+12]:
        d = i.strip(" ")
        tft.text(f8x8, d,4,(20 + (8 * curr_line)),65535)
        curr_line += 1
    
def term_conv(text):
    # Convert text to lines and chunks so it can fit on display
    
    # Split text to lines
    lines = text.split('\n')
    
    # Split all lines to 30 letter chunks (lines so it doesnt go out of the display)
    ready_text = []
    for i in lines:
        parts = to_chunks(i)
        ready_text.append(tuple(parts))
    
    # Flat the array to strings
    flat = [item for tup in ready_text for item in tup]
    return flat

def term_print(text):
    global display
    global current_in_minus
    conv = term_conv(text)
    display.extend(conv)
    current_in_minus = 0
    term_render(display)

def term_clear():
    global display
    global current_in_minus
    display.clear()
    current_in_minus = 0
    term_render(display)

def reload_path():
    global PATH
    PATH = json.read("/modules/StickSh/PATH.json")
    return "PATH reloaded"

def execute(args):
    argsSplit = args.split()
    cmd = argsSplit[0]
    if not argsSplit:
        return
    try:
        cmdPath = ""
        if PATH:
            cmdPath = PATH[cmd]
        if cmd == "reload":
            term_print("> reload")
            term_print(reload_path())
        elif cmd == "which":
            term_print("> which")
            if len(argsSplit) == 2:
                term_print(PATH[argsSplit[1]])
            else:
                term_print("Please provide command!")
        elif cmdPath.endswith(".py"):
            term_print("> " + cmd)
            parent = cmdPath.rsplit("/", 1)[0] if "/" in cmdPath else ""
            if parent and parent not in sys.path:
                sys.path.append(parent)
            name = cmdPath.rsplit("/", 1)[-1].rsplit(".", 1)[0]
            
            comd = __import__(name)
            term_print(comd.execute(argsSplit))
            if name in sys.modules:
                del sys.modules[name]
            gc.collect()
        else:
            term_print("> " + cmd)
            term_print("Unknown command")
    except KeyError as e:
        term_print("> " + cmd)
        term_print("Unknown command")
    except Exception as e:
        term_print("Couldn't execute command!\n" + str(e))