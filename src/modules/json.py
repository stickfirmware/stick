import ujson as json

def read(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except:
        return None

def write(filename, data):
    try:
        with open(filename, 'wb') as file:
            json.dump(data, file)
        return True
    except:
        return False
        
def read_from_string(data):
    try:
        return json.loads(data)
    except:
        return None