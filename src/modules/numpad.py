import fonts.def_8x8 as f8x8
import fonts.def_8x16 as f8x16
import fonts.def_16x16 as f16x16
import modules.cardputer_kb as ckb
import modules.os_constants as osc
import modules.menus as menus
import modules.io_manager as io_man

button_a = io_man.get_btn_a()
button_b = io_man.get_btn_b()
button_c = io_man.get_btn_c()
tft = io_man.get_tft()

def writeNums(is_keyboard, number=99):
    n = [65535, 65535, 65535, 65535, 65535, 65535, 65535, 65535, 65535, 65535, 65535, 65535]
    
    if not number == 99:
        n[number] = 10208
    
    if is_keyboard == False:
        # Row 1
        tft.text(f16x16, "|",45,43,65535)
        tft.text(f16x16, "1",65,43,n[0])
        tft.text(f16x16, "|",85,43,65535)
        tft.text(f16x16, "2",105,43,n[1])
        tft.text(f16x16, "|",125,43,65535)
        tft.text(f16x16, "3",145,43,n[2])
        tft.text(f16x16, "|",165,43,65535)
        
        # Row 2
        tft.text(f16x16, "|",45,59,65535)
        tft.text(f16x16, "4",65,59,n[3])
        tft.text(f16x16, "|",85,59,65535)
        tft.text(f16x16, "5",105,59,n[4])
        tft.text(f16x16, "|",125,59,65535)
        tft.text(f16x16, "6",145,59,n[5])
        tft.text(f16x16, "|",165,59,65535)
        
        # Row 3
        tft.text(f16x16, "|",45,75,65535)
        tft.text(f16x16, "7",65,75,n[6])
        tft.text(f16x16, "|",85,75,65535)
        tft.text(f16x16, "8",105,75,n[7])
        tft.text(f16x16, "|",125,75,65535)
        tft.text(f16x16, "9",145,75,n[8])
        tft.text(f16x16, "|",165,75,65535)
        
        # Row 4
        tft.text(f16x16, "|",45,91,65535)
        tft.text(f16x16, ">",65,91,n[9])
        tft.text(f16x16, "|",85,91,65535)
        tft.text(f16x16, "0",105,91,n[10])
        tft.text(f16x16, "|",125,91,65535)
        tft.text(f16x16, "X",145,91,n[11])
        tft.text(f16x16, "|",165,91,65535)
    else:
        # Row 1
        tft.text(f8x8, "|", 5, 43, 65535)
        tft.text(f8x8, "1", 15, 43, n[0])
        tft.text(f8x8, "|", 57, 43, 65535)
        tft.text(f8x8, "2 abc", 69, 43, n[1])
        tft.text(f8x8, "|", 121, 43, 65535)
        tft.text(f8x8, "3 def", 131, 43, n[2])
        tft.text(f8x8, "|", 183, 43, 65535)

        # Row 2
        tft.text(f8x8, "|", 5, 59, 65535)
        tft.text(f8x8, "4 ghi", 15, 59, n[3])
        tft.text(f8x8, "|", 57, 59, 65535)
        tft.text(f8x8, "5 jkl", 69, 59, n[4])
        tft.text(f8x8, "|", 121, 59, 65535)
        tft.text(f8x8, "6 mno", 131, 59, n[5])
        tft.text(f8x8, "|", 183, 59, 65535)

        # Row 3
        tft.text(f8x8, "|", 5, 75, 65535)
        tft.text(f8x8, "7pqrs", 15, 75, n[6])
        tft.text(f8x8, "|", 57, 75, 65535)
        tft.text(f8x8, "8 tuv", 69, 75, n[7])
        tft.text(f8x8, "|", 121, 75, 65535)
        tft.text(f8x8, "9 wxyz", 131, 75, n[8])
        tft.text(f8x8, "|", 183, 75, 65535)

        # Row 4
        tft.text(f8x8, "|", 5, 91, 65535)
        tft.text(f8x8, "Menu", 15, 91, n[9])
        tft.text(f8x8, "|", 57, 91, 65535)
        tft.text(f8x8, "0space", 69, 91, n[10])
        tft.text(f8x8, "|", 121, 91, 65535)
        tft.text(f8x8, "Symbol", 131, 91, n[11])
        tft.text(f8x8, "|", 183, 91, 65535)

# Refresh io
def load_io():
    global button_c, button_a, button_b, tft
    button_a = io_man.get_btn_a()
    button_b = io_man.get_btn_b()
    button_c = io_man.get_btn_c()
    tft = io_man.get_tft()

def numpad(title, maxlen=0, hideInput=False):
    load_io()
    import time
    tft.fill(0)
    tft.fill_rect(0, 0, 240, 3, 65535)
    tft.fill_rect(0, 132, 240, 3, 65535)
    tft.fill_rect(0, 0, 3, 135, 65535)
    tft.fill_rect(237, 0, 3, 135, 65535)
    tft.fill_rect(3, 3, 234, 13, 0)
    tft.fill_rect(3, 19, 234, 113, 0)
    
    tft.fill_rect(0, 16, 240, 3, 65535)
    tft.text(f8x8, str(title),5,5,65535)
    
    inp = ""
    selection = 0
    tft.fill_rect(0, 39, 240, 3, 65535)
    tft.text(f8x16, str(inp),5,22,65535)
    
    upd = True
    work = True
    while work == True:
        time.sleep(osc.LOOP_WAIT_TIME)
        if upd == True:
            writeNums(False, selection)
            tft.fill_rect(3, 19, 234, 20, 0)
            chunks = [inp[i:i+28] for i in range(0, len(inp), 28)]
            last_chunk = chunks[-1] if chunks else ""
            if hideInput == False:
                tft.text(f8x16, last_chunk, 5, 22, 65535)
            else:
                tft.text(f8x16, str("*" * len(last_chunk)),5,22,65535)
            upd = False
        if button_b.value() == 0:
            while button_b.value() == 0:
                time.sleep(osc.DEBOUNCE_TIME)
            if selection == 11:
                selection = 0
            else:
                selection += 1
            upd = True
        elif button_a.value() == 0:
            while button_a.value() == 0:
                time.sleep(osc.DEBOUNCE_TIME)
            if selection == 11:
                selection = 0
                inp = None
                work = False
            elif selection == 9:
                selection = 0
                work = False
            elif selection == 10:
                upd = True
                selection = 0
                if maxlen == 0:
                    inp += str(0)
                else:
                    if len(inp) < maxlen:
                        inp += str(0)
            else:
                upd = True
                print(selection)
                if maxlen == 0:
                    inp += str(selection + 1)
                else:
                    if len(inp) < maxlen:
                        inp += str(selection + 1)
        elif button_c.value() == 0:
            while button_c.value() == 0:
                time.sleep(osc.DEBOUNCE_TIME)
            if len(inp) == 0:
                selection = 0
                inp = None
                work = False
            else:
                inp = inp[:-1]
            upd = True
    return inp


def _KEYBOARD_CARDKB(title, maxlen=0, hideInput=False):
    import time

    inp = ""
    prev_letter = None
    last_press_time = 0
    debounce_delay = osc.DEBOUNCE_TIME

    upd = True
    big_update = True
    work = True

    ignored_keys = {"ctrl", "fn", "alt", "tab", "opt", "Aa"}

    while work:
        time.sleep(osc.LOOP_WAIT_TIME)
        curr_letter = ckb.scan_and_map()

        now = time.ticks_ms()

        if big_update:
            tft.fill(0)
            tft.fill_rect(0, 0, 240, 3, 65535)
            tft.fill_rect(0, 132, 240, 3, 65535)
            tft.fill_rect(0, 0, 3, 135, 65535)
            tft.fill_rect(237, 0, 3, 135, 65535)
            tft.fill_rect(3, 3, 234, 13, 0)
            tft.fill_rect(3, 19, 234, 113, 0)
            tft.fill_rect(0, 16, 240, 3, 65535)
            tft.text(f8x8, str(title), 5, 5, 65535)
            big_update = False
            upd = True

        if upd:
            tft.fill_rect(3, 19, 234, 20, 0)
            chunks = [inp[i:i + 28] for i in range(0, len(inp), 28)]
            last_chunk = chunks[-1] if chunks else ""
            display_text = "*" * len(last_chunk) if hideInput else last_chunk
            tft.text(f8x16, display_text, 5, 22, 65535)
            upd = False

        if curr_letter:
            key = curr_letter[-1]

            if key == prev_letter and time.ticks_diff(now, last_press_time) < debounce_delay * 1000:
                continue

            prev_letter = key
            last_press_time = now

            if key.lower() in ignored_keys:
                continue

            if key == "enter":
                menu = menus.menu("Menu", [("Confirm", 1), ("Exit", 2), ("Back", 3)])
                if menu == 1:
                    return inp
                elif menu == 2:
                    return None
                else:
                    upd = True
                    big_update = True

            elif key == "backspace":
                if inp:
                    inp = inp[:-1]
                    upd = True

            elif len(key) == 1:
                if maxlen == 0 or len(inp) < maxlen:
                    inp += key
                    upd = True
            
def keyboard(title, maxlen=0, hideInput=False):
    load_io()
    import time
    
    if osc.INPUT_METHOD == 2:
        return _KEYBOARD_CARDKB(title, maxlen, hideInput)
    
    keys = [
        ["1", ".", ",", "!", "?"],
        ["2", "a", "b", "c", "A", "B", "C"],
        ["3", "d", "e", "f", "D", "E", "F"],
        ["4", "g", "h", "i", "G", "H", "I"],
        ["5", "j", "k", "l", "J", "K", "L"],
        ["6", "m", "n", "o", "M", "N", "O"],
        ["7", "p", "q", "r", "s", "P", "Q", "R", "S"],
        ["8", "t", "u", "v", "T", "U", "V"],
        ["9", "w", "x", "y", "z", "W", "X", "Y", "Z"],
        ["menu"],
        ["0", " "],
        ["sym"]
    ]

    inp = ""
    tmp_letter = ""
    last_selection = -1
    cycle_index = 0
    last_press_time = 0
    timeout = 1000

    upd = True
    big_update = True
    work = True
    selection = 0

    while work:
        time.sleep(osc.LOOP_WAIT_TIME)
        now = time.ticks_ms()

        if big_update:
            tft.fill(0)
            tft.fill_rect(0, 0, 240, 3, 65535)
            tft.fill_rect(0, 132, 240, 3, 65535)
            tft.fill_rect(0, 0, 3, 135, 65535)
            tft.fill_rect(237, 0, 3, 135, 65535)
            tft.fill_rect(3, 3, 234, 13, 0)
            tft.fill_rect(3, 19, 234, 113, 0)
            tft.fill_rect(0, 16, 240, 3, 65535)
            tft.text(f8x8, str(title),5,5,65535)
            big_update = False
            upd = True

        if upd:
            writeNums(True, selection)
            tft.fill_rect(3, 19, 234, 20, 0)
            chunks = [inp[i:i+28] for i in range(0, len(inp), 28)]
            last_chunk = chunks[-1] if chunks else ""
            if hideInput == False:
                tft.text(f8x16, last_chunk + tmp_letter, 5, 22, 65535)
            else:
                tft.text(f8x16, "*" * (len(last_chunk) + len(tmp_letter)), 5, 22, 65535)
            upd = False

        if tmp_letter and time.ticks_diff(now, last_press_time) > timeout:
            inp += tmp_letter
            tmp_letter = ""
            last_selection = -1
            cycle_index = 0
            upd = True

        if button_b.value() == 0:
            while button_b.value() == 0: time.sleep(0.02)

            if tmp_letter:
                inp += tmp_letter
                tmp_letter = ""
                cycle_index = 0
                last_selection = -1

            selection = (selection + 1) % 12
            upd = True

        elif button_a.value() == 0:
            while button_a.value() == 0: time.sleep(osc.DEBOUNCE_TIME)

            if selection == 9:
                menu = menus.menu("Menu", [("Confirm", 1), ("Exit", 2), ("Back", 3)])
                if menu == 1:
                    if tmp_letter:
                        inp += tmp_letter
                    return inp
                elif menu == 2:
                    return None
                else:
                    upd = True
                    big_update = True

            elif selection == 11:  # symbols
                symbol = menus.menu("Symbols", [
                    ("@", "@"), ("#", "#"), ("$", "$"), ("%", "%"),
                    ("&", "&"), ("*", "*"), ("(", "("), (")", ")"),
                    ("+", "+"), ("-", "-"), ("_", "_"), ("=", "="),
                    (".", "."), ("?", "?"), ("!", "!"), ("`", "`"),
                    ("~", "~"), ("^", "^"), ("*", "*"), ("[", "]"),
                    ("{", "}"), ("|", "|"), ("'", "'"), ('"', '"'),
                    ('<', '<'), ('>', '>'),
                    ("Back", None)
                ])
                if symbol and (maxlen == 0 or len(inp) < maxlen):
                    inp += symbol
                upd = True
                big_update = True

            elif selection == 10:
                if selection == last_selection:
                    cycle_index = (cycle_index + 1) % len(keys[10])
                else:
                    if tmp_letter:
                        inp += tmp_letter
                    cycle_index = 0
                    last_selection = selection

                tmp_letter = keys[10][cycle_index]
                last_press_time = now
                upd = True

            else:
                if selection == last_selection:
                    cycle_index = (cycle_index + 1) % len(keys[selection])
                else:
                    if tmp_letter:
                        inp += tmp_letter
                    cycle_index = 0
                    last_selection = selection

                tmp_letter = keys[selection][cycle_index]
                last_press_time = now
                upd = True

        elif button_c.value() == 0:
            while button_c.value() == 0: time.sleep(osc.DEBOUNCE_TIME)
            if tmp_letter:
                tmp_letter = ""
                last_selection = -1
                cycle_index = 0
            elif inp:
                inp = inp[:-1]
            else:
                return None
            upd = True