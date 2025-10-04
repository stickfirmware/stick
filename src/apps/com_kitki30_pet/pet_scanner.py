import os

import modules.json as json
import modules.files as files
from modules.printer import log

def get_list(scan_path: str) -> list[tuple]:
    
    # Get directory
    list_dir = os.listdir(scan_path)
    
    # Scan for pets
    pets = []
    
    for pet_folder in list_dir:
        log(f"Scanning {pet_folder} for pets...")
        
        # Check if there is pet manifest in the folder
        if "pet.json" in os.listdir(files.path_join(scan_path, pet_folder)):
            # Read manifest
            pet_manifest = json.read(files.path_join(scan_path, pet_folder, "pet.json"))
            if pet_manifest is None:
                log("Pet manifest read error")
                
            try:
                pet_name = pet_manifest["name"]
                languages = pet_manifest["language_versions"]
                pet_tuple = (pet_name, languages, files.path_join(scan_path, pet_folder))
                pets.append(pet_tuple)
                log(f"Pet found! {pet_tuple}")
            except (KeyError, ValueError):
                log("Pet manifest read error.\nIs it a pet manifest?")
        else:
            log("No pet found!")
            
    return pets