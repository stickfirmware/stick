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
        current = ps.performance_mode
        if current:
            current = l_get("apps.settings.power.enabled")
        else:
            current = l_get("apps.settings.power.disabled")

        menu3 = menus.menu(
            l_get("apps.settings.power.performance_mode"),
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
            if current == l_get("apps.settings.power.enabled"):
                continue
            bat_voltage = b_check.voltage()
            if bat_voltage <= 3.75:
                popup.show(l_get("apps.settings.power.battery_low_error"),
                           l_get("crashes.error"),
                           15)
            popup.show(l_get("apps.settings.power.usage_info"),
                       l_get("popups.info"),
                       15)
            ps.toggle_performance()
        elif menu3 == 3:
            if current == l_get("apps.settings.power.disabled"):
                ps.toggle_performance()
        else:
            break