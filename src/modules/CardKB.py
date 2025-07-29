from machine import I2C, Pin
import time
import modules.os_constants as osc

i2c = None
did_init = False

CARDKB_ADDR = 0x5F

def init():
    global i2c
    try:
        i2c = I2C(osc.GROVE_SLOT, scl=Pin(osc.GROVE_WHITE), sda=Pin(osc.GROVE_YELLOW), freq=100000)
        did_init = True
        return did_init
    except:
        did_init = False
        return did_init

def read():
    data = i2c.readfrom(CARDKB_ADDR, 1)
    return data

def decode(data):
    try:
        return data.decode('utf-8')
    except:
        return None