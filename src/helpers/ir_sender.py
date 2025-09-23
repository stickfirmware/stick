from machine import Pin, PWM
import time

import modules.powersaving as ps
import modules.os_constants as osc
import modules.cache as cache
import modules.nvs as nvs
import modules.io_manager as io_man
    
def parse_array(path):
    """
    Parse array from file
    """
    with open(path, "r") as f:
        data_str = f.read().strip()

    data_str = data_str.strip("[]")
    data = [int(x.strip()) for x in data_str.split(",")]
    return data
    
def open_file(path):
    n_settings = cache.get_nvs('settings')
    pin_nvs = nvs.get_int(n_settings, "irPin")
    if pin_nvs is None or pin_nvs not in osc.IR_ALLOWED_PINS:
        nvs.set_int(n_settings, "irPin", osc.IR_PIN)
        pin_nvs = osc.IR_PIN
        
    # Allow clock boosting, doesn't seem to work on 80MHz
    ps.boost_allowing_state(True)
        
    ir_pin = PWM(Pin(pin_nvs), freq=38000, duty_u16=0)
    io_man.set('IR', ir_pin)
    
    # Give time for IR to init so device doesn't pick up any noise
    time.sleep(0.5)
    
    # Send IR
    import modules.IR.recv as recv
    ps.boost_clock()
    recv.send_ir(parse_array(path))
    
    # Disable boosts
    ps.boost_allowing_state(False)
    ps.loop()