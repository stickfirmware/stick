import fonts.def_8x8 as f8x8
import modules.osconstants as osc
import fonts.def_16x32 as f16x32
import modules.menus as menus
import uos
import gc
import array

from time import sleep, ticks_ms, ticks_diff
from machine import Pin, I2S

import modules.io_manager as io_man

button_a = io_man.get_btn_a()
button_b = io_man.get_btn_b()
button_c = io_man.get_btn_c()
tft = io_man.get_tft()

def io_refresh():
    global button_c, button_a, button_b, tft
    button_a = io_man.get_btn_a()
    button_b = io_man.get_btn_b()
    button_c = io_man.get_btn_c()
    tft = io_man.get_tft()

def skeleton(text="Music Player"):
    tft.fill_rect(0, 0, 240, 3, 65535)
    tft.fill_rect(0, 16, 240, 3, 65535)
    tft.fill_rect(0, 132, 240, 3, 65535)
    tft.fill_rect(0, 0, 3, 135, 65535)
    tft.fill_rect(237, 0, 3, 135, 65535)
    tft.fill_rect(3, 3, 234, 13, 0)
    tft.fill_rect(3, 19, 234, 113, 0)
    tft.text(f8x8, text, 5, 5, 65535)

def volume_to_shift(volume):
    if volume <= 0:
        return -8
    elif volume < 0.8:
        return int((volume / 0.8) * 8 - 8)
    else:
        return int((volume - 0.8) / 0.2 * 2)

def play(path):
    io_refresh()
    tft.fill(0)
    tft.text(f8x8, "Loading...", 0, 0, 65535)

    try:
        uos.stat(path)
    except OSError:
        tft.fill(0)
        tft.text(f8x8, "Error: File not found.", 0, 0, 65535)
        sleep(2)
        return

    tft.fill(0)
    skeleton()
    tft.text(f8x8, path.split("/")[-1], 5, 25, 65535)

    audio_out = I2S(
        0,
        sck=Pin(osc.SPEAKER_BCLK),
        ws=Pin(osc.SPEAKER_LRCLK),
        sd=Pin(osc.SPEAKER_SDATA),
        mode=I2S.TX,
        bits=16,
        format=I2S.MONO,
        rate=16000,
        ibuf=4096
    )

    try:
        with open(path, "rb") as f:
            header = f.read(44)
            file_size = uos.stat(path)[6]
            data_length = file_size - 44
            total_seconds = data_length // 32000
            total_minutes = total_seconds // 60
            total_seconds_remain = total_seconds % 60

            current_pos = 0
            last_displayed_time = -1
            MAX_VOLUME = 0.9
            volume = 0.7
            paused = False
            exit_timer_start = None

            DEBOUNCE_MS = 200
            last_a_press = 0
            last_b_press = 0
            last_c_press = 0

            last_volume_display = None
            was_paused = False

            while True:
                now = ticks_ms()

                if button_a.value() == 0:
                    if exit_timer_start is None:
                        exit_timer_start = now
                    elif ticks_diff(now, exit_timer_start) > 1000:
                        break
                else:
                    exit_timer_start = None

                if button_a.value() == 0 and ticks_diff(now, last_a_press) > DEBOUNCE_MS:
                    paused = not paused
                    if paused:
                        was_paused = True
                    last_a_press = now
                    sleep(0.05)

                if button_b.value() == 0:
                    new_vol = max(0.0, volume - 0.1)
                    if new_vol != volume:
                        volume = new_vol
                    sleep(0.05)

                if button_c.value() == 0:
                    new_vol = min(MAX_VOLUME, volume + 0.1)
                    if new_vol != volume:
                        volume = new_vol
                    sleep(0.05)

                if paused:
                    tft.fill_rect(5, 60, 200, 10, 0)
                    tft.text(f8x8, "[PAUSED]", 5, 60, 65535)
                    sleep(0.1)
                    continue

                data = f.read(1024)
                if not data:
                    break

                samples = bytearray(data)
                shift = volume_to_shift(volume)
                I2S.shift(buf=samples, bits=16, shift=shift)
                audio_out.write(samples)
                
                # Display time
                current_pos += len(data)
        
                elapsed_sec = current_pos // 32000
                if elapsed_sec != last_displayed_time:
                    last_displayed_time = elapsed_sec
                    elapsed_min = elapsed_sec // 60
                    elapsed_remain = elapsed_sec % 60

                    timestamp = "{:02}:{:02}/{:02}:{:02}".format(
                        elapsed_min, elapsed_remain,
                        total_minutes, total_seconds_remain
                    )
                    tft.fill_rect(5, 45, 230, 10, 0)
                    tft.text(f8x8, timestamp, 5, 45, 65535)
                
                # Display volume
                if last_volume_display != volume or was_paused:
                    tft.fill_rect(5, 60, 100, 8, 0)
                    fill_width = int(100 * (volume / MAX_VOLUME))
                    if fill_width > 0:
                        tft.fill_rect(5, 60, fill_width, 8, 65535)
                    tft.rect(5, 60, 100, 8, 65535)

                    vol_percent = int((volume / MAX_VOLUME) * 100)
                    if vol_percent > 100:
                        vol_percent = 100

                    vol_text = f"Vol: {vol_percent}%"
                    tft.fill_rect(5 + 100 + 5, 60, 50, 8, 0)
                    tft.text(f8x8, vol_text, 5 + 100 + 5, 60, 65535)

                    last_volume_display = volume
                was_paused = False

    except Exception as e:
        print(f"Error during playback: {e}")
        tft.text(f8x8, "Playback Error!", 5, 45, 65535)
    finally:
        audio_out.deinit()
        gc.collect()

def run():
    io_refresh()
    
    import sys
    if not osc.HAS_SPEAKER:
        menus.menu("You don't have a speaker!", [("OK", 1)])
        return

    work = True
    while work:
        render = menus.menu("Music Player", [("Browse music in explorer", 4), ("Exit", 3)])
        try:
            if render == 4:
                import modules.fileexplorer as a_fe
                browser_path = a_fe.run(True)
                if browser_path is not None:
                    play(browser_path)
                del a_fe
                sys.modules.pop('modules.fileexplorer', None)
            else:
                work = False
        except Exception as e:
            print(f"Oops!\nSomething wrong has happened in Music Player\nLogs:\n{e}")
            tft.fill(0)
            gc.collect()
            tft.text(f16x32, "Oops!", 0, 0, 1984)
            tft.text(f8x8, "Something wrong has happened!", 0, 32, 65535)
            tft.text(f8x8, "Please try again!", 0, 40, 65535)
            sleep(3)
            work = False
