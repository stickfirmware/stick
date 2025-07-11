file = """
"""
from machine import Pin, PWM
import esp32

def convertLirc(string):
    begun = False
    name = ""
    bits = 0
    pre_data_bits = 0
    pre_data = ""
    flags = ""
    eps = 0
    aeps = 0
    header = []
    one = []
    zero = []
    gap = 0
    min_repeat = 0
    toggle_bit = 0
    
    begun_codes = False
    codes = {}
    
    for line in string.splitlines():
        line = line.strip()

        if not line or line.startswith('#'):
                continue
        
        if line.startswith("begin remote"):
            begun = True
            continue
        if line.startswith("end remote"):
            begun = True
            continue
        
        if line == "begin codes":
            begun_codes = True
            continue
        if line == "end codes":
            begun_codes = False
            continue
        
        if begun_codes == True:
            parts = line.split()
            if len(parts) == 2:
                code_name, code_hex = parts
                codes[code_name] = code_hex
            continue
        
        if ' ' in line:
            key, val = line.split(None, 1)
            
            # Parse for arrays
            if key in ['header', 'one', 'zero']:
                vals = val.split()
                if len(vals) == 2:
                    header_val = [int(vals[0]), int(vals[1])]
                    if key == 'header':
                        header = header_val
                    if key == 'one':
                        one = header_val
                    if key == 'zero':
                       zero = header_val
                continue
            
            # Parse others
            if key == "name":
                name = str(val)
                continue
            if key == "bits":
                bits = int(val)
                continue
            if key == "pre_data_bits":
                pre_data_bits = int(val)
                continue
            if key == "pre_data":
                pre_data = str(val)
                continue
            if key == "flags":
                flags = str(val)
                continue
            if key == "eps":
                eps = int(val)
                continue
            if key == "aeps":
                aeps = int(val)
                continue
            if key == "gap":
                gap = int(val)
                continue
            if key == "min_repeat":
                min_repeat = int(val)
                continue
            if key == "toggle_bit":
                toggle_bit = int(val)
                continue
    return {
        'name': name,
        'bits': bits,
        'flags': flags,
        'eps': eps,
        'aeps': aeps,
        'header': header,
        'one': one,
        'zero': zero,
        'gap': gap,
        'min_repeat': min_repeat,
        'toggle_bit': toggle_bit,
        'codes': codes,
        'pre_data_bits': pre_data_bits,
        'pre_data': pre_data
    }

def convertToTimes(lirc, code):
    target_bits = lirc['bits']
    pre_data_bits = lirc.get('pre_data_bits') or 0
    pre_data = lirc.get('pre_data') or "0x0"
    cd = bin(int(lirc['codes'][code]))[2:]
    pre_data = bin(int(pre_data))[2:]
    
    padding = target_bits - len(cd)
    
    if padding > 0:
        cd = "0" * padding + cd
    else:
        cd = cd[-target_bits:]
    
    out = []
    
    for i in lirc['header']:
        out.append(i * 10)
        
    padding = pre_data_bits - len(pre_data)
    
    if padding > 0:
        pre_data = "0" * padding + pre_data
    else:
        pre_data = pre_data[-pre_data_bits:]
        
    pre_data = pre_data + cd
    for i in pre_data:
        if i == '0':
            for l in lirc['zero']:
                out.append(l * 10)
        if i == '1':
            for l in lirc['one']:
                out.append(l * 10)
                
    return out
    
lirc = convertLirc(file)
print(lirc)
times = convertToTimes(lirc, 'KEY_MUTE')
print(times)

r = esp32.RMT(0, pin=Pin(19), clock_div=8, tx_carrier=(38000, 50, 1))
r.write_pulses(times, True)