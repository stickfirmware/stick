import gc
import socket
import ssl

import urequests


def download(url, filename, bufsize=512):
    assert url.startswith("https://"), "Only https supported now"
    url = url[8:]

    slash_pos = url.find('/')
    if slash_pos == -1:
        host = url
        path = '/'
    else:
        host = url[:slash_pos]
        path = url[slash_pos:]

    addr_info = socket.getaddrinfo(host, 443)
    addr = addr_info[0][-1]

    s = socket.socket()
    s.connect(addr)

    s = ssl.wrap_socket(s, server_hostname=host)

    req = "GET {} HTTP/1.0\r\nHost: {}\r\n\r\n".format(path, host)
    s.write(req.encode())

    gc.collect()
    with open(filename, "wb") as f:
        header_ended = False
        leftover = b""
        while True:
            gc.collect()
            data = s.read(bufsize)
            if not data:
                break

            if not header_ended:
                leftover += data
                header_end_idx = leftover.find(b"\r\n\r\n")
                if header_end_idx != -1:
                    header_ended = True
                    body = leftover[header_end_idx+4:]
                    f.write(body)
                    leftover = b""
            else:
                f.write(data)

    s.close()
    
def get(url):
    result = urequests.get(url, headers={"User-Agent": "Stick firmware (https://github.com/stick)"})
    return result