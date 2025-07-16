def check_code(code):
    # Testing code
    if code == 1:
        return "TEST_CRASH"
    # External I2C RTC error
    elif code == 1001:
        return "RTC_INIT_ERROR"
    # LCD / TFT init error
    elif code == 1002:
        return "LCD_INIT_ERROR"
    # NVS init error
    elif code == 2001:
        return "NVS_INIT_ERROR"
    # Wi-Fi error
    elif code == 3001:
        return "WIFI_CONNECT_ERROR"
    # Supervisor timeout
    elif code == 4001:
        return "SUPERVISOR_TIMEOUT"
    else:
        return "UNKNOWN"