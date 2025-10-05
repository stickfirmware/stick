"""
Translations for Stick firmware with lazy loading + cache
"""

import gc

import modules.json as json
import modules.printer as printer
from modules.printer import Levels as log_levels

main_file = None
_language_cache = {}
_current_lang = None
_last_access = {}


def init():
    """
    Reads main languages.json file (lang registry).
    """
    global main_file
    try:
        main_file = json.read("/language/languages.json")
    except Exception as e:
        printer.log("Failed to load languages.json: " + str(e), log_levels.WARNING)
        main_file = {
            "langs": ["en", "pl"],
            "en": {"name": "English", "path": "/language/lang_en.json"},
            "pl": {"name": "Polski", "path": "/language/lang_pl.json"}
        }


def _load_lang(lang):
    """
    Loads given language into cache if not present.
    """
    import modules.files as files
    global _language_cache, _last_access

    if lang in _language_cache:
        _last_access[lang] = gc.mem_free()
        return _language_cache[lang]

    try:
        lang_path = main_file[lang]["path"]
        printer.log(f"Loading {lang} from {lang_path}")

        if files.exists(lang_path + ".gz"):
            try:
                data = json.read_gzipped(lang_path + ".gz")
                try:
                    import os
                    for file in os.listdir("/language"):
                        if file.endswith(".json") and file.startswith("lang_"):
                            gz_path = file + ".gz"
                            if files.exists("/language/" + gz_path):
                                os.remove("/language/" + file)
                    printer.log("Removed uncompressed lang files (only with .gz)")
                except Exception:
                    printer.log("Failed to remove uncompressed lang")
            except Exception:
                data = json.read(lang_path)
        else:
            data = json.read(lang_path)


        _language_cache[lang] = data
        _last_access[lang] = gc.mem_free()
        return data

    except Exception as e:
        printer.log(f"[lang] Failed to load {lang}: {e}", log_levels.WARNING)
        return {}


def load(lang):
    """
    Switch current language. Lazy-loads if not cached.
    """
    global _current_lang
    _current_lang = lang
    return _load_lang(lang) != {}


def unload(lang=None):
    """
    Unloads a language from cache to free RAM.
    If lang=None, unloads least recently used one.
    """
    global _language_cache, _last_access

    if lang is None:
        if not _last_access:
            return
        victim = sorted(_last_access.items(), key=lambda x: x[1])[0][0]
        lang = victim

    if lang in _language_cache:
        del _language_cache[lang]
        _last_access.pop(lang, None)
        gc.collect()
        printer.log(f"Unloaded {lang}")


def get(path):
    """
    Gets translation string from current language.
    
    Args:
        path (str): path to string (ex. "apps.minesweeper.name")
        
    Returns:
        str: String or "Translate error" if could not translate
        
    Example:
        >>> import modules.translate as translate
        >>> translate.load("pl")
        >>> print(translate.get("apps.minesweeper.name"))
        "Saper"
    """
    global _current_lang
    if not _current_lang:
        return "Translate error"

    lang_data = _load_lang(_current_lang)
    try:
        parts = path.split(".")
        d = lang_data
        for p in parts:
            d = d[p]
        return d
    except (KeyError, TypeError) as e:
        printer.log(f"[lang] Missing path {path}: {e}", log_levels.WARNING)
        return "Translate error"


# init languages registry at import
init()