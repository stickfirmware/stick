import modules.cache as cache
import modules.menus as menus
import modules.numpad as numpad
import modules.nvs as nvs
import modules.popup as popup


def run():
    popup.show("This tool is used for getting or setting nvs values, make sure you know variable types and maximum values to not break system.")
    
    namespace = numpad.keyboard("NVS Namespace")
    if namespace is None:
        popup.show("NVS namespace not set!!!")
        return
    
    key = numpad.keyboard("NVS Key") 
    if key is None:
        popup.show("NVS key not set!!!")
        return
    
    val_type = menus.menu("Select value type", [("Int", 1), ("Float", 2), ("String", 3), ("Exit", None)])
    if val_type is None:
        popup.show("NVS value type not set!!!")
        return
    
    operation_type = menus.menu("Select operation type", [("Get", 1), ("Set", 2), ("Exit", None)])
    if operation_type is None:
        popup.show("NVS operation type not set!!!")
        return
    
    namespace = cache.get_nvs(str(namespace))
    
    value = None
    if val_type == 1:
        value = nvs.get_int(namespace, str(key))
    elif val_type == 2:
        value = nvs.get_float(namespace, str(key))
    elif val_type == 3:
        value = nvs.get_string(namespace, str(key))
        
    popup.show(f"Namespace: {namespace}\nKey: {key}\nValue: {value}")
    
    if operation_type == 1:
        return
    
    new_value = numpad.keyboard("NVS new value") 
    if new_value is None:
        popup.show("NVS new value not set!!!")
        return
    
    if val_type == 1:
        value = nvs.set_int(namespace, str(key), int(new_value))
    elif val_type == 2:
        value = nvs.set_float(namespace, str(key), float(new_value))
    elif val_type == 3:
        value = nvs.set_string(namespace, str(key), str(new_value))
        
    popup.show("New value set!")