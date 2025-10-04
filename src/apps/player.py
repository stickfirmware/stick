import uos
import gc
from time import sleep, ticks_ms, ticks_diff
from machine import Pin, I2S

import fonts.def_8x8 as f8x8

import modules.os_constants as osc
import modules.io_manager as io_man
from modules.translate import get as l_get

button_a = io_man.get('button_a')
button_b = io_man.get('button_b')
button_c = io_man.get('button_c')
tft = None

def io_refresh():
    global button_c, button_a, button_b, tft
    button_a = io_man.get('button_a')
    button_b = io_man.get('button_b')
    button_c = io_man.get('button_c')
    tft = io_man.get('tft')

def skeleton(text=l_get("apps.music_player.name")):
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
    tft.text(f8x8, l_get("apps.music_player.loading"), 0, 0, 65535)

    try:
        uos.stat(path)
    except OSError:
        tft.fill(0)
        tft.text(f8x8, l_get("apps.music_player.file_not_found"), 0, 0, 65535)
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
            header = f.read(44) # noqa: F841
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

                if button_b.value() == 0 and ticks_diff(now, last_b_press) > DEBOUNCE_MS:
                    new_vol = max(0.0, volume - 0.1)
                    if new_vol != volume:
                        volume = new_vol
                    sleep(0.05)

                if button_c.value() == 0 and ticks_diff(now, last_c_press) > DEBOUNCE_MS:
                    new_vol = min(MAX_VOLUME, volume + 0.1)
                    if new_vol != volume:
                        volume = new_vol
                    sleep(0.05)

                if paused:
                    tft.fill_rect(5, 60, 200, 10, 0)
                    tft.text(f8x8, l_get("apps.music_player.paused"), 5, 60, 65535)
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

                    vol_text = f"{l_get("apps.music_player.vol")}: {vol_percent}%   "
                    tft.fill_rect(5 + 100 + 5, 60, 50, 8, 0)
                    tft.text(f8x8, vol_text, 5 + 100 + 5, 60, 65535)

                    last_volume_display = volume
                was_paused = False

    except Exception as e:
        print(f"Error during playback: {e}")
        tft.text(f8x8, l_get("apps.music_player.playback_err"), 5, 45, 65535)
        sleep(1)
    finally:
        audio_out.deinit()
        gc.collect()