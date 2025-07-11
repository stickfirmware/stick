# Dumb Package Tool
import modules.StickSh.executor as texec
import modules.StickSh.default.requests_cmd as req
import json
import os
import modules.json as json_wrap
import version as v

def setup():
    if "usr" not in os.listdir("/"):
        os.mkdir("/usr")
    if "pkg" not in os.listdir("/usr/"):
        os.mkdir("/usr/pkg")
    if "dpt" not in os.listdir("/usr/"):
        os.mkdir("/usr/dpt")
    if "repos" not in os.listdir("/usr/dpt/"):
        os.mkdir("/usr/dpt/repos")
        
    data = {
        "repos": [
            {
                "name": "stick-dpt-main",
                "manifest": "https://raw.githubusercontent.com/Kitki30/Stick-DPT/refs/heads/main/repo.json",
                "localpath": "/usr/dpt/repos/stick-dpt-main.json"
            }
        ]
    }
    
    
    with open("/usr/dpt/repos.json", "w") as f:
        f.write(json.dumps(data))
    
    return "DPT is ready to use!"
    
def update():
    try:
        repolist = json_wrap.read('/usr/dpt/repos.json')
        if repolist == None:
            return "DPT needs to be setup first, use dpt setup"
        for repo in repolist['repos']:
            texec.term_print("Updating " + repo['name'])
            if req.download_file(repo['manifest'], repo['localpath']) == True:
                texec.term_print("Done!")
            else:
                texec.term_print("Failed!")
        return "Repos are updated!"
    except OSError:
        return "DPT needs to be setup first, use dpt setup"
    except:
        return "Unknown exception! Please check your repos!"
    
def install(package_name):
    try:
        repos_data = json_wrap.read('/usr/dpt/repos.json')
        repos = repos_data.get("repos", [])
        
        for repo in repos:
            repo_manifest = json_wrap.read(repo['localpath'])
            if not repo_manifest:
                texec.term_print("Could not read repo manifest: " + repo['localpath'])
                continue
            
            packages = repo_manifest.get("packages", {})
            if package_name in packages:
                manifest_url = packages[package_name]
                texec.term_print("Package found!")
                pkgmnloc = "/temp/" + str(int(time.time())) + ".dptcache"
                if req.download_file(manifest_url, pkgmnloc) == True:
                    texec.term_print("Manifest downloaded!")
                    pkgmn = json_wrap.read(pkgmnloc)
                    texec.term_print("Package info:")
                    texec.term_print("Name: " + pkgmn['name'])
                    texec.term_print("Description: " + pkgmn['desc'])
                    texec.term_print("License: " + pkgmn['MIT'])
                    texec.term_print("Version: " + pkgmn['version']['major'] + "." + pkgmn['version']['minor'] + "." + pkgmn['version']['patch'])
                    texec.term_print("Sys ver: " + str(v.MAJOR) + "." + str(v.MINOR) + "." + str(v.PATCH))
                    texec.term_print("Minimal sys ver: " + pkgmn['sysVerMin']['major'] + "." + pkgmn['sysVerMin']['minor'] + "." + pkgmn['sysVerMin']['patch'])
                    if int(pkgmn['sysVerMin']['major']) =< v.MAJOR and int(pkgmn['sysVerMin']['minor']) <= v.MINOR and int(pkgmn['sysVerMin']['patch']) <= v.PATCH:
                        texec.term_print("System version OK!")
                    else:
                        texec.term_print("System version too low!\nPlease update first!")
                else:
                    texec.term_print("Manifest could not be downloaded!")
                    return False
        texec.term_print("Package was not found in any repo!")
        return False
    except Exception as e:
        texec.term_print("Could not parse/install package")
        return False
    
def execute(args):
    if len(args) >= 2:
        if args[1] == "update":
            return update()
        if args[1] == "setup":
            return setup()
    else:
        return "Usage: dpt {command}\n\nCommands:\nsetup - setup DPT\nupdate - update saved repos"