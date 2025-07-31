import os
import machine
import esp32
import network
import machine
import modules.os_constants as osc
import modules.nvs as nvs
import modules.menus as menus
import modules.io_manager as io_man
import modules.sleep as m_sleep
import fonts.def_8x8 as f8x8

button_a = io_man.get_btn_a()
button_b = io_man.get_btn_b()
button_c = io_man.get_btn_c()
tft = io_man.get_tft()
power_hold = io_man.get_power_hold()
mpu = io_man.get_imu()

def run():
    global button_c, button_a, button_b, tft
    button_a = io_man.get_btn_a()
    button_b = io_man.get_btn_b()
    button_c = io_man.get_btn_c()
    tft = io_man.get_tft()
    
    nic = network.WLAN(network.STA_IF)
    powermenu = menus.menu("Power", [("Sleep", 1), ("Power off", 2), ("Reboot", 3), ("Cancel", 4)])
    n_wifi = esp32.NVS("wifi")
    if powermenu == 1:
        machine.freq(osc.BASE_FREQ)
        wasConnected = False
        if nic.isconnected() == True:
            nic.disconnect()
            wasConnected = True
        nic.active(False)
        os.sync()
        if mpu != None:
            mpu.sleep_on()
        m_sleep.sleep(osc.ENABLE_DEBUG_PRINTS)
        if mpu != None:
            mpu.sleep_off()
        if wasConnected == True:
            nic.active(True)
            nic.connect(nvs.get_string(n_wifi, "ssid"), nvs.get_string(n_wifi, "passwd"))
    elif powermenu == 2:
        machine.freq(osc.BASE_FREQ)
        nic.active(False)
        tft.fill(703)
        tft.text(f8x8, "Powering off...",0,0,65535,703)
        tft.text(f8x8, "Please wait!",0,8,65535,703)
        os.sync()
        if osc.HAS_HOLD_PIN:
            power_hold.value(0)
        m_sleep.sleep(osc.ENABLE_DEBUG_PRINTS)
    elif powermenu == 3:
        machine.freq(osc.BASE_FREQ)
        nic.active(False)
        tft.fill(703)
        tft.text(f8x8, "Rebooting...",0,0,65535,703)
        tft.text(f8x8, "Please wait!",0,8,65535,703)
        os.sync()
        machine.reset()
    else:
        machine.freq(osc.BASE_FREQ)