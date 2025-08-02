import time

import modules.io_manager as io_man
import modules.printer as printer

ir_pin = io_man.get('IR')

def set_ir(pin):
    global ir_pin
    ir_pin = pin

def mark(duration):
    ir_pin.freq(37900)
    ir_pin.duty(512)
    time.sleep_us(duration)

def space(duration):
    ir_pin.duty(0)
    time.sleep_us(duration)

def send_panasonic(data, bits=48):
    mark(3456)
    space(1728)
    
    for i in range(bits):
        if (data >> i) & 1:
            mark(864)
            space(864)
        else:
            mark(864)
            space(2592)
    
    ir_pin.duty(0)

def send_array(codes):
    global ir_pin
    ir_pin = io_man.get('IR')
    for data in codes:
        printer.log("Sending Panasonic (Code: " + str(data) + ")")
        send_panasonic(data, 48)
        time.sleep(0.1)
