from machine import I2C, Pin

import modules.menus as menus
import modules.os_constants as osc
import modules.popup as popup


def run():
    if osc.HAS_GROVE:
        i2c = I2C(osc.GROVE_SLOT, scl=Pin(osc.GROVE_WHITE), sda=Pin(osc.GROVE_YELLOW), freq=100000)
        scan = i2c.scan()
        menu = []
        for i in scan:
            menu.append((hex(i), None))
        menu.append(("Close", None))
        menus.menu("I2C Scanner", menu)
    else:
        popup.show("No grove slot in your device.", "Error", 10)