import modules.CardKB as CardKB
import modules.StickSh.executor as term_exec
import modules.menus as menus
import machine
import modules.numpad as npad
import time
import fonts.def_8x8 as f8x8
import modules.io_manager as io_man

button_c = io_man.get_btn_c()
tft = io_man.get_tft()

# Refresh io
def load_io():
    global button_c, tft
    button_c = io_man.get_btn_c()
    tft = io_man.get_tft()

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

def update_screen(input_text, hard_update):
    if hard_update == True:
        tft.fill_rect(0, 0, 240, 3, 65535)
        tft.fill_rect(0, 16, 240, 3, 65535)
        tft.fill_rect(0, 132, 240, 3, 65535)
        tft.fill_rect(0, 0, 3, 135, 65535)
        tft.fill_rect(237, 0, 3, 135, 65535)
        tft.fill_rect(3, 3, 234, 13, 0) # Clear top bar
    
    tft.fill_rect(3, 19, 234, 113, 0)
    tft.fill_rect(4, 123, 233, 8, 0)
    tft.text(f8x8, ">",4,123,4064)
    chunks = term_exec.to_chunks(input_text)
    last_chunk = chunks[-1] if chunks else ""
    tft.text(f8x8, last_chunk,14,123,65535)

def set_tft(tft_n):
    global tft
    tft = tft_n
    
def update_top(text):
    tft.fill_rect(3, 3, 234, 13, 0)
    tft.text(f8x8, text,5,5,65535)
    
def run():
    load_io()
    # Render terminal
    update_screen("", True)
    tft.text(f8x8, "Terminal | Loading",5,5,65535)
    
    # Setup term executor
    term_exec.set_tft(tft)
    term_exec.executep('reload')
    
    on_screen_keyboard = False
    
    # Test CardKB
    failed = False
    try:
        CardKB.init()
    except:
        on_screen_keyboard = True

    # Terminal i/o
    term_ok = True
    term_upd = True
    input_text = ""
    
    term_exec.term_clear()
    term_exec.term_print("Welcome to the StickSh terminal!\nWarning! Only for advanced users!\nYou can destroy your system there!\nTo exit press ESC.")
    
    update_top("Terminal")
    while term_ok == True:
        if button_c.value() == 0:
            return
        
        if term_upd == True:
            # Update input
            update_screen(input_text, on_screen_keyboard)
            term_upd = False
        
        try:
            if on_screen_keyboard == False:
                KB_Data = CardKB.read()
            else:
                input_on_screen = npad.keyboard("Enter command")
                if input_on_screen == None:
                    term_ok = False
                else:
                    update_screen(input_text, True)
                    term_exec.executep(input_on_screen)
                    time.sleep(2)
                    continue
        except:
            on_screen_keyboard = True
        if on_screen_keyboard == False:
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
                    term_exec.executep(input_text)
                    input_text = ""
                # Up
                elif KB_Data == b'\xb5':
                    term_exec.term_up()
                    term_exec.term_render(term_exec.display)          
                # Down
                elif KB_Data == b'\xb6':
                    term_exec.term_down()
                    term_exec.term_render(term_exec.display)
                # FN + Up
                elif KB_Data == b'\x99':
                    term_exec.term_pup()
                    term_exec.term_render(term_exec.display)          
                # FN + Down
                elif KB_Data == b'\xa4':
                    term_exec.term_pdown()
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
    