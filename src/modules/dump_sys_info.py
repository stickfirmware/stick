import modules.translate as translate

def language_pack():
    if translate.language == None:
        return "Pack not loaded"
    authors_list = translate.get("lang_info.authors")
    authors = " ".join(authors_list) if authors_list else ""
    version = str(translate.get("lang_info.version")[0]) + "." + str(translate.get("lang_info.version")[1])
    return f"{translate.get("lang_info.name")} ({translate.get("lang_info.code")}, v{version}, {authors})"