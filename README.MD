# Kitki30 Stick
Makes your stick a usefull EDC device
## Features
- Clock with i2c RTC sync
- Screen auto-rotate by IMU
- Custom and built in apps

## Supported devices
**M5StickC Plus2** is the only device supported, if M5Stack will release a new stick, i will probably try to port this firmware to it.

## Milestones
- [X] IMU Support
- [ ] Refactor code (In progress)
- [ ] Better power saving (In progress)
- [ ] Bluethooth support
- [ ] Autoupdate
- [ ] Better SD card support

## Supported UNIT modules
- CardKB for terminal

## Instalation
We need to add an installer later

1. Install micropython with esp_tool, thonny or M5Burner (v1.23.0 is the only tested version, make sure it has SPIRAM support)
2. Copy the files from **src** directory, using thonny (with files view) or something else
3. Done!
