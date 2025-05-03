# Database of Panasonic IR codes

# If you would like to help, please make a PR with new IR codes!
# Or you can just test the codes, open issue to help!
# I plan to compress this list so it doesnt take much space

# Format:
# (code) # Device name
# 48bit code in format of "0x40040100BCBD"

# Source:
# https://tasmota.github.io/docs/Codes-for-IR-Remotes/

# Supported devices:
# TVs:
# Panasonic TV (Untested)
# Soundbars / Amplifiers & Receivers:
# Panasonic Soundbar (Untested)


power = [
    (0x40040500BCB9), # Panasonic Soundbar
    (0x40040100BCBD) # Panasonic TV
]

vol_up = [
    (0x400405000401), # Panasonic Soundbar
    (0x400401000405) # Panasonic TV
]

vol_down = [
    (0x400405008481), # Panasonic Soundbar
    (0x400401008485) # Panasonic TV
]

mute = [
    (0x400405004C49), # Panasonic Soundbar
    (0x400401004C4D) # Panasonic TV
]

prog_up = [
    (0x400405383F02), # Panasonic Soundbar
    (0x400401002C2D) # Panasonic TV
]

prog_down = [
    (0x40040538BF82), # Panasonic Soundbar
    (0x40040100ACAD) # Panasonic TV
]

# Only for projectors
freeze = [
]

