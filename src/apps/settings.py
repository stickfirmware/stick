import modules.menus as menus
import modules.nvs as nvs
import modules.os_constants as osc
import modules.openFile as openfile
import fonts.def_8x8 as f8x8
import modules.sdcard as sd
import modules.crash_handler as c_handler
import esp32
import machine
import network
import time
import modules.qr_codes as qr
import modules.numpad as keypad
import gc
import modules.io_manager as io_man

button_a = io_man.get_btn_a()
button_b = io_man.get_btn_b()
button_c = io_man.get_btn_c()
tft = io_man.get_tft()

# Refresh io
def load_io():
    global button_c, button_a, button_b, tft
    button_a = io_man.get_btn_a()
    button_b = io_man.get_btn_b()
    button_c = io_man.get_btn_c()
    tft = io_man.get_tft()
    
def url_decode(s):
    res = ''
    i = 0
    while i < len(s):
        if s[i] == '+':
            res += ' '
        elif s[i] == '%' and i + 2 < len(s):
            res += chr(int(s[i+1:i+3], 16))
            i += 2
        else:
            res += s[i]
        i += 1
    return res


def run():
    load_io()
    n_settings = esp32.NVS("settings")
    n_wifi = esp32.NVS("wifi")
    
    work = True
    while work == True:
        
        # Main menu
        menu1 = menus.menu("Settings", [("LCD / st7789", 1), ("Sound", 2), ("Wi-Fi", 3), ("SD Card", 7), ("About", 8), ("Close", 13)])
        
        # LCD / st7789 settings
        if menu1 == 1:
            menu2 = menus.menu("Settings/st7789", [("Backlight", 1), ("Autorotate", 2), ("Power saving", 3), ("Close", 13)])
            
            # Backlight settings
            if menu2 == 1:
                work1 = True
                while work1 == True:
                    menu3 = menus.menu("Settings/st7789/Backlight", [("Current: " + str(round(nvs.get_float(n_settings, "backlight"), 1)), 1), ("+", 2), ("-", 3), ("Close", 13)])
                    if menu3 == 1:
                        time.sleep(0.02)
                    elif menu3 == 2:
                        if round(nvs.get_float(n_settings, "backlight"), 1) != 1.0:
                            nvs.set_float(n_settings, "backlight", (nvs.get_float(n_settings, "backlight") + 0.1))
                    elif menu3 == 3:
                        if round(nvs.get_float(n_settings, "backlight"), 1) >= 0.4:
                            nvs.set_float(n_settings, "backlight", (nvs.get_float(n_settings, "backlight") - 0.1))
                    else:
                        work1 = False
                    tft.set_backlight(nvs.get_float(n_settings, "backlight"))
             
            # Autorotate settings       
            elif menu2 == 2:
                work1 = True
                if osc.HAS_IMU == False:
                    work1 = False
                    menus.menu("No IMU in your device :(", [("OK", 13)])
                while work1 == True:
                    menu3 = menus.menu("Settings/st7789/Autorotate", [("Current: " + str(nvs.get_int(n_settings, "autorotate")), 1), ("Enable", 2), ("Disable", 3), ("Close", 13)])
                    if menu3 == 1:
                        time.sleep(0.02)
                    elif menu3 == 2:
                        nvs.set_int(n_settings, "autorotate", 1)
                    elif menu3 == 3:
                        nvs.set_int(n_settings, "autorotate", 0)
                    else:
                        work1 = False
                        
            # Power saving settings
            elif menu2 == 3:
                work1 = True
                while work1 == True:
                    menu3 = menus.menu("Settings/st7789/Power saving", [("Current: " + str(nvs.get_int(n_settings, "allowsaving")), 1), ("Enable", 2), ("Disable", 3), ("Close", 13)])
                    if menu3 == 1:
                        time.sleep(0.02)
                    elif menu3 == 2:
                        nvs.set_int(n_settings, "allowsaving", 1)
                    elif menu3 == 3:
                        nvs.set_int(n_settings, "allowsaving", 0)
                    else:
                        work1 = False  
                        
        # Sound settings
        elif menu1 == 2:
            menu2 = menus.menu("Settings/Buzzer", [("Volume", 1), ("Close", 13)])
            
            # Volume settings
            if menu2 == 1:
                work1 = True
                while work1 == True:
                    menu3 = menus.menu("Settings/Buzzer/Volume", [("Current: " + str(round(nvs.get_float(n_settings, "volume"), 1)), 1), ("+", 2), ("-", 3), ("Close", 13)])
                    if menu3 == 1:
                        time.sleep(0.02)
                    elif menu3 == 2:
                        if round(nvs.get_float(n_settings, "volume"), 1) != 0.8:
                            nvs.set_float(n_settings, "volume", (nvs.get_float(n_settings, "volume") + 0.1))
                    elif menu3 == 3:
                        if round(nvs.get_float(n_settings, "volume"), 1) != 0.1:
                            nvs.set_float(n_settings, "volume", (nvs.get_float(n_settings, "volume") - 0.1))
                    else:
                        work1 = False
                        
        # Wi-Fi settings
        elif menu1 == 3:
            rendr =  menus.menu("Settings/Wi-Fi", [("Setup AP", 1), ("Connection", 2), ("NTP Sync", 3), ("NTP Timezone", 4), ("Close", 13)])
            
            # Wi-Fi AP setup
            if rendr == 1:
                ssid = keypad.keyboard("Enter SSID", maxlen=32, hideInput=False)
                if ssid == None:
                    continue
                password = keypad.keyboard("Enter password", maxlen=63, hideInput=False)
                if password == None:
                    continue
                nvs.set_float(n_wifi, "conf", 1)
                nvs.set_int(n_wifi, "autoConnect", 1)
                nvs.set_string(n_wifi, "ssid", ssid)
                nvs.set_string(n_wifi, "passwd", password)
                menus.menu("Now you can connect!", [("OK",  1)])
                
            # Wi-Fi connection
            elif rendr == 2:
                if int(nvs.get_float(n_wifi, "conf")) == 1:
                    try:
                        nic = network.WLAN(network.STA_IF)
                        if nic.isconnected() == False:
                            rend = menus.menu("Connect with " + nvs.get_string(n_wifi, "ssid") + "?", [("Yes",  1), ("No",  2)])
                            if rend == 1:
                                nic.active(False)
                                time.sleep(0.2)
                                nic.active(True)
                                print("Wifi connecting")
                                nic.connect(nvs.get_string(n_wifi, "ssid"), nvs.get_string(n_wifi, "passwd"))
                                menus.menu("Please wait for connection!", [("OK",  1)])
                        else:
                            rend = menus.menu("Wi-Fi connected, diconnect?", [("Yes",  1), ("No",  2)])
                            if rend == 1:
                                nic.disconnect()
                    except Exception as e:
                        c_handler.crash_screen(tft, 3001, str(e), True, True, 2)
                else:
                    menus.menu("Wi-Fi not set-up yet!", [("OK",  1)])
                    
            # NTP Sync
            elif rendr == 3:
                nic = network.WLAN(network.STA_IF)
                if nic.isconnected() == True:
                    syncing = True
                    while syncing == True:
                        import modules.ntp as ntp
                        syn = ntp.sync()
                        del ntp
                        if syn == True:
                            menus.menu("NTP Sync successfull!", [("OK",  1)])
                            syncing = False
                        elif syn == False:
                            rend = menus.menu("NTP Sync failed :(", [("Retry?",  1), ("OK",  2)])
                            if rend == 2:
                                syncing = False
                else:
                    menus.menu("No Wi-Fi connection!", [("OK",  1)])
                    
            # NTP Timezone
            elif rendr == 4:
                tim = True
                menu = 1
                while tim:
                    if menu == 1:
                        timezone = menus.menu("NTP Timezone", [
                            ("UTC+00:00", 0), ("UTC+01:00", 1), ("UTC+02:00", 2), ("UTC+03:00", 3),
                            ("UTC+03:30", 4), ("UTC+04:00", 5), ("UTC+04:30", 6), ("UTC+05:00", 7),
                            ("UTC+05:30", 8), ("UTC+05:45", 9), ("UTC+06:00", 10), ("UTC+06:30", 11),
                            ("UTC+07:00", 12), ("UTC+08:00", 13), ("UTC+08:45", 14),
                            ("UTC+09:00", 15), ("UTC+09:30", 16), ("UTC+10:00", 17), ("UTC+10:30", 18),
                            ("UTC+11:00", 19), ("UTC+12:00", 20), ("UTC+12:45", 21), ("UTC+13:00", 22),
                            ("UTC+14:00", 23), ("UTC-01:00", 24), ("UTC-02:00", 25),
                            ("UTC-03:00", 26), ("UTC-03:30", 27), ("UTC-04:00", 28), ("UTC-05:00", 29),
                            ("UTC-06:00", 30), ("UTC-07:00", 31), ("UTC-08:00", 32), ("UTC-09:00", 33),
                            ("UTC-10:00", 34), ("UTC-11:00", 35), ("UTC-12:00", 36)
                        ])
                        if timezone == None:
                            tim = False
                        else:
                            nvs.set_int(n_settings, "timezoneIndex", timezone)
                            tim = False
                timezone = menus.menu("Please sync NTP to apply!", [("OK", 1)])
                
        # SD Card settings
        elif menu1 == 7:
            
            # SD Card menu if SD is not mounted
            if sd.sd is None:
                sd_menu = menus.menu("Settings/SD Card", [("Init", 1), ("Close", 13)])
                if sd_menu == 1:
                    tft.fill(0)
                    tft.text(f8x8, "Init SD...",135,30, 65535)
                    sdin = sd.init()
                    time.sleep(2)
                    if sdin == True:
                        if sd.mount() == True:
                            tft.text(f8x8, "Done!",135,38, 65535)
                        else:
                            tft.text(f8x8, "Failed!",135,38, 65535)
                    else:
                        tft.text(f8x8, "Failed!",135,38, 65535)
                    time.sleep(2)
                    
            # Menu if SD is mounted
            else:
                sd_menu = menus.menu("Settings/SD Card", [("Unmount", 1), ("Close", 13)])
                if sd_menu == 1:
                    tft.fill(0)
                    tft.text(f8x8, "Unmount SD...",135,30, 65535)
                    sdin = sd.umount()
                    if sdin == True:
                        tft.text(f8x8, "Done!",135,38, 65535)
                        sd.sd = None
                    else:
                        tft.text(f8x8, "Failed!",135,38, 65535)
                    time.sleep(2)
        
        # About screen
        elif menu1 == 8:
            import version as v
            tft.fill(0)
            gc.collect()
            if v.is_beta == True:
                ver_color = 65088
            else:
                ver_color = 65535
            tft.text(f8x8, "Kitki30 Stick version " + str(v.MAJOR) + "." + str(v.MINOR) + "." + str(v.PATCH),0,0,ver_color)
            tft.text(f8x8, "by @Kitki30",0,8,ver_color)
            tft.text(f8x8, "MIT License",0,16,65535)
            tft.text(f8x8, "For more details, scan the QR",0,30,2016)
            qr.make_qr(tft, "https://github.com/stickfirmware/stick", 0, 38, size=2)
            tft.text(f8x8, "Press button A to exit,",0,111,65535)
            tft.text(f8x8, "button B for credits",0,119,65535)
            tft.text(f8x8, "and button C for license.",0,127,65535)
            while button_a.value() == 1 and button_b.value() == 1 and button_c.value() == 1:
                time.sleep(osc.DEBOUNCE_TIME)
            if button_b.value() == 0:
                openfile.openMenu("/CREDITS")
            if button_c.value() == 0:
                openfile.openMenu("/LICENSE")
        else:
            work = False
            
        
    gc.collect()
    machine.freq(osc.BASE_FREQ)
