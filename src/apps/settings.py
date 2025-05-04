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
    import modules.menus as menus
    import modules.nvs as nvs
    import fonts.def_8x8 as f8x8
    import esp32
    import machine
    import network
    import time
    import gc
    
    n_settings = esp32.NVS("settings")
    n_wifi = esp32.NVS("wifi")
    n_boot = esp32.NVS("boot")
    n_crash = esp32.NVS("crash")
    
    work = True
    while work == True:
        menu1 = menus.menu("Settings", [("LCD / st7789", 1), ("Buzzer", 2), ("Wi-Fi Setup Mode", 3), ("Wi-Fi Connection", 4), ("NTP sync", 5), ("NTP Timezone", 6), ("Close", 13)])
        if menu1 == 1:
            menu2 = menus.menu("Settings/st7789", [("Backlight", 1), ("Close", 13)])
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
            
                addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
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
        elif menu1 == 4:
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
        elif menu1 == 5:
            nic = network.WLAN(network.STA_IF)
            if nic.isconnected() == True:
                import modules.ntp as ntp
                syn = ntp.sync(rtc)
                del ntp
                tft.fill_rect(4, 124, 60, 8, 0)
                if syn == True:
                    menus.menu("NTP Sync successfull!", [("OK",  1)])
                elif syn == False:
                    menus.menu("NTP Sync failed :(", [("OK",  1)])
            else:
                menus.menu("No Wi-Fi connection!", [("OK",  1)])
            time.sleep(1)
        elif menu1 == 6:
            tim = True
            menu = 1
            while tim:
                if menu == 1:
                    timezone = menus.menu("NTP Timezone", [
                        ("UTC+00:00", 0), ("UTC+01:00", 1), ("UTC+02:00", 2), ("UTC+03:00", 3),
                        ("UTC+03:30", 4), ("UTC+04:00", 5), ("UTC+04:30", 6), ("UTC+05:00", 7),
                        ("UTC+05:30", 8), ("UTC+05:45", 9), ("UTC+06:00", 10), ("UTC+06:30", 11),
                        ("Next", 12)
                    ])
                    if timezone == 12:
                        menu = 2
                    elif timezone == None:
                        tim = False
                    else:
                        nvs.set_int(n_settings, "timezoneIndex", timezone)
                        tim = False
                elif menu == 2:
                    timezone = menus.menu("NTP Timezone", [
                        ("Previous", 0), ("UTC+07:00", 1), ("UTC+08:00", 2), ("UTC+08:45", 3),
                        ("UTC+09:00", 4), ("UTC+09:30", 5), ("UTC+10:00", 6), ("UTC+10:30", 7),
                        ("UTC+11:00", 8), ("UTC+12:00", 9), ("UTC+12:45", 10), ("UTC+13:00", 11),
                        ("Next", 12)
                    ])
                    if timezone == 0:
                        menu = 1
                    elif timezone == 12:
                        menu = 3
                    elif timezone == None:
                        tim = False
                    else:
                        nvs.set_int(n_settings, "timezoneIndex", timezone + 13) 
                        tim = False
                elif menu == 3:
                    timezone = menus.menu("NTP Timezone", [
                        ("Previous", 0), ("UTC+14:00", 1), ("UTC-01:00", 2), ("UTC-02:00", 3),
                        ("UTC-03:00", 4), ("UTC-03:30", 5), ("UTC-04:00", 6), ("UTC-05:00", 7),
                        ("UTC-06:00", 8), ("UTC-07:00", 9), ("UTC-08:00", 10), ("UTC-09:00", 11),
                        ("Next", 12)
                    ])
                    if timezone == 0:
                        menu = 2
                    elif timezone == 12:
                        menu = 4
                    elif timezone == None:
                        tim = False
                    else:
                        nvs.set_int(n_settings, "timezoneIndex", timezone + 25)
                        tim = False
                elif menu == 4:
                    timezone = menus.menu("NTP Timezone", [
                        ("Previous", 0), ("UTC-10:00", 1), ("UTC-11:00", 2), ("UTC-12:00", 3)
                    ])
                    if timezone == 0:
                        menu = 3
                    elif timezone == None:
                        tim = False
                    else:
                        nvs.set_int(n_settings, "timezoneIndex", timezone + 37)
                        tim = False
            timezone = menus.menu("Please sync NTP to apply!", [("OK", 1)])

        else:
            work = False
            
        
    gc.collect()
    machine.freq(80000000)
