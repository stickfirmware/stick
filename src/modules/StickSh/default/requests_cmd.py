import urequests
import json
import gc
import uos

def mkdir_p(path):
    parts = path.split('/')
    current = ''
    for part in parts:
        if part == '':
            continue
        current += '/' + part
        try:
            uos.mkdir(current)
        except OSError as e:
            if e.args[0] != 17:
                raise


def request(method, url, data=None, headers=None):
    gc.collect()
    if headers is None:
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Kitki30-Stick/1.0 (requests)'
        }
    resp = urequests.request(method, url, data=data, headers=headers)
    return resp

def HEAD(url, headers=None):
    gc.collect()
    if headers == None:
        headers = {'User-Agent': 'Kitki30-Stick/1.0 (requests)'}
    response = urequests.head(url, headers=headers)
    return response

def GET(url, headers=None):
    gc.collect()
    if headers == None:
        headers = {'User-Agent': 'Kitki30-Stick/1.0 (requests)'}
    response = urequests.get(url, headers=headers)
    return response

def POST(url, data=None, headers=None):
    return request("POST", url, data, headers)

def PUT(url, data=None, headers=None):
    return request("PUT", url, data, headers)

def DELETE(url, data=None, headers=None):
    return request("DELETE", url, data, headers)

def PATCH(url, data=None, headers=None):
    return request("PATCH", url, data=data, headers=headers)

def download_file(url, filename):
    try:
        response = GET(url)
        if response.status_code == 200:
            folder = '/'.join(filename.split('/')[:-1])
            if folder:
                mkdir_p(folder)
            with open(filename, 'wb') as f:
                f.write(response.content)
            response.close()
            return True
        else:
            response.close()
            return False
    except:
        try:
            response.close()
        except:
            pass
        return False