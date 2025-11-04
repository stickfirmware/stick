import gc
import time

import machine
import network

import fonts.def_8x8 as f8x8
import modules.cache as cache
import modules.crash_handler as c_handler
import modules.io_manager as io_man
import modules.menus as menus
import modules.nvs as nvs
import modules.os_constants as osc
import modules.popup as popup
import modules.powersaving as ps
import modules.printer as printer
import modules.wifi_master as wifi_man
from modules.decache import decache
from modules.printer import Levels as log_levels
from modules.translate import get as l_get

printer.log("Getting buttons", log_levels.DEBUG)
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
                            (l_get("apps.settings.menu1.power"), 50),
                            (l_get("apps.settings.menu1.neopixel"), 5),
                            (l_get("apps.settings.menu1.sound"), 2),
                            (l_get("apps.settings.menu1.wifi"), 3),
                            (l_get("apps.settings.menu1.sdcard"), 7),
                            (l_get("apps.settings.menu1.language"), 11),
                            (l_get("apps.settings.menu1.about"), 8),
                            (l_get("apps.settings.menu1.factory"), 9),
                            (l_get("apps.settings.menu1.backups"), 10),
                            (l_get("apps.settings.menu1.show_guides_again"), 12),
                            (l_get("menus.menu_close"), None)]) # ("Account", 10),
        
        # Power settings
        if menu1 == 50:
            import apps.settings_menus.power_menu_gui as pm_gui
            pm_gui.run()
            decache("apps.settings_menus.power_menu_gui")
            del pm_gui
                
        # Show guides again
        elif menu1 == 12:
            n_guides = cache.get_nvs("guides")
            nvs.set_int(n_guides, 'quick_start', 0)
            nvs.set_int(n_guides, 'account_popup', 0)
            popup.show(l_get("apps.settings.guides.reboot_notify"), l_get("popups.info"))
            
        # Clock
        elif menu1 == 0:
            import apps.settings_menus.clock_gui as c_gui
            c_gui.run()
            decache("apps.settings_menus.clock_gui")
            del c_gui
                
        # Langs
        elif menu1 == 11:
            import apps.settings_menus.language_gui as l_gui
            l_gui.run()
            decache("apps.settings_menus.language_gui")
            del l_gui
            
        # LCD / st7789 settings
        elif menu1 == 1:
            import apps.settings_menus.lcd_settings as l_gui
            l_gui.run()
            decache("apps.settings_menus.lcd_settings")
            del l_gui
                        
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
            
            import apps.settings_menus.neopixel_gui as np_gui
            np_gui.run()
            decache("apps.settings_menus.neopixel_gui")
            del np_gui
                    
        # Wi-Fi settings
        elif menu1 == 3:
            # TODO: Move this to apps.settings
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
            
            import apps.settings_menus.sd_gui as s_gui
            s_gui.run()
            decache("apps.settings_menus.sd_gui")
            del s_gui
        
        # About screen
        elif menu1 == 8:
            import apps.settings_menus.about_gui as a_gui
            a_gui.run()
            decache("apps.settings_menus.about_gui")
            del a_gui
                
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
        
        # Backups
        elif menu1 == 10:
            import apps.settings_menus.backups_gui as b_gui
            b_gui.run()
            decache("apps.settings_menus.backups_gui")
            del b_gui
            
        else:
            work = False
            
        
    gc.collect()
    ps.set_freq(osc.BASE_FREQ)