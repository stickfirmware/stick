"""
Error code checker for Stick firmware
"""

err_db = {
    "1": "TEST_CRASH",
    "2": "BUTTON_GOT_CRUSHED",
    "1001": "RTC_INIT_ERROR",
    "1002": "LCD_INIT_ERROR",
    "2001": "NVS_INIT_ERROR",
    "3001": "WIFI_CONNECT_ERROR",
    "4001": "UNHANDLED_SYS_ERROR"
}

def check_code(code: int | str) -> str:
    """
    Checks error codes

    Args:
        code (int | str): Error code

    Returns:
        str: Human readable error code
    """
    try:
        return err_db[str(code)]
    except KeyError:
        return "UNKNOWN_ERROR"