import network
import modules.nvs as nvs
import esp32

security_map = {
        0: "Open",
        1: "WEP",
        2: "WPA/PSK",
        3: "WPA2/PSK",
        4: "WPA/WPA2/PSK",
}

def format_bssid(bssid_bytes):
    return ':'.join(f'{b:02X}' for b in bssid_bytes)

def execute(args):
    n_wifi = esp32.NVS("wifi")
    if len(args) == 1:
        return "Usage: network {arguments}\nArguments:\nstation - station mode"
    else:
        if args[1] == "station":
            if len(args) == 2:
                return "Usage: network station {arguments}\nArguments:\nhostname (hostname) - sets/gets hostmame\nenable - Enable wlan\ndisable - Disable wlan\ndisconnect - Disconnect from AP\nconnect - Connect to AP\nscan - Scan for APs\nsaved - Saved network functions"
            else:
                nic = network.WLAN(network.STA_IF)
                if args[2] == "enable":
                    nic.active(True)
                    return "Wlan enabled!"
                elif args[2] == "disable":
                    nic.active(False)
                    return "Wlan disabled!"
                elif args[2] == "disconnect":
                    if nic.isconnected():
                        nic.disconnect()
                    return "Disconnected from the access point!"
                elif args[2] == "scan":
                    if len(args) == 3:
                        if nic.active() == True:
                            scan_string = ""
                            for i in nic.scan():
                                if i[5] is not False:
                                    scan_string += str(i[0].decode()) + "\n"
                            return scan_string
                        else:
                            return "Please enable Wlan as station first!"
                    else:
                        if args[3] == "-f":
                            if nic.active() == True:
                                scan_string = "SSID, BSSID, CHAN, RSSI, SEC, HIDD?\n"
                                for i in nic.scan():
                                    if i[5] is not False:
                                        scan_string += str(i[0].decode())
                                        scan_string += ", "
                                        scan_string += format_bssid(i[1])
                                        scan_string += ", "
                                        scan_string += str(i[2])
                                        scan_string += ", "
                                        scan_string += str(i[3])
                                        scan_string += ", "
                                        scan_string += security_map.get(i[4], "unknown")
                                        scan_string += ", "
                                        scan_string += str(i[5])
                                        scan_string += "\n"
                                return scan_string
                            else:
                                return "Please enable Wlan as station first!"
                elif args[2] == "connect":
                    if not nic.active():
                        return "Please enable Wlan as station first!"

                    if len(args) < 4:
                        return (
                            "Usage: network station connect {SSID} (PASSWD*) (Args)\nArguments:\n"
                            "-s - Save configuration to NVS**\n"
                            "*Password only if network is secured!\n"
                            "**Not available for open networks!"
                        )

                    ssid = args[3]
                    passwd = None
                    save_cfg = False

                    if len(args) >= 5:
                        if args[4] == "-s":
                            save_cfg = True
                        else:
                            passwd = args[4]
                    if len(args) >= 6 and args[5] == "-s":
                        save_cfg = True

                    found = False
                    security = -1
                    for i in nic.scan():
                        if i[0].decode() == ssid:
                            found = True
                            security = i[4]
                            break

                    if not found:
                        return "Network was not available!"

                    if security != 0 and passwd is None:
                        return "Password is required for secured network!"
                        
                    if save_cfg and security == 0:
                        return "Can't save open networks!"
                    
                    if nic.isconnected():
                        nic.disconnect()
                    if passwd:
                        nic.connect(ssid, passwd)
                    else:
                        nic.connect(ssid)
                            
                    if save_cfg:
                        nvs.set_float(n_wifi, "conf", 1)
                        nvs.set_string(n_wifi, "ssid", ssid)
                        nvs.set_string(n_wifi, "passwd", passwd)
                    return "Connecting..."
                elif args[2] == "saved":
                    if len(args) == 3:
                        return "Usage: network station saved {arguments}\nArguments:\nview - View saved network\nclear - Clear saved network\nautoConnect {enable / disable} - Set auto connect on startup"
                    if args[3] == "view":
                        if nvs.get_float(n_wifi, "conf") == 0:
                            return "Wi-fi not configured!"
                        else:
                            return "Auto connect: " + str(nvs.get_int(n_wifi, "autoConnect")) + "\nSSID: " + nvs.get_string(n_wifi, "ssid") + "\nPassword: " + nvs.get_string(n_wifi, "passwd")
                    elif args[3] == "clear":
                        nvs.set_float(n_wifi, "conf", 0)
                        nvs.set_int(n_wifi, "autoConnect", 0)
                        nvs.set_string(n_wifi, "ssid", "")
                        nvs.set_string(n_wifi, "passwd", "")
                        return "Wi-fi config cleared!"
                    elif args[3] == "autoConnect":
                        if len(args) == 4:
                            return "Usage: network station saved autoConnect {enable / disable}"
                        else:
                            if args[4] == "enable":
                                nvs.set_int(n_wifi, "autoConnect", 1)
                                return "Auto connect enabled!"
                            elif args[4] == "disable":
                                nvs.set_int(n_wifi, "autoConnect", 0)
                                return "Auto connect disabled!"
                            else:
                                return "Usage: network station saved autoConnect {enable / disable}"
                    else:
                        return "Usage: network station saved {arguments}\nArguments:\nview - View saved network\nclear - Clear saved network\nautoConnect {enable / disable} - Set auto connect on startup"
                elif args[2] == "status":
                    ifconfig = nic.ifconfig()
                    return "WLAN Status: " + str(nic.active()) + "\nIs connected?: " + str(nic.isconnected()) + "\n\nLocal IP: " + ifconfig[0] + "\nSubnet mask: " + ifconfig[1] + "\nGateway: " + ifconfig[2] + "\nDNS: " + ifconfig[3]
                elif args[2] == "hostname":
                    if len(args) == 3:
                        return nic.hostname()
                    else:
                        nvs.set_string(n_wifi, "hostname", args[3])
                        nic.hostname(args[3])
                        return nic.hostname()
                else:
                    return "Usage: network station {arguments}\nArguments:\nhostname (hostname) - sets/gets hostmame\nenable - Enable wlan\ndisable - Disable wlan\ndisconnect - Disconnect from AP\nconnect - Connect to AP\nscan - Scan for APs\nsaved - Saved network functions"
        else:
            return "Usage: network {arguments}\nArguments:\nstation - station mode"