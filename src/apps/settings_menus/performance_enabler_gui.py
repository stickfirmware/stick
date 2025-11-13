"""
Performance mode settings GUI
"""

import time

import modules.popup as popup
import modules.menus as menus
from modules.translate import get as l_get
import modules.powersaving as ps
import modules.battery_check as b_check


def run():
    while True:
        # TODO: Translate this
        current = ps.performance_mode
        if current:
            current = "Enabled"
        else:
            current = "Disabled"

        menu3 = menus.menu(
            l_get("apps.settings.power.pwr_saving_title"),
            [
                (
                    l_get("apps.settings.current")
                    + ": "
                    + current,
                    1,
                ),
                (l_get("menus.enable"), 2),
                (l_get("menus.disable"), 3),
                (l_get("menus.menu_close"), 13),
            ],
        )
        if menu3 == 1:
            time.sleep(0.02)
        elif menu3 == 2:
            if current == "Enabled":
                continue
            bat_voltage = b_check.voltage()
            if bat_voltage <= 3.75:
                popup.show("Battery charge is too low to enable performance mode, please charge your device to enable.",
                           "Info",
                           15)
            popup.show("Performance mode is can use up to 4 times more battery!\nIt will disable automatically after reboot or when battery is low.",
                       "Info",
                       15)
            ps.toggle_performance()
        elif menu3 == 3:
            if current == "Enabled":
                ps.toggle_performance()
        else:
            break