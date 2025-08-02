import machine
import time

import modules.os_constants as osc
import modules.io_manager as io_man

if osc.ALLOW_IR_RECORD:
    ir_pin = machine.Pin(osc.IR_RECORD_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

pwm = None

def record_ir(wait_timeout_ms=15000, silence_timeout_ms=3000):
    data = []

    wait_start = time.ticks_ms()
    while ir_pin.value() == 1:
        if time.ticks_diff(time.ticks_ms(), wait_start) > wait_timeout_ms:
            return None

    start = time.ticks_us()
    last_time = start
    last_val = ir_pin.value()
    last_change = time.ticks_ms()

    while True:
        now_us = time.ticks_us()
        now_ms = time.ticks_ms()
        val = ir_pin.value()

        if val != last_val:
            dur = time.ticks_diff(now_us, last_time)
            data.append(dur)
            last_time = now_us
            last_val = val
            last_change = now_ms

        if time.ticks_diff(now_ms, last_change) > silence_timeout_ms:
            break

    return data if data else None


def send_ir(pulses):
    global pwm
    pwm = io_man.get('IR')
    for i, dur in enumerate(pulses):
        if i % 2 == 0:
            pwm.duty_u16(32768)
        else:
            pwm.duty_u16(0)
        time.sleep_us(dur)
    pwm.duty_u16(0)