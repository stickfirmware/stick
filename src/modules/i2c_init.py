import machine

import modules.os_constants as osc
import modules.crash_handler as c_handler
import modules.io_manager as io_man
import modules.printer as debug
import modules.nvs as nvs
import modules.cache as cache

n_settings = cache.get_nvs("settings")
tft = io_man.get('tft')

auto_rotate = cache.get('n_cache_arotate')

def init():
    auto_rotate = nvs.get_int(n_settings, "autorotate")

    try:
        # Init I2C
        i2c = machine.I2C(osc.I2C_SLOT, scl=machine.Pin(osc.I2C_SCL), sda=machine.Pin(osc.I2C_SDA))
    except Exception as e:
        c_handler.crash_screen(tft, 1001, str(e), True, True, 2)
        
    # Init and sync time from rtc
    if osc.HAS_RTC == True:
        import modules.rtc as rtc_bm8536  
        rtc = rtc_bm8536.BM8563(i2c)
        # rtc.set_time((2025, 4, 29, 1, 13, 37, 0, 0))
        dt = rtc.get_time()
        machine.RTC().datetime(dt)
        debug.log(dt)
    else:
        rtc = None
    
    # Init IMU/MPU
    if osc.HAS_IMU == True: 
        from modules.mpu6886 import MPU6886

        mpu = MPU6886(i2c)
        
        # If autorotate is disabled, put IMU to sleep for power saving
        if auto_rotate == 0:
            mpu.sleep_on()
    else:
        mpu = None
        nvs.set_int(n_settings, "autorotate", 0)
        auto_rotate = 0

    return i2c, rtc, mpu