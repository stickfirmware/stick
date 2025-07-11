# Settings for Kitki30 Boot


# Allow list for secure boot

# You can leave it blank if secure boot is not enabled
# Hashes in order: mainos, recovery
# Format: MD5 Hash (Lowercase letters)

ALLOW_LIST = [
    'ef4d13418e763e8c46353b876fc4cc3f', 'f2f937d2303cfdbe518cf1ce5ad71112' # Version 1.3.0 hashes 
    ]


# Secureboot
# Enable it if you want, make sure you have correct hashes, or it won't boot
# It it very slow

SECURE_BOOT = False

# Starting scripts
# Add path to script to run it before system, can be used for low battery shutdown
STARTING_SCRIPTS = [
    '/scripts/checkbattery.py'
    ]

# MainOS

MAINOS_PATH = "/mainos.py" # Path to main script, boots at default, cannot be disabled.

# Recovery

ENABLE_RECOVERY = True # Enable if you have recovery script
RECOVERY_PATH = "/recovery/recovery.py" # Recovery script path
RECOVERY_PIN = 39 # Recovery button Pin

# Updates

ENABLE_UPDATES = True # Enable if you have update script, will boot when exists at provided path
UPDATE_PATH = "/update.py" # Update script path