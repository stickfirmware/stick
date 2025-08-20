import time

import fonts.def_8x8 as f8x8
import fonts.def_16x16 as f16x16

import modules.io_manager as io_man
import modules.powersaving as ps
import modules.os_constants as osc

# Split text into array
def split_text(text, max_len=29, max_lines=13):
    lines = []
    
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + (1 if current_line else 0) <= max_len:
                current_line += (" " if current_line else "") + word
            else:
                if current_line:
                    lines.append(current_line)
                    if len(lines) >= max_lines:
                        return lines
                    current_line = ""
                
                while len(word) > max_len:
                    lines.append(word[:max_len])
                    if len(lines) >= max_lines:
                        return lines
                    word = word[max_len:]
                
                current_line = word
        
        if current_line:
            lines.append(current_line)
            if len(lines) >= max_lines:
                return lines
        
        if paragraph == "":
            lines.append("")
            if len(lines) >= max_lines:
                return lines
    
    return lines


def show(message, title="Info", timeout=3600):
    ps.boost_allowing_state(True)
    
    # Clear / Display title
    tft = io_man.get("tft")
    tft.fill(0)
    tft.text(f16x16, title, 0, 0, 65535)
    
    current_y = 16 # Should be 16 or the height of title font
    msg_font_height = 8 # Height of message font
    msg_font_width = 8 # Width of message font
    
    # NO NEED TO CHANGE, CALCULATES ITSELF
    bottom_padding_height = msg_font_height + 4 # Padding at the bottom for info on closing
    max_y = osc.LCD_HEIGHT - bottom_padding_height # Max pixels, LCD_HEIGHT - bottom padding (For bottom thing with info on closing)
    msg_max_font_lines = (max_y - current_y) // msg_font_height # Max lines of message font that can fit
    line_max_len = (osc.LCD_WIDTH - 4) // msg_font_width # Max lenght of text per line
    any_button_y = osc.LCD_HEIGHT - msg_font_height # Y pos to display close info
    any_button_line_y = osc.LCD_HEIGHT - bottom_padding_height
    
    # Display msg
    for line in split_text(message, max_len=line_max_len, max_lines=msg_max_font_lines):
        tft.text(f8x8, line, 0, current_y, 65535)
        current_y += msg_font_height
        if current_y >= max_y:
            break
        
    tft.fill_rect(0, any_button_line_y, osc.LCD_WIDTH, 3) # Separator
    tft.text(f8x8, "Press any button to close", 0, any_button_y, 65535)
    
    if timeout > 3600:
        timeout = 3600
    elif timeout == 0:
        timeout = 3600
        
    timeout_ms = timeout * 1000 # Convert to ms
    start_time = time.ticks_ms()
    
    import modules.button_combos as button_combos
    
    while time.ticks_diff(time.ticks_ms(), start_time) < timeout_ms and button_combos.any_btn(['a', 'b', 'c']) == False:
        time.sleep(osc.LOOP_WAIT_TIME)
    
    ps.loop()