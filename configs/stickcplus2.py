# Config info
DEVICE_NAME = "M5StickC Plus 2" # Device name
RELEASE_NAME = "stickcplus2" # Name in builder

# Debug
ENABLE_DEBUG_PRINTS = False

# Power managament
HAS_HOLD_PIN = True # Do we need to put power hold pin HIGH? (Like on M5StickC Plus 2)
HOLD_PIN = 4
BATTERY_ADC = 38 # Battery ADC pin (Often called Battery Detect by M5Stack), used to get battery voltage, needs voltage divider.

# Sound
HAS_BUZZER = True # Has buzzer?
BUZZER_PIN = 2
HAS_MIC = True # Has mic?
MIC_DATA = 34 # Microphone DATA Pin
MIC_CLK = 0 # Mic Clock Pin

# SD Card
HAS_SD_SLOT = False # Has built-in sd card slot?
SD_CS = 12
SD_MOSI = 14
SD_MISO = 39
SD_CLK = 40

# IR
IR_PIN = 19

# Input methods
INPUT_METHOD = 1 # 1 - Standard (3 Buttons, Exit, Cycle, Select, used in sticks), 2 - Cardputer (Input over cardputer keyboard)

# Standard input method settings
BUTTON_A_PIN = 37
BUTTON_B_PIN = 39
BUTTON_C_PIN = 35

# GROVE Port
HAS_GROVE = True
GROVE_SLOT = 1
GROVE_SDA = 32
GROVE_SCL = 33

# Shared I2C (RTC + IMU)
HAS_SHARED_I2C = True # True if has RTC + IMU shared i2c
HAS_RTC = True # True if has RTC, overwritten by HAS_SHARED_I2C if it's False
HAS_IMU = True # True if has IMU
I2C_SLOT = 0 # I2C Slot???, can be 0 or 1 depending on the pins
I2C_SDA = 21
I2C_SCL = 22

# st7789
LCD_LOAD_BG = 0 # Loading screen background color
LCD_LOAD_TEXT = 65535 # Loading screen text color
LCD_SPI_SLOT = 1 # Something like with I2C, 0 or 1
LCD_SPI_BAUD = 26_000_000 # SPI Baud in Hz
LCD_SPI_SCK=13 # LCD SCK Pin
LCD_SPI_MOSI=15 # LCD MOSI Pin
LCD_SPI_MISO = None # Leave it None, does nothing
LCD_SPI_CS = 5 # LCD Chip select pin
LCD_DC = 14 # LCD Data/Command pin
LCD_RESET = 12 # LCD Reset pin
LCD_BL = 27 # Backlight pin
LCD_BL_FREQ = 1000 # Backlight frequency, higher values may not work
LCD_HEIGHT = 135 # LCD Height in pixels
LCD_WIDTH = 240 # LCD Width in pixels
LCD_ROTATIONS = {
    "BUTTON_LEFT": 3, # M5Stick button on the left, Cardputer keyboard on bottom
    "BUTTON_RIGHT": 1, # Stick button right, Cardputer kb top
    "BUTTON_UPPER": 2, # Stick button up, cardputer kb left
    "BUTTON_BOTTOM": 0 # Stick button down, cardputer kb right
    }
IMU_ROTATE_THRESHOLD = 0.9 # IMU Sensitivity
LCD_POWER_SAVE_BL = 0.3 # Backlight brightness on power saving

# MCU Frequencies
ULTRA_FREQ = 240 * 1000000 # Ultra fast, used for renders
FAST_FREQ = 160 * 1000000 # Fast
BASE_FREQ = 80 * 1000000 # Basic, used in loops
SLOW_FREQ = 40 * 1000000 # Slow, used in power saving, clock can be 1 second late
ULTRA_SLOW_FREQ = 20 * 1000000

# Networking
WIFI_DEF_HOST = "Stick" # Default WLAN hostname

# Loop timings
WIFI_DISABLE_TIMEOUT = 15 * 1000 # Timeout for disabling wifi if not connected
POWER_SAVE_TIMEOUT = 15 * 1000 # Time to enter power saving after no activity
IMU_CHECK_TIME = 200 # IMU update time, in ms
IMU_STAY_TIME = 1000 # IMU stay time, in ms, device needs to be in same rotatation for X ms to accept rotation as stable
NTP_SYNC_TIME = 600000 # NTP automatic sync time in ms
LOOP_WAIT_TIME = 0.025 # Time loops wait until starting again in seconds (Start, wait time, start)
DIAGNOSTIC_REFRESH_TIME = 2000 # On-screen diagnostics (Voltage + CPU speed in menu)

# Boot settings
BOOT_ENABLE_RECOVERY = True
BOOT_RECOVERY_PATH = "/recovery/recovery.py"
BOOT_RECOVERY_PIN = BUTTON_B_PIN
BOOT_MAINOS_PATH = "/mainos.py"
BOOT_STARTING_SCRIPTS = [ # Scripts to fire at start of the device, in bootloader (main.py)
    '/scripts/checkbattery.py'
    ]
BOOT_ENABLE_UPDATES = False # Enable searching for updates on boot
BOOT_UPDATE_PATH = "/update.py"

# Others
EMERG_BUFF_SIZE = 1000 # Emergency buffer allocation size in bytes