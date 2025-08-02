import time
import modules.io_manager as io_man

pwm = io_man.get('IR')

def ir_on(): pwm.duty_u16(32768)
def ir_off(): pwm.duty_u16(0)

def convert(code):
    if not code or code.strip() == "":
        return []
    parts = code.strip().split()[4:]
    durations = [int(x, 16) * 26 for x in parts]
    return durations


def send_ir(durations):
    if not durations:
        return
    for i, dur in enumerate(durations):
        if i % 2 == 0: ir_on()
        else: ir_off()
        time.sleep_us(dur)
    ir_off()

def send_array(codes):
    for cmd in codes:
        durations = convert(cmd)
        send_ir(durations)
        time.sleep(0.12) 

