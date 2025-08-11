import gc
import socket

def download(url, filename, bufsize=512):
    # Split to parts
    assert url.startswith("http://"), "Only http supported"
    url = url[7:]  # delete http://

    slash_pos = url.find('/')
    if slash_pos == -1:
        host = url
        path = '/'
    else:
        host = url[:slash_pos]
        path = url[slash_pos:]

    addr_info = socket.getaddrinfo(host, 80)
    addr = addr_info[0][-1]

    s = socket.socket()
    s.connect(addr)
    req = "GET {} HTTP/1.0\r\nHost: {}\r\n\r\n".format(path, host)
    s.send(req.encode())

    gc.collect()
    with open(filename, "wb") as f:
        header_ended = False
        leftover = b""
        while True:
            gc.collect()
            data = s.recv(bufsize)
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
