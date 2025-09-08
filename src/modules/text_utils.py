"""
Text placement helper for Stick firmware
"""

def center_x(text: str, width: int) -> int:
    """
    Center x of text on screen

    Args:
        text (str): Text to center
        width (int): Width of font

    Returns:
        int: x coordinates of text
    """
    text_width = len(text) * width
    x = (240 - text_width) // 2
    return x

def center_y(height: int) -> int:
    """
    Center y of text on screen

    Args:
        height (int): Height of font

    Returns:
        int: y coordinates of text
    """
    text_height = height
    x = (135 - text_height) // 2
    return x