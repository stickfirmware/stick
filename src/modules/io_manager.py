# IO manager

_BUTTON_A = None
_BUTTON_B = None
_BUTTON_C = None
_TFT = None
_IMU = None
_RTC = None
_POWER_HOLD = None
_IR = None

# Set buttons and tft
def set_btn_a(btn):
    global _BUTTON_A
    _BUTTON_A = btn
    return _BUTTON_A

def set_btn_b(btn):
    global _BUTTON_B
    _BUTTON_B = btn
    return _BUTTON_B

def set_btn_c(btn):
    global _BUTTON_C
    _BUTTON_C = btn
    return _BUTTON_C

def set_tft(tft):
    global _TFT
    _TFT = tft
    return _TFT

def set_imu(imu):
    global _IMU
    _IMU = imu
    return _IMU

def set_rtc(rtc):
    global _RTC
    _RTC = rtc
    return _RTC

def set_power_hold(power_hold):
    global _POWER_HOLD
    _POWER_HOLD = power_hold
    return _POWER_HOLD

def set_IR(ir):
    global _IR
    _IR = ir
    return _IR

# Get buttons and tft
def get_btn_a():
    return _BUTTON_A

def get_btn_b():
    return _BUTTON_B

def get_btn_c():
    return _BUTTON_C

def get_tft():
    return _TFT

def get_imu():
    return _IMU

def get_rtc():
    return _RTC

def get_power_hold():
    return _POWER_HOLD

def get_IR():
    return _IR