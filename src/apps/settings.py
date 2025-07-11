import modules.menus as menus
import modules.nvs as nvs
import modules.openFile as openfile
import modules.uptime as uptime
import fonts.def_8x8 as f8x8
import modules.sdcard as sd
import esp32
import machine
import network
import time
import gc

button_a = None
button_b = None
button_c = None
tft = None
rtc = None

def set_btf(bta, btb, btc, ttft, rtcc):
    global button_a
    global button_b
    global button_c
    global tft
    global rtc
    
    button_a = bta
    button_b = btb
    button_c = btc
    tft = ttft
    rtc = rtcc
    
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
    import bitmaps.floppy as b_floppy
    n_settings = esp32.NVS("settings")
    n_wifi = esp32.NVS("wifi")
    n_boot = esp32.NVS("boot")
    n_crash = esp32.NVS("crash")
    
    work = True
    while work == True:
        menu1 = menus.menu("Settings", [("LCD / st7789", 1), ("Buzzer", 2), ("Wi-Fi", 3), ("SD Card", 7), ("About", 8), ("Close", 13)])
        if menu1 == 1:
            menu2 = menus.menu("Settings/st7789", [("Backlight", 1), ("Autorotate", 2), ("Power saving", 3), ("Close", 13)])
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
            elif menu2 == 2:
                work1 = True
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
        elif menu1 == 2:
            menu2 = menus.menu("Settings/Buzzer", [("Volume", 1), ("Close", 13)])
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
        elif menu1 == 3:
            rendr =  menus.menu("Settings/Wi-Fi", [("Setup Mode", 1), ("Connection", 2), ("NTP Sync", 3), ("NTP Timezone", 4), ("Close", 13)])
            if rendr == 1:
                server = True
                tft.fill(0)
                tft.text(f8x8, "Do you really want",0,0,65535)
                tft.text(f8x8, "to enter Wi-Fi setup?",0,8,65535)
                tft.text(f8x8, "You can exit only with",0,20,65535)
                tft.text(f8x8, "reboot or connecting",0,28,65535)
                tft.text(f8x8, "with Access Point of",0,36,65535)
                tft.text(f8x8, "your M5StickC Plus2!",0,44,65535)
                time.sleep(6)
                men = menus.menu("Enter setup mode?", [("Yes",  1), ("No", 2)])
                if men != 1:
                    server = False
                if server == True:
                    tft.fill(703)
                    tft.text(f8x8, "Wi-Fi setup mode!",0,0,0,703)
                    nic = network.WLAN(network.STA_IF)
                    ap = network.WLAN(network.AP_IF)
                    ap.active(False)
                    nic.disconnect()
                    nic.active(False)
                    time.sleep(0.2)
                    time.sleep(0.3)
                    ap = network.WLAN(network.WLAN.IF_AP)
                    ap.active(True)
                    ap.config(ssid='M5Stick-Config')
                    ap.config(max_clients=1)
                    tft.text(f8x8, "Connect to AP: ",0,8,0,703)
                    tft.text(f8x8, "SSID: M5Stick-Config",0,16,0,703)
                    try:
                        import usocket as socket
                    except:
                        import socket
                
                    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1] # nosec
                    s = socket.socket()
                    s.bind(addr)
                    s.listen(1)
                    tft.text(f8x8, "IP: 192.168.4.1",0,24,0,703)
                    tft.text(f8x8, "Enter it in browser!",0,32,0,703)
                
                    print('Listening on: 192.168.4.1')

                while server == True:
                    conn, addr = s.accept()
                    print('Connected with: ', addr)
                    request = conn.recv(1024).decode('utf-8')
                    request_line = request.split('\n')[0]
                    path = request_line.split(' ')[1]

                    if path.startswith('/config'):
                        if '?' in path:
                            query = path.split('?', 1)[1]
                            params = {}
                            for kv in query.split('&'):
                                k, v = kv.split('=')
                                params[k] = v

                            if 'ssid' in params:
                                nvs.set_float(n_wifi, "conf", 1)
                                nvs.set_int(n_wifi, "autoConnect", params['auto_connect'])
                                nvs.set_string(n_wifi, "ssid", url_decode(params['ssid']))
                                nvs.set_string(n_wifi, "passwd", url_decode(params['password']))
                                ap.active(False)
                                server = False

                        response = 'HTTP/1.1 200 OK\nContent-Type: text/plain\n\nConfig updated!'
        
                    elif path == '/':
                        with open('/html/config.html', 'r') as f:
                            response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n' + f.read()

                    else:
                        response = 'HTTP/1.1 404 Not Found\nContent-Type: text/plain\n\nNot found'

                    conn.sendall(response.encode('utf-8'))
                    conn.close()
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
            elif rendr == 3:
                nic = network.WLAN(network.STA_IF)
                if nic.isconnected() == True:
                    syncing = True
                    while syncing == True:
                        import modules.ntp as ntp
                        syn = ntp.sync(rtc)
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
        elif menu1 == 7:
            if sd.sd is None:
                sd_menu = menus.menu("Settings/SD Card", [("Init", 1), ("Close", 13)])
                if sd_menu == 1:
                    tft.fill(0)
                    tft.bitmap(b_floppy, 5,5)
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
            else:
                sd_menu = menus.menu("Settings/SD Card", [("Unmount", 1), ("Close", 13)])
                if sd_menu == 1:
                    tft.fill(0)
                    tft.bitmap(b_floppy, 5,5)
                    tft.text(f8x8, "Unmount SD...",135,30, 65535)
                    sdin = sd.umount()
                    if sdin == True:
                        tft.text(f8x8, "Done!",135,38, 65535)
                        sd.sd = None
                    else:
                        tft.text(f8x8, "Failed!",135,38, 65535)
                    time.sleep(2)
        elif menu1 == 8:
            import version as v
            tft.fill(0)
            gc.collect()
            memfree = gc.mem_free() / 1024 / 1024
            used = gc.mem_alloc() / 1024 / 1024
            if v.is_beta == True:
                ver_color = 65088
            else:
                ver_color = 65535
            tft.text(f8x8, "Kitki30 Stick version " + str(v.MAJOR) + "." + str(v.MINOR) + "." + str(v.PATCH),0,0,ver_color)
            tft.text(f8x8, "by @Kitki30",0,8,ver_color)
            tft.text(f8x8, "MIT License",0,16,65535)
            tft.text(f8x8, "Free RAM: " + str(round(memfree, 2)) + "MB",0,30,2016)
            tft.text(f8x8, "Used RAM: " + str(round(used, 2)) + "MB",0,38,2016)
            tft.text(f8x8, "Uptime: " + uptime.get_formated(),0,46,2016)
            tft.text(f8x8, "Press button A to exit,",0,119,65535)
            tft.text(f8x8, "button B for credits.",0,127,65535)
            while button_a.value() == 1 and button_b.value() == 1 and button_c.value() == 1:
                time.sleep(0.02)
            if button_b.value() == 0:
                openfile.set_btf(button_a, button_b, button_c, tft)
                openfile.openMenu("/CREDITS")
        else:
            work = False
            
        
    gc.collect()
    machine.freq(80000000)
