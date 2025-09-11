"""
App open helper for Stick firmware
"""

import asyncio

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


async def run(pack_id: str):
    """
    Run app with package id you provided

    Args:
        pack_id (str): Package ID to run
    """
    import apps.oobe as oobe
    import modules.io_manager as io_man
    appsConfig = oobe.read_config()
    
    # Check if exists
    file = app_exists(appsConfig, pack_id)
    if file != None:
        tft = io_man.get("tft")
        tft.fill(65535)
        import modules.appboot as appboot
        
        modpath = file
        parts = modpath.split(".")
        
        await appboot.make_text(tft)
        
        comd = __import__(modpath)
        for part in parts[1:]:
            comd = getattr(comd, part)

        await appboot.app_boot_make_anim(tft)
        
        if hasattr(comd, "run"):
            comd.run()
        
        import modules.ram_cleaner as rclean
        rclean.deep_clean_module(modpath)
    else:
        raise AppNotFound(f"Error, app '{pack_id}' not found, cannot import!")