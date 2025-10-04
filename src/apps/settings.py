import machine
import network
import time
import gc

import fonts.def_8x8 as f8x8

import modules.printer as printer
import modules.menus as menus
import modules.nvs as nvs
import modules.os_constants as osc
import modules.open_file as open_file
import modules.crash_handler as c_handler
import modules.io_manager as io_man
import modules.wifi_master as wifi_man
import modules.powersaving as ps
import modules.cache as cache
import modules.ntp as ntp
import modules.popup as popup
import modules.translate as translate
from modules.translate import get as l_get

printer.log("Getting buttons")
button_a = io_man.get('button_a')
button_b = io_man.get('button_b')
button_c = io_man.get('button_c')
tft = None

# Refresh io
def _LOAD_IO():
    global button_c, button_a, button_b, tft
    button_a = io_man.get('button_a')
    button_b = io_man.get('button_b')
    button_c = io_man.get('button_c')
    tft = io_man.get('tft')

def run():
    _LOAD_IO()
    n_settings = cache.get_nvs('settings')
    n_updates = cache.get_nvs('updates')
    n_wifi = cache.get_nvs('wifi')
    
    work = True
    while work:
        # Main menu
        menu1 = menus.menu(l_get("apps.settings.name"),
                           [(l_get("apps.clock.name"), 0),
                            (l_get("apps.settings.menu1.lcd"), 1),
                            (l_get("apps.settings.menu1.neopixel"), 5),
                            (l_get("apps.settings.menu1.sound"), 2),
                            (l_get("apps.settings.menu1.wifi"), 3),
                            (l_get("apps.settings.menu1.sdcard"), 7),
                            (l_get("apps.settings.menu1.language"), 11),
                            (l_get("apps.settings.menu1.about"), 8),
                            (l_get("apps.settings.menu1.factory"), 9),
                            (l_get("apps.settings.menu1.show_guides_again"), 12),
                            (l_get("menus.menu_close"), None)]) # ("Account", 10),
        
        # Account settings
        if menu1 == 10:
            import modules.account_manager as account_manager
            menu2 = menus.menu(l_get("apps.settings.acc_menu.title"),
                               [(l_get("apps.settings.acc_menu.link"), 1),
                                (l_get("menus.menu_close"), None)])
            if menu2 == 1:
                account_manager.link()
                
        # Show guides again
        elif menu1 == 12:
            n_guides = cache.get_nvs("guides")
            nvs.set_int(n_guides, 'quick_start', 0)
            nvs.set_int(n_guides, 'account_popup', 0)
            popup.show(l_get("apps.settings.guides.reboot_notify"), l_get("popups.info"))
            
        # Clock
        elif menu1 == 0:
            # TODO: Add clock manual date setting
            clock_menu = menus.menu(l_get("apps.clock.name"), [
                (l_get("apps.clock.ntp_sync"), 0),
                (l_get("apps.settings.wifi.timezone"), 1),
                (l_get("menus.menu_close"), None)
            ])
            
            # NTP Sync
            if clock_menu == 0:
                ntp.sync_interactive()
                    
            # NTP Timezone
            elif clock_menu == 1:
                tim = True
                menu = 1
                while tim:
                    if menu == 1:
                        timezone = menus.menu(l_get("apps.settings.wifi.timezone"), [
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
                        if timezone is None:
                            tim = False
                        else:
                            nvs.set_int(n_settings, "timezoneIndex", timezone)
                            tim = False
                ntp.get_time_timezoned(True)
                
        # Langs
        elif menu1 == 11:
            lang_old = nvs.get_string(n_settings, "lang")
            translations = []
            for i in translate.main_file["langs"]:
                translations.append((translate.main_file[i]["name"], i))
            translations.append((l_get("menus.menu_close"), None))
            ts_menu = menus.menu(l_get("apps.settings.lang_menu.title"), translations)
            if ts_menu is not None:
                if translate.load(ts_menu):
                    import version
                    if l_get("lang_info.version")[0] < version.LANG_VER[0] or l_get("lang_info.version")[1] < version.LANG_VER[1]:
                        popup.show("The language pack is older than system pack version and can not work properly. Expect errors", "Info", 60)
                    nvs.set_string(n_settings, "lang", ts_menu)
                    reboot_confirm = menus.menu(l_get("apps.settings.lang_menu.reboot"),
                                                [(l_get("menus.yes"), 1),
                                                 (l_get("menus.no"), None)])
                    if reboot_confirm == 1: 
                        machine.soft_reset()
                else:
                    popup.show("Translation loading error.", "Error", 10)
                    translate.load(lang_old)
            
        # LCD / st7789 settings
        elif menu1 == 1:
            menu2 = menus.menu(l_get("apps.settings.lcd_menu.title"),
                               [(l_get("apps.settings.lcd_menu.backlight"), 1),
                                (l_get("apps.settings.lcd_menu.autorotate"), 2),
                                (l_get("apps.settings.lcd_menu.pwr_save"), 3),
                                (l_get("menus.menu_close"), 13)])
            
            # Backlight settings
            if menu2 == 1:
                work1 = True
                while work1:
                    menu3 = menus.menu(l_get("apps.settings.lcd_menu.backlight_title"),
                                       [(l_get("apps.settings.current") + ": " + str(round(nvs.get_float(n_settings, "backlight"), 1)), 1),
                                        ("+", 2),
                                        ("-", 3),
                                        (l_get("menus.menu_close"), 13)])
                    if menu3 == 1:
                        time.sleep(0.02)
                    elif menu3 == 2:
                        if round(nvs.get_float(n_settings, "backlight"), 1) != 1.0:
                            nvs.set_float(n_settings, "backlight", (nvs.get_float(n_settings, "backlight") + 0.1))
                    elif menu3 == 3:
                        if round(nvs.get_float(n_settings, "backlight"), 1) > osc.LCD_MIN_BL:
                            nvs.set_float(n_settings, "backlight", (nvs.get_float(n_settings, "backlight") - 0.1))
                    else:
                        work1 = False
                    tft.set_backlight(nvs.get_float(n_settings, "backlight"))
             
            # Autorotate settings       
            elif menu2 == 2:
                work1 = True
                if not osc.HAS_IMU:
                    work1 = False
                    popup.show(l_get("apps.settings.lcd_menu.imu_error_popup"), l_get("crashes.error"), 10)
                while work1:
                    menu3 = menus.menu(l_get("apps.settings.lcd_menu.autorotate_title"),
                                       [(l_get("apps.settings.current") + ": " + str(nvs.get_int(n_settings, "autorotate")), 1),
                                        (l_get("menus.enable"), 2),
                                        (l_get("menus.disable"), 3), 
                                        (l_get("menus.menu_close"), 13)])
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
                while work1:
                    menu3 = menus.menu(l_get("apps.settings.lcd_menu.power_saver_title"),
                                       [(l_get("apps.settings.current") + ": " + str(nvs.get_int(n_settings, "allowsaving")), 1),
                                        (l_get("menus.enable"), 2),
                                        (l_get("menus.disable"), 3), 
                                        (l_get("menus.menu_close"), 13)])
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
            menu2 = menus.menu(l_get("apps.settings.buzzer_menu.buzzer_title"),
                               [(l_get("apps.settings.buzzer_menu.volume"), 1), 
                                (l_get("menus.menu_close"), 13)])
            
            # Volume settings
            if menu2 == 1:
                work1 = True
                while work1:
                    menu3 = menus.menu(l_get("apps.settings.buzzer_menu.volume_title"),
                                       [(l_get("apps.settings.current") + ": " + str(round(nvs.get_float(n_settings, "volume"), 1)), 1),
                                        ("+", 2),
                                        ("-", 3),
                                        (l_get("menus.menu_close"), 13)])
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
        
        # Neopixel settings
        elif menu1 == 5:
            if not osc.HAS_NEOPIXEL:
                popup.show(l_get("apps.settings.neopixel.no_neo_popup"), l_get("popups.info"))
                continue
            
            import modules.neopixel_anims as np_anims
            
            np_menu =  menus.menu(l_get("apps.settings.neopixel.title"),
                                  [(l_get("apps.settings.neopixel.enable"), 0), 
                                  (l_get("apps.settings.neopixel.anim_style"), 1),
                                  (l_get("apps.settings.neopixel.notice_menu"), 2),
                                    (l_get("menus.menu_close"), None)])
            if np_menu == 0:
                enable = menus.menu(l_get("apps.settings.neopixel.enable_ask"),
                                    [(l_get("menus.yes"), 1),
                                     (l_get("menus.no"), 0)])
                if enable is not None:
                    nvs.set_int(n_settings, 'neo_enabled', enable)
                    
            elif np_menu == 1:
                anim_style_selector = menus.menu(l_get("apps.settings.neopixel.anim_style"), 
                                                 [(l_get("apps.settings.neopixel.static"), 1),
                                                  (l_get("apps.settings.neopixel.rainbow"), 2),
                                                  (l_get("menus.menu_close"), None)])
                if anim_style_selector == 1:
                    nvs.set_int(n_settings, "neo_anim_style", 1)
                    color_change_ask = menus.menu(l_get("apps.settings.neopixel.also_change_colors"),
                                                  [(l_get("menus.yes"), 1),
                                                   (l_get("menus.no"), None)])
                    if color_change_ask == 1:
                        import modules.numpad as keypad
                        r = keypad.numpad("R color, 0-255", 3)
                        g = keypad.numpad("G color, 0-255", 3)
                        b = keypad.numpad("B color, 0-255", 3)
                        if r > 255:
                            r = 255
                        if g > 255:
                            g = 255
                        if b > 255:
                            b = 255
                        nvs.set_int(n_settings, "neo_R", r)
                        nvs.set_int(n_settings, "neo_G", g)
                        nvs.set_int(n_settings, "neo_B", b)
                    
                elif anim_style_selector == 2:
                    nvs.set_int(n_settings, "neo_anim_style", 2)
            
            elif np_menu == 2:
                popup.show(
                    l_get("apps.settings.neopixel.notice").replace("%backlight", str(osc.NEOPIXEL_BACKLIGHT_THRESHOLD)).replace("%ledtype", str(osc.NEOPIXEL_TYPE)),
                    l_get("apps.settings.neopixel.notice_menu"))
                    
            np_anims.refresh_counters()
                    
        # Wi-Fi settings
        elif menu1 == 3:
            rendr =  menus.menu(l_get("apps.settings.wifi.title"), 
                                [(l_get("apps.settings.wifi.setup_ap"), 1),
                                 (l_get("apps.settings.wifi.connection"), 2),
                                 (l_get("apps.settings.wifi.status"), 5),
                                 (l_get("menus.menu_close"), 13)])
            
            # Wi-Fi AP setup
            if rendr == 1:
                tft.text(f8x8, l_get("apps.settings.wifi.scanning"), 0,0, 65535)
                nic = network.WLAN(network.STA_IF)
                wifi_man.nic_reset()
                #wifi_man.set_pwr_modes(0)
                nic_scan = nic.scan()
                if nic_scan == []:
                    attempts = 5
                    while attempts != 0 and nic_scan == []:
                        nic_scan = nic.scan()
                        wifi_man.nic_reset()
                        attempts -= 1
                    if nic_scan == []:
                        popup.show(l_get("apps.settings.wifi.no_ap_error_popup"), l_get("crashes.error"), 10)
                        continue
                wlan_scan = []
                index = 0
                for ap in nic_scan:
                    ap_name = ap[0].decode()
                    if ap_name != '' and ap_name is not None and not ap[5]:
                        wlan_scan.append((ap_name, index))
                    index += 1
                wlan_scan.append((l_get("menus.menu_close"), None))
                num = menus.menu(l_get("apps.settings.wifi.select_ssid"), wlan_scan)
                if num is None:
                    continue
                ssid = nic_scan[num][0].decode()
                if nic_scan[num][4] != 0:
                    import modules.numpad as keypad
                    password = str(keypad.keyboard(l_get("apps.settings.wifi.enter_passwd"), maxlen=63, hideInput=False))
                    if password is None:
                        continue
                else:
                    password = ""
                autoconnect = menus.menu(l_get("apps.settings.wifi.auto_connect_ask"),
                                         [(l_get("menus.yes"), 1),
                                          (l_get("menus.no"), 0)])
                if autoconnect is None:
                    autoconnect = 0
                tft.fill(0)
                tft.text(f8x8, l_get("apps.settings.wifi.connecting"), 0,0, 65535)
                tft.text(f8x8, ssid, 0,8, 65535)
                #wifi_man.set_pwr_modes()
                printer.log("Wifi connecting")
                if password != "":
                    nic.connect(ssid, password)
                else:
                    nic.connect(ssid)

                start_time = time.ticks_ms()
                while not nic.isconnected() and time.ticks_diff(time.ticks_ms(), start_time) < 10000:
                    time.sleep(0.2)

                if nic.isconnected():
                    nvs.set_float(n_wifi, "conf", 1.0)
                    nvs.set_int(n_wifi, "autoConnect", autoconnect)
                    nvs.set_string(n_wifi, "ssid", ssid)
                    nvs.set_string(n_wifi, "passwd", password)
                    popup.show(l_get("apps.settings.wifi.connected_to") + ": " + ssid, "Info", 10)
                elif nic.status() == network.STAT_WRONG_PASSWORD:
                    popup.show(l_get("apps.settings.wifi.wrong_passwd"), l_get("crashes.error"), 10)
                elif nic.status() == network.STAT_NO_AP_FOUND:
                    popup.show(l_get("apps.settings.wifi.ap_not_found"), l_get("crashes.error"), 10)
                else:
                    popup.show(l_get("apps.settings.wifi.could_not_conn_popup"), l_get("crashes.error"), 10)
                
            # Wi-Fi connection
            elif rendr == 2:
                if int(nvs.get_float(n_wifi, "conf")) == 1.0:
                    try:
                        nic = wifi_man.nic
                        if not nic.isconnected():
                            rend = menus.menu(l_get("apps.settings.wifi.connect_with") + nvs.get_string(n_wifi, "ssid") + "?", 
                                              [(l_get("menus.yes"),  1),
                                               (l_get("menus.no"),  2)])
                            if rend == 1:
                                ssid = nvs.set_string(n_wifi, "ssid")
                                password = nvs.set_string(n_wifi, "passwd")
                                                                
                                wifi_man.nic_reset()
                                #wifi_man.set_pwr_modes(0)
                                tft.fill(0)
                                tft.text(f8x8, l_get("apps.settings.wifi.connecting"), 0,0, 65535)
                                tft.text(f8x8, ssid, 0,8, 65535)
                                
                                printer.log("Wifi connecting")
                                if password != "":
                                    nic.connect(ssid, password)
                                else:
                                    nic.connect(ssid)

                                start_time = time.ticks_ms()
                                while not nic.isconnected() and time.ticks_diff(time.ticks_ms(), start_time) < 10000:
                                    time.sleep(0.2)

                                if nic.isconnected():
                                    popup.show(l_get("apps.settings.wifi.connected_to") + ": " + ssid, "Info", 10)
                                elif nic.status() == network.STAT_WRONG_PASSWORD:
                                    popup.show(l_get("apps.settings.wifi.wrong_passwd"), l_get("crashes.error"), 10)
                                elif nic.status() == network.STAT_NO_AP_FOUND:
                                    popup.show(l_get("apps.settings.wifi.ap_not_found"), l_get("crashes.error"), 10)
                                else:
                                    popup.show(l_get("apps.settings.wifi.could_not_conn_popup"), l_get("crashes.error"), 10)
                        else:
                            rend = menus.menu(l_get("apps.settings.wifi.connected_disconnect"),
                                              [(l_get("menus.yes"),  1),
                                               (l_get("menus.no"),  2)])
                            if rend == 1:
                                nic.disconnect()
                    except Exception as e:
                        c_handler.crash_screen(tft, 3001, str(e), True, True, 2)
                else:
                    popup.show(l_get("apps.settings.wifi.not_setup"), l_get("crashes.error"), 10)

            # Wi-Fi status
            elif rendr == 5:
                nic = network.WLAN(network.STA_IF)
                nic_active = nic.active()
                nic_ifconfig = nic.ifconfig()
                tft.fill(0)
                tft.text(f8x8, l_get("apps.settings.wifi.wlan_active") + str(nic_active),0,0, 65535)
                tft.text(f8x8, l_get("apps.settings.wifi.connected") + str(nic.isconnected()),0,8, 65535)
                if nic.isconnected():
                    tft.text(f8x8, l_get("apps.settings.local_ip") + str(nic_ifconfig[0]),0,16, 65535)
                    tft.text(f8x8, l_get("apps.settings.wifi.subnet") + str(nic_ifconfig[1]),0,24, 65535)
                    tft.text(f8x8, l_get("apps.settings.wifi.gateway") + str(nic_ifconfig[2]),0,32, 65535)
                    tft.text(f8x8, l_get("apps.settings.wifi.dns") + str(nic_ifconfig[3]),0,40, 65535)
                    tft.text(f8x8, l_get("apps.settings.wifi.ssid") + nic.config('ssid'),0,48, 65535)
                    tft.text(f8x8, l_get("apps.settings.wifi.channel") + str(nic.config('channel')),0,56, 65535)
                    tft.text(f8x8, l_get("apps.settings.wifi.hostname") + network.hostname(),0,64, 65535)
                while button_a.value() == 1 and button_b.value() == 1 and button_c.value() == 1:
                    time.sleep(osc.DEBOUNCE_TIME)
                
        # SD Card settings
        elif menu1 == 7:
            
            # SD Slot check
            if not osc.HAS_SD_SLOT or nvs.get_int(n_settings, "sd_overwrite") == 1:
                popup.show(l_get("apps.settings.sd.no_slot_detected_popup"), l_get("crashes.error"), 10)
                continue
            
            import modules.sdcard as sd
            
            # SD Card menu if SD is not mounted
            if sd.sd is None:
                sd_menu = menus.menu(l_get("apps.settings.sd.title"),
                                     [(l_get("apps.settings.sd.init"), 1),
                                      (l_get("menus.menu_close"), 13)])
                if sd_menu == 1:
                    tft.fill(0)
                    tft.text(f8x8, l_get("apps.settings.sd.init_load"),0,0, 65535)
                    if nvs.get_int(n_settings, "sd_overwrite") == 1 and nvs.get_int(n_settings, "sd_automount") == 1:
                        cs = nvs.get_int(n_settings, "sd_cs")
                        if cs == 99:
                            cs = None
                        sdin = sd.init(2, nvs.get_int(n_settings, "sd_clk"), cs, nvs.get_int(n_settings, "sd_miso"), nvs.get_int(n_settings, "sd_mosi"))
                    else:
                        sdin = sd.init(2, osc.SD_CLK, osc.SD_CS, osc.SD_MISO, osc.SD_MOSI)
                    time.sleep(2)
                    if sdin:
                        if sd.mount():
                            tft.text(f8x8, l_get("apps.settings.sd.done"),0,8, 65535)
                        else:
                            tft.text(f8x8, l_get("apps.settings.sd.failed"),0,8, 65535)
                    else:
                        tft.text(f8x8, l_get("apps.settings.sd.failed"),0,8, 65535)
                    time.sleep(2)
                    
            # Menu if SD is mounted
            else:
                sd_menu = menus.menu(l_get("apps.settings.sd.title"),
                                     [(l_get("apps.settings.sd.unmount"), 1),
                                      (l_get("menus.menu_close"), 13)])
                if sd_menu == 1:
                    tft.fill(0)
                    tft.text(f8x8, l_get("apps.settings.sd.unmount_load"),0,0, 65535)
                    sdin = sd.umount()
                    if sdin:
                        tft.text(f8x8, l_get("apps.settings.sd.done"),0,8, 65535)
                        sd.sd = None
                    else:
                        tft.text(f8x8, l_get("apps.settings.sd.failed"),0,8, 65535)
                    time.sleep(2)
        
        # About screen
        elif menu1 == 8:
            while True:
                about_menu = menus.menu(l_get("apps.settings.menu1.about"), [
                    (l_get("apps.settings.about.firmware_info"), 1),
                    (l_get("apps.settings.about.hardware_info"), 2),
                    (l_get("menus.menu_exit"), None)
                ])
                
                if about_menu == 1:
                    tft.fill(0)
                    gc.collect()
                    if cache.get("ver_isbeta"):
                        ver_color = 65088
                    else:
                        ver_color = 65535
                    tft.text(f8x8, f"Stick firmware {l_get("apps.settings.about.fw.version")} {cache.get("ver_displayname")}" ,0,0,ver_color)
                    tft.text(f8x8, l_get("apps.settings.about.fw.by_kitki30") + " @Kitki30",0,8,ver_color)
                    tft.text(f8x8, l_get("apps.settings.about.fw.apache_license"),0,16,65535)
                    tft.text(f8x8, l_get("apps.settings.about.fw.a_exit"),0,111,65535)
                    tft.text(f8x8, l_get("apps.settings.about.fw.b_credits"),0,119,65535)
                    tft.text(f8x8, l_get("apps.settings.about.fw.c_license"),0,127,65535)
                    while button_a.value() == 1 and button_b.value() == 1 and button_c.value() == 1:
                        time.sleep(osc.DEBOUNCE_TIME)
                    if button_b.value() == 0:
                        open_file.openMenu("/CREDITS")
                    if button_c.value() == 0:
                        open_file.openMenu("/LICENSE")
                        
                elif about_menu == 2:
                    tft.fill(0)
                    tft.text(f8x8, l_get("apps.settings.about.hw.hwinfo"), 0, 0, 65535)
                    serial = machine.unique_id().hex().upper()
                    tft.text(f8x8, osc.DEVICE_NAME, 0, 8, 64288)
                    tft.text(f8x8, l_get("apps.settings.about.hw.esp_serial"), 0, 16, 65535)
                    tft.text(f8x8, serial, 0, 24, 64288)
                    tft.text(f8x8, l_get("menus.popup_any_btn"),0,127,65535)
                    while button_a.value() == 1 and button_b.value() == 1 and button_c.value() == 1:
                        time.sleep(osc.DEBOUNCE_TIME)
                        
                elif about_menu is None:
                    break
                
        # Factory
        elif menu1 == 9:
            confirm_reset = menus.menu(l_get("apps.settings.factory.reset_all"),
                                       [(l_get("menus.no"), None),
                                        (l_get("menus.yes"), 1)])
            if confirm_reset == 1:
                confirm_reset = menus.menu(l_get("apps.settings.factory.it_removes_all"),
                                           [(l_get("menus.menu_cancel"), 2),
                                            (l_get("apps.settings.factory.confirm"), 1)])
                if confirm_reset == 1:
                    nvs.set_int(n_updates, "factory", 1) # Set NVS bootloader entry
                    machine.soft_reset() # Reboot
        else:
            work = False
            
        
    gc.collect()
    ps.set_freq(osc.BASE_FREQ)
