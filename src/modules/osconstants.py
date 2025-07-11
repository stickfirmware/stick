# GPIO
BUZZER_PIN = 2
HOLD_PIN = 4
BUTTON_A_PIN = 37
BUTTON_B_PIN = 39
BUTTON_C_PIN = 35

### Shared I2C (RTC + IMU)
I2C_SLOT = 0 # I2C Slot???, can be 0 or 1 depending on the pins
I2C_SDA = 21
I2C_SCL = 22

# st7789
LCD_SPI_SLOT = 1 # Something like with I2C, 0 or 1
LCD_SPI_BAUD = 31250000 
LCD_SPI_SCK=13
LCD_SPI_MOSI=15
LCD_SPI_MISO = None # Leave it None, does nothing
LCD_SPI_CS = 5
LCD_DC = 14
LCD_RESET = 12
LCD_BL = 27
LCD_BL_FREQ = 1000 # Backlight frequency, higher values may not work
LCD_HEIGHT = 135 # LCD Height in pixels
LCD_WIDTH = 240 # LCD Width in pixels
LCD_ROTATIONS = {
    "BUTTON_LEFT": 3,
    "BUTTON_RIGHT": 1,
    "BUTTON_UPPER": 2,
    "BUTTON_BOTTOM": 0
    }
IMU_ROTATE_THRESHOLD = 0.9 # IMU Sensitivity
LCD_POWER_SAVE_BL = 0.3 # Backlight brightness on power saving

# MCU Frequencies
ULTRA_FREQ = 240 * 1000000 # Ultra fast, used for renders
FAST_FREQ = 160 * 1000000 # Fast
BASE_FREQ = 80 * 1000000 # Basic, used in loops
SLOW_FREQ = 40 * 1000000
ULTRA_SLOW_FREQ = 20 * 1000000

# Networking
WIFI_DEF_HOST = "Stick" # Default WLAN hostname

# Loop timings
WIFI_DISABLE_TIMEOUT = 15 * 1000 # Timeout for disabling wifi if not connected
POWER_SAVE_TIMEOUT = 15 * 1000 # Time to enter power saving after no activity
IMU_CHECK_TIME = 200 # IMU update time, in ms
IMU_STAY_TIME = 1000 # IMU stay time, in ms, device needs to be in same rotatation for X ms to accept rotation as stable
NTP_SYNC_TIME = 600000 # NTP automatic sync time in ms

# Others
EMERG_BUFF_SIZE = 1000 # Emergency buffer allocation size in bytes