import os
import gc
import machine

sd = None
mntpoint = "/sd"

def init(slot=2, sck=40, cs=12, miso=39, mosi=14, freq=10_000_000):
    global sd
    try:
        gc.collect()
        sd = machine.SDCard(slot=slot, sck=sck, cs=cs, miso=miso, mosi=mosi, freq=freq)
        return True
    except Exception as e:
        print(e)
        return False
        
    
def mount(mountpoint=mntpoint):
    try:
        os.sync()
        gc.collect()
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