# Stick firmware
Small stick but powerful beast.

![GitHub License](https://img.shields.io/github/license/stickfirmware/stick?label=License)
![GitHub repo size](https://img.shields.io/github/repo-size/stickfirmware/stick?label=Repo%20size)
![GitHub last commit](https://img.shields.io/github/last-commit/stickfirmware/stick?label=Last%20commit)
![GitHub Repo stars](https://img.shields.io/github/stars/stickfirmware/stick?style=flat&label=Stars)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/stickfirmware/stick/build.yml?style=flat&label=Build)
![GitHub Release](https://img.shields.io/github/v/release/stickfirmware/stick?label=Release)
[![Crowdin](https://badges.crowdin.net/stick-firmware/localized.svg)](https://crowdin.com/project/stick-firmware)

## Features
- Clock with i2c RTC sync
- Screen auto-rotate by IMU
- Custom and built in apps
- Music player (For devices with speaker)
- File explorer and reader
- SD Card support
- Lightsleep support

## Supported devices
- M5StickC Plus 2 (Button A - Confirm, B - Cycle, C - Cancel/Exit)
- Cardputer (Enter - Confirm, Tab - Cycle, ESC - Cancel/Exit

## Milestones
- [X] IMU Support
- [X] Refactor code
- [X] Better power saving
- [ ] Bluethooth support
- [ ] Autoupdate
- [X] Better SD card support
- [ ] More translations

## Links
- YouTube tutorials for Stick firmware - https://kitki30.tk/tutorials

## Translations
Please help us translate Stick firmware in [Crowdin](https://crowdin.com/project/stick-firmware)
If your language is not here, please open a github issue.

Currently supported languages:
- English (Source language, 100%)
- Polish (@Kitki30, 100%)

### Known issues with translations
Currently there are some issues with translations that you must know before translating anything:
- Our font only supports english characters (Won't fix, please try swaping some letters to work with font (ex. "ł" to "l"), but try to make it human readable. We are aware that some languages may not be possible to display using only english characters, but there is no way to fix it staying on the same font)

## Instalation
We need to add an installer later

1. Install micropython with esp_tool, thonny or M5Burner (Make sure to download correct version!)
2. Copy the files from **src** directory, using thonny (with files view) or something else
3. Reboot and done!
