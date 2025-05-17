import modules.UNIT.CardKB as CardKB
import modules.StickSh.executor as term_exec
import modules.menus as menus
import machine
import time
import fonts.def_8x8 as f8x8

tft = None

# Banned bytes
banned_bytes = [ 
    b'\x00',  # NULL
    b'\x08',  # Backspace
    b'\x09',  # Tab
    b'\x0a',  # Line Feed (LF, \n)
    b'\x0d',  # Carriage Return (CR, \r)
    b'\x1b',  # Escape
    b'\x7f',  # Delete
]

# b'\x08' - FN + C

def set_tft(tft_n):
    global tft
    tft = tft_n
    
def update_top(text):
    tft.fill_rect(3, 3, 234, 13, 0)
    tft.text(f8x8, text,5,5,65535)
    
def run():
    # Render terminal
    tft.fill_rect(0, 0, 240, 3, 65535)
    tft.fill_rect(0, 16, 240, 3, 65535)
    tft.fill_rect(0, 132, 240, 3, 65535)
    tft.fill_rect(0, 0, 3, 135, 65535)
    tft.fill_rect(237, 0, 3, 135, 65535)
    tft.fill_rect(3, 3, 234, 13, 0) # Clear top bar
    tft.fill_rect(3, 19, 234, 113, 0)
    tft.text(f8x8, "Terminal | Loading",5,5,65535)
    
    # Setup term executor
    term_exec.set_tft(tft)
    term_exec.execute('reload')
    
    # Test CardKB
    failed = False
    try:
        CardKB.init()
    except:
        failed = True
        
    if failed == True:
        menus.menu("Please connect CardKB first!", [("OK", 1)])
        return
    
    # Terminal i/o
    term_ok = True
    term_upd = True
    input_text = ""
    
    term_exec.term_clear()
    term_exec.term_print("Welcome to the StickSh terminal!\nWarning! Only for advanced users!\nYou can destroy your system there!\nTo exit press ESC.")
    
    update_top("Terminal")
    while term_ok == True:
        if term_upd == True:
            # Update input
            tft.fill_rect(4, 123, 233, 8, 0)
            tft.text(f8x8, ">",4,123,4064)
            chunks = term_exec.to_chunks(input_text)
            last_chunk = chunks[-1] if chunks else ""
            tft.text(f8x8, last_chunk,14,123,65535)
            
            term_upd = False
        
        try:
            KB_Data = CardKB.read()
        except:
            menus.menu("Please connect CardKB first!", [("OK", 1)])
            term_ok = False
            return
        KB_Text = CardKB.decode(KB_Data)
        if KB_Data != b'\x00':
            print(str(KB_Data))
            print(str(KB_Text))
            # Backspace
            if KB_Data == b'\x08':
                input_text = input_text[:-1]
            # Escape
            elif KB_Data == b'\x1b':
                term_ok = False
            # Enter
            elif KB_Data == b'\r':
                term_exec.execute(input_text)
                input_text = ""
            # Up
            elif KB_Data == b'\xb5':
                term_exec.term_up()
                term_exec.term_render(term_exec.display)          
            # Down
            elif KB_Data == b'\xb6':
                term_exec.term_down()
                term_exec.term_render(term_exec.display)
            # FN + C
            elif KB_Data == b'\xa8':
                input_text = ""
            # FN + L
            elif KB_Data == b'\xa2':
                input_text = ""
                term_exec.term_clear()
            # Display char
            elif KB_Text != None and KB_Data not in banned_bytes:
                input_text += KB_Text
            term_upd = True
        
        time.sleep(0.01)
    