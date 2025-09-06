# App packages guide

New versions of Stick firmware have built in app installer, this is a guide for developers

# Package structure
Packages are just zips, with a specific structure, they can also be with ``.stk`` extension.

## Manifest
Manifests tell system what app is this, how to install it, version and many more. It should be placed on the root of the package as ``manifest.json``
### V1 (Latest)
Manifest V1 consists of 8 fields:

- version - version of manifest, for V1 should be 1
- app_ver - app version, integer incremental
- name - name of your app - string
- app_type - type of the app, integer, 0 - Standard app with UI, 1 - Dependency pack (Currently not supported)
- install_dependencies - either true or false, if true dependencies from /dependencies folder will be installed (Currently not supported)
- description - your app description - string
- entrypoint - main app filename, in python import syntax (if your file is named app.py, put app here, replace slashes (/) with dots)
- pack_id - unique id of your app package, similar to androids ID's

Example manifest:
```
{
    "version": 1,
    "app_ver": 2,
    "name": "Test app",
    "app_type": 0,
    "install_dependencies": false,
    "description": "Test app, for handle_apps testing purposes",
    "entrypoint": "app",
    "pack_id": "com.kitki30.test_app"
}
```

## Standard app with UI, main file structure
Standard app with UI type is an app type that is just an app with User Interface, they appear in menu, and user can run them. Regardless of manifest version, main file structure (specified in entrypoint field) is the same.

When user runs the app from menu, app is imported and ``run()`` functions is called, without any arguments, app doesn't need to return anything.

# Where apps are saved?
All apps are saved to ``/apps/thirdparty/{APP_ID_FROM_MANIFEST}`` all dots in app manifest are replaced with ``_``

# Limitations
- Apps are currently not sandboxed, they run "as root"
- There is 64KB package size limit
- Only STORED (no compression) zips are tested, DEFLATE compressed ones may not work.