"""
App open helper for Stick firmware
"""

class AppNotFound(Exception):
    pass

def app_exists(appsConfig: dict, pack_id: str) -> str | None:
    """
    Gets module name of app if it exists
    
    Args:
        appsConfig (dict): Apps config dictionary (Json)
        pack_id (str): ID of package you are searching for

    Returns:
        str | None: Module name or None if not found
    """
    for app in appsConfig.get("apps", []):
        if app.get("id") == pack_id:
            return app.get("file")
    return None


def run(pack_id: str, skip_intro = False):
    """
    Run app with package id you provided

    Args:
        pack_id (str): Package ID to run
    """
    import modules.io_manager as io_man
    import modules.oobe as oobe
    from modules.printer import Levels as log_levels
    from modules.printer import log
    
    log(f"Launching app: {pack_id}")
    
    log("Reading config", log_levels.DEBUG)
    appsConfig = oobe.read_config()
    
    # Grant xp
    log("Granting XP to user", log_levels.DEBUG)
    import modules.xp_leveling as xp_levels
    xp_levels.add_xp(5)
    xp_levels.add_mood(2)
    
    # Check if exists
    file = app_exists(appsConfig, pack_id)
    if file is not None:
        tft = io_man.get("tft")
        
        if not skip_intro:
            tft.fill(65535)
            import modules.appboot as appboot
        
        modpath = file
        parts = modpath.split(".")
        
        if not skip_intro:
            appboot.make_text(tft)
        
        comd = __import__(modpath)
        for part in parts[1:]:
            comd = getattr(comd, part)

        if not skip_intro:
            appboot.app_boot_make_anim(tft)
        
        if hasattr(comd, "run"):
            comd.run()
        
        import modules.ram_cleaner as rclean
        rclean.deep_clean_module(modpath)
    else:
        log("App not found, cannot import!", log_levels.WARNING)
        raise AppNotFound(f"Error, app '{pack_id}' not found, cannot import!")