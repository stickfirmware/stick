import ujson as json

def read(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            file.close()
        return data
    except:
        return None
    
def read_gzipped(filename):
    import deflate
    with open(filename, "rb") as f:
        with deflate.DeflateIO(f, deflate.AUTO) as f:
            data = json.load(f)
            f.close()
            return data

def write(filename, data):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file)
            file.close()
        return True
    except:
        return False
        
def read_from_string(data):
    try:
        return json.loads(data)
    except:
        return None