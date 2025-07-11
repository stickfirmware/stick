import os
import machine
import time

sd = None
mntpoint = "/sd"

def init(slot=2, sck=26, cs=None, miso=36, mosi=0, freq=10000000):
    global sd
    try:
        sd = machine.SDCard(slot=slot, sck=sck, cs=cs, miso=miso, mosi=mosi, freq=freq)
        return True
    except Exception as e:
        print(e)
        return False
        
    
def mount(mountpoint=mntpoint):
    try:
        os.sync()
        vfs=os.VfsFat(sd)
        os.mount(vfs, mountpoint)
        return True
    except Exception as e:
        print(e)
        return False
    
def umount(mountpoint=mntpoint):
    global sd
    try:
        os.sync()
        os.umount(mountpoint)
        return True
    except Exception as e:
        print(e)
        return False