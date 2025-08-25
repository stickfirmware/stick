# Consts
from micropython import const

# Config info
DEVICE_NAME = const("M5Stack Cardputer v1.1") # Device name
RELEASE_NAME = const("cardputerv1_1") # Name in builder

# Debug
ENABLE_DEBUG_PRINTS = const(False)
LESS_RAM_CLEANER_OUTPUT = const(True) # Don't show ram cleaner output

# Default language
DEFAULT_LANGUAGE = "en"

# Power managament
HAS_HOLD_PIN = const(False) # Do we need to put power hold pin HIGH? (Like on M5StickC Plus 2)
HOLD_PIN = None
BATTERY_ADC = const(10) # Battery ADC pin (Often called Battery Detect by M5Stack), used to get battery voltage, needs voltage divider.

# Sound
HAS_BUZZER = const(False) # Has buzzer?
BUZZER_PIN = None

HAS_MIC = const(True) # Has mic?
MIC_DATA = const(46) # Microphone DATA Pin
MIC_CLK = const(43) # Mic Clock Pin

HAS_SPEAKER = const(True) # Has speaker?
SPEAKER_BCLK  = const(41)  # Bit Clock (I2S BCLK)
SPEAKER_SDATA = const(42)  # Serial Data (I2S DATA)
SPEAKER_LRCLK = const(43)  # Left/Right Clock (I2S WS/LRCLK)

# SD Card
HAS_SD_SLOT = const(True) # Has built-in sd card slot?
SD_CS = const(12)
SD_MOSI = const(14)
SD_MISO = const(39)
SD_CLK = const(40)
SD_FREQ = const(10_000_000) # SD Card frequency in Hz, it can not work past 10 MHz

# IR
IR_PIN = const(44) # Built-in IR pin
IR_ALLOWED_PINS = [1,2,44] 
IR_SENDING_WAIT_TIME = const(0.3)

ALLOW_IR_RECORD = const(False) # Allow IR recording?
IR_RECORD_PIN = const(26)

# Input methods
INPUT_METHOD = const(2) # 1 - Standard (3 Buttons, Exit, Cycle, Select, used in sticks), 2 - Cardputer (Input over cardputer keyboard)

# Standard input method settings
BUTTON_A_PIN = None
BUTTON_B_PIN = None
BUTTON_C_PIN = None

# GROVE Port
HAS_GROVE = const(True)
GROVE_SLOT = const(1)
GROVE_YELLOW = const(2)
GROVE_WHITE = const(1)

# Shared I2C (RTC + IMU)
HAS_SHARED_I2C = const(False) # True if has RTC + IMU shared i2c
HAS_RTC = const(True) # True if has RTC, overwritten by HAS_SHARED_I2C if it's False
HAS_IMU = const(True) # True if has IMU
I2C_SLOT = const(0) # I2C Slot???, can be 0 or 1 depending on the pins
I2C_SDA = const(21)
I2C_SCL = const(22)

# st7789
LCD_LOAD_BG = const(0) # Loading screen background color
LCD_LOAD_TEXT = const(65535) # Loading screen text color
LCD_SPI_SLOT = const(1) # Something like with I2C, 0 or 1
LCD_SPI_BAUD = const(26_000_000) # SPI Baud in Hz
LCD_SPI_SCK= const(36) # LCD SCK Pin
LCD_SPI_MOSI= const(35) # LCD MOSI Pin
LCD_SPI_MISO = None # Leave it None, does nothing
LCD_SPI_CS = const(37) # LCD Chip select pin
LCD_DC = const(34) # LCD Data/Command pin
LCD_RESET = const(33) # LCD Reset pin
LCD_BL = const(38) # Backlight pin
LCD_BL_FREQ = const(1000) # Backlight frequency, higher values may not work
LCD_HEIGHT = const(135) # LCD Height in pixels
LCD_WIDTH = const(240) # LCD Width in pixels
LCD_ROTATIONS = {
    "BUTTON_LEFT": 1, # M5Stick button on the left, Cardputer keyboard on bottom
    "BUTTON_RIGHT": 3, # Stick button right, Cardputer kb top
    "BUTTON_UPPER": 0, # Stick button up, cardputer kb left
    "BUTTON_BOTTOM": 2 # Stick button down, cardputer kb right
    }
IMU_ROTATE_THRESHOLD = const(0.9) # IMU Sensitivity
LCD_POWER_SAVE_BL = const(0.3) # Backlight brightness on power saving

# MCU Frequencies
ULTRA_FREQ = const(240_000_000) # Ultra fast, used for renders
FAST_FREQ = const(160_000_000) # Fast
BASE_FREQ = const(80_000_000) # Basic, used in loops
SLOW_FREQ = const(40_000_000) # Slow, used in power saving, clock can be 1 second late
ULTRA_SLOW_FREQ = const(20_000_000)

# Networking
WIFI_DEF_HOST = const("Cardputer") # Default WLAN hostname
REQUESTS_USERAGENT = const("Stick firmware/Cardputer") # User agent for requests module (WIP)

# Loop timings
WIFI_PWR_SAVER_TIME = const(15000) # Wifi power saver trigger time (ms)
RAM_CLEANER_TIME = const(7500) # RAM Cleaner trigger time (ms)
WIFI_DISABLE_TIMEOUT = const(15000) # Timeout for disabling wifi if not connected
POWER_SAVE_TIMEOUT = const(15000) # Time to enter power saving after no activity
POWER_SAVER_TIME = const(1000) # Time to trigger ps loop (modules.powersaving)
IMU_CHECK_TIME = const(200) # IMU update time, in ms
IMU_STAY_TIME = const(1000) # IMU stay time, in ms, device needs to be in same rotatation for X ms to accept rotation as stable
NTP_SYNC_TIME = const(600000) # NTP automatic sync time in ms
LOOP_WAIT_TIME = const(0.025) # Time loops wait until starting again in seconds (Start, wait time, start)
DEBOUNCE_TIME = const(0.02) # Button check debounce time in seconds
DIAGNOSTIC_REFRESH_TIME = const(2000) # On-screen diagnostics (Voltage + CPU speed in menu)

# Boot settings
BOOT_ENABLE_RECOVERY = const(True)
BOOT_RECOVERY_PIN = const(0)
BOOT_ENABLE_UPDATES = const(False) # Enable searching for updates on boot
BOOT_UPDATE_PATH = const("/update.py")

# Post install config
POSTINSTALL_BLACKLIST = [
    'modules/rtc.py',
    'modules/rtc.mpy',
    'modules/mpu6886.py',
    'modules/mpu6886.mpy',
    'apps/metronome.py',
    'apps/metronome.mpy'
    ]   