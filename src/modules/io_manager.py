_HW = {}

def get(name):
    return _HW.get(name)

def set(name, value):
    _HW[name] = value

def clear():
    _HW.clear()