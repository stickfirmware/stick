def center_x(text, width):
    text_width = len(text) * width
    x = (240 - text_width) // 2
    return x

def center_y(text, height):
    text_height = height
    x = (135 - text_height) // 2
    return x