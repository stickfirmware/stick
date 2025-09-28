"""
Module that helps developer to manage licenses. Without taking more flash space.
"""

supported = ["mit", "apache_2_0"]

def get_license(license_name, author, year):
    if license_name not in supported:
        raise ValueError("License not supported")
    
    with open(f"/licenses/{license_name}", "r") as f:
        license_text = f.read()
        license_text = license_text.replace("%year%", str(year)).replace("%author%", author)
        
    return license_text