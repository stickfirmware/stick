import modules.json as json
import fonts.def_8x8 as f8x8
import gc
import os
import sys

PATH = None
tft = None

variables = {}

import re

def replace_vars(text, varias):
    def repl(match):
        var_name = match.group(1)
        return str(varias.get(var_name, f"*{var_name}*"))
    return re.sub(r'\*([a-zA-Z_][a-zA-Z0-9_]*)\*', repl, text)


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

def term_pup():
    global current_in_minus
    max_scroll = max(0, len(display) - 12)
    if current_in_minus + 12 <= max_scroll:
        current_in_minus += 12
    else:
        current_in_minus = max_scroll

def term_pdown():
    global current_in_minus
    if current_in_minus - 12 >= 0:
        current_in_minus -= 12
    else:
        current_in_minus = 0


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
    txt = str(text)
    
    # Split text to lines
    lines = txt.split('\n')
    
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
    argss = replace_vars(args, variables)
    argsSplit = argss.split()
    if len(args) == 0:
        return ""
    cmd = argsSplit[0]
    if not argsSplit:
        return
    try:
        cmdPath = ""
        if PATH:
            cmdPath = PATH[cmd]       
        if cmdPath.endswith(".py"):
            parent = cmdPath.rsplit("/", 1)[0] if "/" in cmdPath else ""
            if parent and parent not in sys.path:
                sys.path.append(parent)
            name = cmdPath.rsplit("/", 1)[-1].rsplit(".", 1)[0]
            comd = __import__(name)
            if name in sys.modules:
                del sys.modules[name]
            return comd.execute(argsSplit)
        else:
            if cmd == "reload":
                return reload_path()
            elif cmd == "which":
                if len(argsSplit) == 2:
                    
                    return PATH[argsSplit[1]]
                else:
                    return "Please provide command!"
            elif cmd == "clear-cache":
                for name in cache:
                    if name in sys.modules:
                        del sys.modules[name]
                cache.clear()
                gc.collect()
            return "Unknown command / Error"
    except KeyError as e:
        
        try:
            if cmd == "reload":
                return reload_path()
            elif cmd == "which":
                if len(argsSplit) == 2:
                    return PATH[argsSplit[1]]
                else:
                    return "Please provide command!"
            elif cmd == "cls" or cmd == "clear":
                term_clear()
                return None
            elif cmd == "clear-cache":
                for name in cache:
                    if name in sys.modules:
                        del sys.modules[name]
                cache.clear()
                gc.collect()
            else:
                return "Unknown command / Error"
        except:
               return "Couldn't execute command!\n" + str(e) 
            
        return "Unknown command / Error"
    except Exception as e:
        return "Couldn't execute command!\n" + str(e)
    
def executep(args):
    execut = execute(args)
    if execut == None:
        print("There was nothing to print")
    else:
        term_print(execut)