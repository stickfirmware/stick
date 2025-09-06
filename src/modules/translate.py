"""
Translations for Stick firmware.
"""

import modules.json as json
import modules.printer as printer
main_file = None
language = None

def init():
    """
    Reads main languages.json file.W
    """
    
    global main_file
    try:
        main_file = json.read("/language/languages.json")
        printer.log(main_file)
    except Exception as e:
        printer.log("Failed to load languages.json: " + str(e))
        main_file = {"langs": [
        "en",
        "pl"
    ],
    "en": {
        "name": "English",
        "path": "/language/lang_en.json"
    },
    "pl": {
        "name": "Polski",
        "path": "/language/lang_pl.json"
    }}
    return

def load(lang):
    """
    Loads language.

    Args:
        lang (str): Name of the language (ex. "pl" or "en")

    Returns:
        bool: True if success, False if failed
    """
    
    import modules.files as files
    printer.log(lang)
    global language
    try:
        lang_path = main_file[lang]["path"]
        printer.log(lang_path)
        if files.exists(lang_path + ".gz"):
            try:
                language = json.read_gzipped(lang_path + ".gz")
                try:
                    import os
                    for file in os.listdir("/language"):
                        if file.endswith(".json") and file.startswith("lang_"):
                            os.remove(file)
                    printer.log("Removed ungzipped ver of language packs to save disk space")
                except:
                    printer.log("Failed to remove ungzipped lang")
            except:
                language = json.read(lang_path)
        else:
            language = json.read(lang_path)
        printer.log(language)
        return True
    except Exception as e:
        printer.log(f"Failed to load {lang_path}: {e}")
        language = {}
        return False
        
def get(path):
    """
    Gets translation

    Args:
        path (str): path to string in language file (ex. "crashes.error")

    Returns:
        str: Requested string, or "Translate error" if non-existent
        
    Example:
        >>> get("crashes.error")
        "Blad"
    """
    try:
        parts = path.split(".")
        d = language
        for p in parts:
            d = d[p]
        return d
    except (KeyError, TypeError):
        return "Translate error"
        
init()