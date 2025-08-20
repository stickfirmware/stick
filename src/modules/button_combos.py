import modules.io_manager as io_man

# Gets button by name (ex. "a")
def get_button(name):
    return io_man.get("button_" + name.lower())

# Check if button combo is pressed/released
def combo(buttons, pressed=True):
    buttons = [get_button(b) for b in buttons]
    if pressed:
        return all(b.value() == 0 for b in buttons)
    else:
        return all(b.value() == 1 for b in buttons)
    
# Check if any button in list is pressed/released
def any_btn(buttons, pressed=True):
    buttons = [get_button(b) for b in buttons]
    if pressed:
        return any(b.value() == 0 for b in buttons)
    else:
        return any(b.value() == 1 for b in buttons)