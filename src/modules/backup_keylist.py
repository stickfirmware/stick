"""
List of keys to backup from NVS

Used for backups module
"""

KEYS = [
    "settings;backlight;float", # Backlight power
    "settings;volume;float", # Buzzer volume
    "wifi;conf;float", # Is Wi-Fi configured
    "wifi;autoConnect;int", # Wi-Fi autoconnect
    "wifi;ssid;string", # Wi-Fi SSID
    "wifi;passwd;string", # Wi-Fi Password
    "settings;autorotate;int", # IMU autorotate settings
    "settings;allowsaving;int", # Power saving settings
    "settings;shutdown_mode;int", # Shutdown mode
    "settings;allow_metrics;int", # Diagnostic data sending
    "settings;lang;string", # Language settings
    "settings;timezoneIndex;int", # Timezone settings
    "settings;neo_anim_style;int", # Neopixel animation style
    "settings;neo_enabled;int", # Neopixel enable
    "settings;neo_R;int", # Neopixel Red
    "settings;neo_G;int", # Neo Green
    "settings;neo_B;int", # Neo Blue
    "settings;xp;int", # Pet XP
    "settings;mood;int", # Pet mood
    "settings;dev_apps;int" # Developer apps
]
"""Keys to backup, in format namespace;key;type"""

LIST_VERSION = 1