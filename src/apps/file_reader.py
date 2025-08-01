import gc
import time

import fonts.def_8x8 as f8x8

import modules.os_constants as osc
import modules.io_manager as io_man

def splittext(text):
    CHARLIMIT = 27
    LINELIMIT = 16

    pages = []
    page = []
    
    raw_lines = text.split('\n')
    
    for raw in raw_lines:
        if raw.strip() == "":
            page.append([""])
            if len(page) >= LINELIMIT:
                pages.append(page)
                page = []
            continue
        
        start = 0
        while start < len(raw):
            chunk = raw[start:start+CHARLIMIT]
            page.append([chunk])
            start += CHARLIMIT
            
            if len(page) >= LINELIMIT:
                pages.append(page)
                page = []
    
    if page:
        pages.append(page)

    return pages

def read(filename):
    gc.collect()
    max_bytes=500*1024
    
    try:
        with open(filename, "rb") as f:
            data = f.read(max_bytes)
        text = data.decode("utf-8")
        text = text.replace('\t', '    ')
    except Exception as e:
        return splittext("Error: {str(e)}")
    
    return splittext(text)

def showfile(file):
    button_a = io_man.get_btn_a()
    button_b = io_man.get_btn_b()
    button_c = io_man.get_btn_c()
    tft = io_man.get_tft()
    tft.fill(0)
    tft.text(f8x8, "Loading file preview...",0,8,65535)
    tft.text(f8x8, "Kitki30 Stick File Reader",0,0,65535)
    split = read(file)
    if not split or len(split) == 0:
        split = [[["No content to display"]]]
    current_page = 0
    tft.fill(0)
    tft.fill_rect(220, 0, 20, 135, 65535)
    update = True
    work = True
    while work == True:
        if update:
            index = 0
            tft.fill_rect(0, 0, 220, 135, 0)
            tft.fill_rect(223, 3, 14, 129, 0)
            scrollbar_height = 129
            pages_count = len(split)
            thumb_height = max(10, scrollbar_height // pages_count)
            if pages_count > 1:
                pos = 3 + (current_page * (scrollbar_height - thumb_height)) // (pages_count - 1)
            else:
                pos = 0
            tft.fill_rect(223, pos, 14, thumb_height, 50776)
            for i in split[current_page]:
                tft.text(f8x8, i[0],3,3 + (index * 8),65535)
                index += 1
            update = False
        if button_c.value() == 0:
            while button_c.value() == 0:
                time.sleep(osc.DEBOUNCE_TIME)
            if current_page == 0:
                work = False
            else:
                current_page -= 1
                update = True
        if button_b.value() == 0:
            while button_b.value() == 0:
                time.sleep(osc.DEBOUNCE_TIME)
            if current_page == len(split) - 1:
                current_page = 0
                update = True
            else:
                current_page += 1
                update = True
        if button_a.value() == 0:
            while button_a.value() == 0:
                time.sleep(osc.DEBOUNCE_TIME)
            work = False
        time.sleep(osc.LOOP_WAIT_TIME)