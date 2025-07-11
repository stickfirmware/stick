jobs = []

def loop():
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
    elif path.startswith('/html/'):
        with open('/html/config.html', 'r') as f:
            response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n' + f.read()
    elif path == '/' or path == '/':
        with open('/html/index.html', 'r') as f:
            response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n' + f.read()

    else:
        response = 'HTTP/1.1 404 Not Found\nContent-Type: text/plain\n\nNot found'

    conn.sendall(response.encode('utf-8'))
    conn.close()
