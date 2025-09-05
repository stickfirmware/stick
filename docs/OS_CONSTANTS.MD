# OS Constants module
OS Constants provides all the info about the device, it is located in ``/modules/os_constants.py`` and should not be changed during runtime.

## Device info
| Constant     | Type | Example                  | Description                                                             |
|--------------|------|--------------------------|-------------------------------------------------------------------------|
| DEVICE_NAME  | str  | "M5Stack Cardputer v1.1" | Human readable device name                                              |
| RELEASE_NAME | str  | "cardputerv1_1"           | Name in builder, make sure it is sanitized to work with all filesystems |

## Debug
| Constant                | Type | Example | Description                                                                      |
|-------------------------|------|---------|----------------------------------------------------------------------------------|
| ENABLE_DEBUG_PRINTS     | bool | False   | Debug prints                                                                     |
| LESS_RAM_CLEANER_OUTPUT | bool | True    | Disable ram cleaner output, if debug prints are disabled, it also works as False |

## Power managament
| Constant     | Type | Example | Description                                        |
|--------------|------|---------|----------------------------------------------------|
| HAS_HOLD_PIN | bool | False   | True if device has power hold pin, like in M5Stack |
| HOLD_PIN     | int  | 12      | If has hold pin, this is Pin number of it          |
| BATTERY_ADC  | int  | 10      | Pin number of battery voltage pin                  |

## Sound
| Constant      | Type | Example | Description                           |
|---------------|------|---------|---------------------------------------|
| HAS_MIC       | bool | True    | True if device has microphone.        |
| MIC_DATA      | int  | 46      | Microphone data pin number            |
| MIC_CLK       | int  | 43      | Microphone clk pin number             |
| HAS_SPEAKER   | bool | True    | True if device has speaker            |
| SPEAKER_BCLK  | int  | 41      | Speakers I2S Bit clock pin num        |
| SPEAKER_SDATA | int  | 42      | Speakers I2S Serial data pin num      |
| SPEAKER_LRCLK | int  | 43      | Speakers I2S Left/Right Clock pin num |

## SD Card
| Constant    | Type | Example    | Description                              |
|-------------|------|------------|------------------------------------------|
| HAS_SD_SLOT | bool | True       | True if device has built in SD Card slot |
| SD_CS       | int  | 12         | SD Card Chip Select pin num              |
| SD_MOSI     | int  | 14         | SD Card MOSI pin num                     |
| SD_MISO     | int  | 39         | SD Card MISO pin num                     |
| SD_CLK      | int  | 40         | SD Card CLK pin num                      |
| SD_FREQ     | int  | 10_000_000 | SD Card SPI frequency                    |

## IR
| Constant             | Type      | Example  | Description                                   |
|----------------------|-----------|----------|-----------------------------------------------|
| IR_PIN               | int       | 44       | IR receiver pin num                           |
| IR_ALLOWED_PINS      | list[int] | [1,2,44] | IR pin selector allowed pins                  |
| IR_SENDING_WAIT_TIME | float     | 0.3      | Delay between sending IR protocols in seconds |
| ALLOW_IR_RECORD      | bool      | False    | True if device has IR receiver                |
| IR_RECORD_PIN        | int       | 26       | IR receiver pin                               |

## Input methods
| Constant             | Type      | Example  | Description                                                                                                  |
|----------------------|-----------|----------|--------------------------------------------------------------------------------------------------------------|
| INPUT_METHOD         | int       | 2        | 1 - Standard (3 Buttons, Exit, Cycle, Select, used in sticks), 2 - Cardputer (Input over cardputer keyboard) |
| IR_ALLOWED_PINS      | list[int] | [1,2,44] | IR pin selector allowed pins                                                                                 |
| IR_SENDING_WAIT_TIME | float     | 0.3      | Delay between sending IR protocols in seconds                                                                |
| ALLOW_IR_RECORD      | bool      | False    | True if device has IR receiver                                                                               |

## GROVE
| Constant      | Type | Example | Description            |
|---------------|------|---------|------------------------|
| HAS_GROVE     | bool | True    | True if has grove port |
| GROVE_SLOT    | int  | 1       | I2C slot of grove port |
| GROVE_YELLOW  | int  | 2       | Grove yellow cable pin |
| GROVE_WHITE   | int  | 1       | Grove white cable pin  |

## Shared I2C
| Constant       | Type | Example | Description                                 |
|----------------|------|---------|---------------------------------------------|
| HAS_SHARED_I2C | bool | True    | True if has shared I2C (For RTC, IMU, etc.) |
| HAS_RTC        | bool | True    | True if has RTC (On shared I2C)             |
| HAS_IMU        | bool | True    | True if has IMU (On shared I2C)             |
| I2C_SLOT       | int  | 0       | I2C Slot                                    |
| I2C_SDA        | int  | 21      | Shared I2C SDA                              |
| I2C_SCL        | int  | 22      | Shared I2C SCL                              |\

## LCD
| Constant               | Type    | Default      | Description                           |
| ---------------------- | ------- | ------------ | ------------------------------------- |
| LCD_LOAD_BG          | int   | 0          | Loading screen background color       |
| LCD_LOAD_TEXT     | int   | 65535      | Loading screen text color             |
| LCD_SPI_SLOT         | int   | 1          | SPI slot used                         |
| LCD_SPI_BAUD         | int   | 26_000_000 | SPI frequency                    |
| LCD_SPI_SCK          | int   | 36         | SPI clock pin                         |
| LCD_SPI_MOSI         | int   | 35         | SPI MOSI pin                          |
| LCD_SPI_MISO         | None  | None       | SPI MISO pin (unused)                 |
| LCD_SPI_CS           | int   | 37         | SPI chip select                       |
| LCD_DC               | int   | 34         | Data/Command pin                      |
| LCD_RESET            | int   | 33         | Reset pin                             |
| LCD_BL               | int   | 38         | Backlight pin                         |
| LCD_BL_FREQ          | int   | 1000       | Backlight frequency (Hz)              |
| LCD_HEIGHT           | int   | 135        | Screen height (pixels)                |
| LCD_WIDTH            | int   | 240        | Screen width (pixels)                 |
| LCD_ROTATIONS        | dict  | {...}        | Rotation mapping for buttons & screen |
| IMU_ROTATE_THRESHOLD | float | 0.9        | IMU sensitivity                       |
| LCD_POWER_SAVE_BL    | float | 0.3        | Backlight brightness in power saving  |

## MCU Frequencies
| Constant          | Type  | Default       | Description            |
| ----------------- | ----- | ------------- | ---------------------- |
| ULTRA_FREQ      | int | 240_000_000 | Ultra fast (rendering) |
| FAST_FREQ       | int | 160_000_000 | Fast                   |
| BASE_FREQ       | int | 80_000_000  | Basic (loops)          |
| SLOW_FREQ       | int | 40_000_000  | Power-saving mode      |
| ULTRA_SLOW_FREQ | int | 20_000_000  | Extreme power saving   |

## Networking
| Constant             | Type  | Default                      | Description                      |
| -------------------- | ----- | ---------------------------- | -------------------------------- |
| WIFI_DEF_HOST      | str | "Cardputer"                | Default Wi-Fi hostname           |
| REQUESTS_USERAGENT | str | "Stick firmware/Cardputer" | User agent for requests module |

## Loop timings
| Constant                  | Type    | Default   | Description                     |
| ------------------------- | ------- | --------- | ------------------------------- |
| WIFI_PWR_SAVER_TIME     | int   | 15000   | Wi-Fi power saver trigger       |
| RAM_CLEANER_TIME        | int   | 7500    | RAM cleaner trigger             |
| WIFI_DISABLE_TIMEOUT    | int   | 15000   | Timeout to disable Wi-Fi        |
| POWER_SAVE_TIMEOUT      | int   | 15000   | Time to enter power-saving      |
| POWER_SAVER_TIME        | int   | 1000    | Power-saving loop interval      |
| IMU_CHECK_TIME          | int   | 200     | IMU update interval             |
| IMU_STAY_TIME           | int   | 1000    | IMU stability duration          |
| NTP_SYNC_TIME           | int   | 600_000 | NTP sync interval               |
| LOOP_WAIT_TIME          | float | 0.025   | Loop wait time in seconds       |
| DEBOUNCE_TIME           | float | 0.02    | Button debounce time in seconds |
| DIAGNOSTIC_REFRESH_TIME | int   | 2000    | Diagnostic screen refresh       |

## Boot settings
| Constant               | Type   | Default        | Description                  |
| ---------------------- | ------ | -------------- | ---------------------------- |
| BOOT_ENABLE_RECOVERY | bool | True         | Enable recovery mode button |
| BOOT_RECOVERY_PIN    | int  | 0            | Pin to trigger recovery      |
| BOOT_ENABLE_UPDATES  | bool | False        | Search for updates on boot   |
| BOOT_UPDATE_PATH     | str  | "/update.py" | Update script path           |

## Post-install config
| Constant                | Type        | Default | Description                      |
| ----------------------- | ----------- | ------- | -------------------------------- |
| POSTINSTALL_BLACKLIST | list[str] | [...] | Files deleted in post-install |