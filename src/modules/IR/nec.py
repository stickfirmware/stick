import machine
import time

pwm = None

def set_ir(ir):
    global pwm
    pwm = ir
    

def ir_on():
    pwm.freq(38000)
    pwm.duty_u16(32768)

def ir_off():
    pwm.duty_u16(0)

def send_nec(address, command):
    ir_on()
    time.sleep_us(9000)
    ir_off()
    time.sleep_us(4500)

    for i in range(16):
        if (address >> (15 - i)) & 1:
            ir_on()
            time.sleep_us(560)
            ir_off()
            time.sleep_us(1690)
        else:
            ir_on()
            time.sleep_us(560)
            ir_off()
            time.sleep_us(560)

    for i in range(16):
        if (command >> (15 - i)) & 1:
            ir_on()
            time.sleep_us(560)
            ir_off()
            time.sleep_us(1690)
        else:
            ir_on()
            time.sleep_us(560)
            ir_off()
            time.sleep_us(560)

    ir_on()
    time.sleep_us(560)
    ir_off()

def send_array(codes):
    for address, command in codes:
        print("Sending NEC (Addr: "+ str(address) + " Cmd: " + str(command) + ")")
        send_nec(address, command)
        time.sleep(0.12)
