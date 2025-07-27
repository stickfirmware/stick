import time
import modules.io_manager as io_man

ir_pin = io_man.get_IR()

def set_ir(pin):
    global ir_pin
    ir_pin = pin

def mark(dur):
    ir_pin.freq(38000)
    ir_pin.duty(512) 
    time.sleep_us(dur)

def space(dur):
    ir_pin.duty(0)
    time.sleep_us(dur)

def send_samsung(data):
    # start bit
    mark(4500)
    space(4500)
    
    for i in range(32):
        if (data >> (31 - i)) & 1:
            mark(560)
            space(1690)
        else:
            mark(560)
            space(560)
    
    # stop bit
    mark(560)
    ir_pin.duty(0)

def send_array(codes):
    global ir_pin
    ir_pin = io_man.get_IR()
    for data in codes:
        print("Sending Samsung (Code: " + str(data) + ")")
        send_samsung(data)
        time.sleep(0.11)
