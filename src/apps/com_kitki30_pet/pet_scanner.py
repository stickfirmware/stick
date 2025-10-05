import os

import modules.files as files
import modules.json as json
from modules.printer import Levels as log_levels
from modules.printer import log


def get_list(scan_path: str) -> list[tuple]:
    
    # Get directory
    list_dir = os.listdir(scan_path)
    
    # Scan for pets
    pets = []
    
    for pet_folder in list_dir:    
        # Check if there is pet manifest in the folder
        if "pet.json" in os.listdir(files.path_join(scan_path, pet_folder)):
            # Read manifest
            pet_manifest = json.read(files.path_join(scan_path, pet_folder, "pet.json"))
            if pet_manifest is None:
                log("Pet manifest read error", log_levels.WARNING)
                
            try:
                pet_name = pet_manifest["name"]
                pet_tuple = (pet_name, files.path_join(scan_path, pet_folder))
                pets.append(pet_tuple)
                log(f"Pet found! {pet_tuple}", log_levels.DEBUG)
            except (KeyError, ValueError):
                log("Pet manifest read error.\nIs it a pet manifest?", log_levels.WARNING)
        else:
            log("No pet found in folder!", log_levels.WARNING)
    
    log("Pet scan successful!")        
    
    return pets