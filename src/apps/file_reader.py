import gc
import time

import fonts.def_8x8 as f8x8

import modules.os_constants as osc
import modules.io_manager as io_man
import modules.powersaving as ps
from modules.translate import get as l_get

def splittext_stream(fileobj, charlimit=27, linelimit=16):
    page = []
    for raw in fileobj:
        try:
            raw = raw.decode("utf-8")
        except Exception:
            yield [[[""]]]
            return

        raw = raw.replace('\t', '    ').rstrip("\r\n")

        if not raw.strip():
            page.append("")
            if len(page) >= linelimit:
                yield page
                page = []
            continue

        for i in range(0, len(raw), charlimit):
            page.append(raw[i:i+charlimit])
            if len(page) >= linelimit:
                yield page
                page = []

    if page:
        yield page


def read(filename):
    gc.collect()
    try:
        with open(filename, "rb") as f:
            return list(splittext_stream(f))
    except Exception as e:
        return [[[l_get("crashes.error") + ": " + str(e)]]]


def showfile(file):
    ps.boost_allowing_state(True)
    button_a = io_man.get('button_a')
    button_b = io_man.get('button_b')
    button_c = io_man.get('button_c')
    tft = io_man.get('tft')
    tft.fill(0)
    tft.text(f8x8, l_get("apps.file_reader.load_preview"),0,0,65535)
    split = read(file)
    if not split or len(split) == 0:
        split = [[[l_get("apps.file_reader.nothing_to_display")]]]
    current_page = 0
    tft.fill(0)
    tft.fill_rect(220, 0, 20, 135, 65535)
    update = True
    work = True
    while work:
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
                tft.text(f8x8, i,3,3 + (index * 8),65535)
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
        ps.boost_allowing_state(False)