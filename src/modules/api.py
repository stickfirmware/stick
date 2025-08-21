API_URL = "https://api.kitki30.tk/v1" # API URL
USER_AGENT = "Stick firmware (https://github.com/stick)"
LINK_URL = "https://kitki30.tk/link" # Link URL for account linking

# Someone want to help? Partial docs: https://api.kitki30.tk you will be redirected to markdown docs
# This module broken for now

import urequests
import modules.powersaving as ps
import modules.cache as cache
import modules.io_manager as io_man
import modules.popup as popup

def get_request_authenticated(url):
    token = cache.get('token')
    if not token:
        return None
    
    headers = {"User-Agent": USER_AGENT, "authorization": f"Bearer {token}"}
    try:
        result = urequests.get(url, headers=headers)
    except Exception as e:
        print(f"Error in get_request_authenticated: {e}")
        return None
    return result

def get_request(url):
    headers = {"User-Agent": USER_AGENT}
    try:
        result = urequests.get(url, headers=headers)
    except Exception as e:
        print(f"Error in get_request: {e}")
        return None
    return result

# def link(code, interactive=False):
#     headers = {"User-Agent": USER_AGENT}
    
#     result = urequests.post(
#         API_URL + '/auth/link',
#         json={"code": code},
#         headers=headers
#     )
    
#     if result.status_code == 200:
#         data = result.json()
#         cache.set('token', data['token'])
#         cache.set('username', data['username'])
#         if interactive: 
#         return True
#     else:
#         return False

def display_captcha(xpos,ypos):
    import framebuf

    tft = io_man.get("tft")

    result = get_request(API_URL + '/captchas/get')
    if result.status() != 200:
        return False
    rle_string = result.json()['compressedBitmap']
    cache.set('captcha_token', result.json()['token'])
    result.close()
    
    WIDTH = 180
    HEIGHT = 60
    buf = bytearray(WIDTH * HEIGHT * 2)
    fb = framebuf.FrameBuffer(buf, WIDTH, HEIGHT, framebuf.RGB565)

    x = 0
    y = 0
    for item in rle_string.split(';'):
        if not item:
            continue
        count, val = item.split(':')
        count = int(count)
        val = int(val)
        for _ in range(count):
            color = 0x0000 if val else 0xFFFF
            fb.pixel(x, y, color)
            x += 1
            if x >= WIDTH:
                x = 0
                y += 1
                if y >= HEIGHT:
                    break

    ps.boost_allowing_state(True)
    ps.boost_clock()

    tft.blit_buffer(buf, xpos, ypos, WIDTH, HEIGHT)
    ps.boost_allowing_state(False)
    ps.loop()
    return True
    
# def register(username, password, captcha_token):
#     headers = {"User-Agent": USER_AGENT}

#     result = urequests.post(
#         API_URL + '/auth/register',
#         json={
#             "username": username,
#             "password": password,
#             "captchaToken": captcha_token
#         },
#         headers=headers
#     )
#     return result

# def login(username, password, captcha_token=None):
#     headers = {"User-Agent": USER_AGENT}

#     result = urequests.post(
#         API_URL + '/auth/login',
#         json={
#             "username": username,
#             "password": password,
#             "captchaToken": captcha_token
#         },
#         headers=headers
#     )
#     return result

# def logout(token):
#     headers = {"User-Agent": USER_AGENT}
#     result = urequests.post(
#         API_URL + '/auth/logout',
#         json={
#             "token": token,
#         },
#         headers=headers
#     )
#     return result