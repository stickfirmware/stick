class AppNotFound(Exception):
    pass

def app_exists(appsConfig, pack_id):
    for app in appsConfig.get("apps", []):
        if app.get("id") == pack_id:
            return app.get("file")
    return None


def run(pack_id):
    import apps.oobe as oobe
    appsConfig = oobe.read_config()
    
    # Check if exists
    file = app_exists(appsConfig, pack_id)
    if file != None:
        modpath = file
        parts = modpath.split(".")
        comd = __import__(modpath)
        for part in parts[1:]:
            comd = getattr(comd, part)
        if hasattr(comd, "run"):
            comd.run()

        import modules.ram_cleaner as rclean
        rclean.deep_clean_module(modpath)
    else:
        raise AppNotFound(f"Error, app '{pack_id}' not found, cannot import!")