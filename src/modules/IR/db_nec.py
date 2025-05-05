# Database of nec IR codes

# If you would like to help, please make a PR with new IR codes!
# Or you can just test the codes, open issue to help!
# I plan to compress this list so it doesnt take much space

# Format:
# (address, code) # Device name

# Source:
# https://gitlab.com/-/snippets/1690600
# https://tasmota.github.io/docs/Codes-for-IR-Remotes/
# https://gist.github.com/DDRBoxman/c68b68e41a47338496ba8cbd1bb5d20e

# Supported devices:
# TVs:
# LG TV (Tested)
# Generic TV (Untested)
# TLC TV Nec version (Untested, Partial support)
# Projectors:
# Acer Projector (Untested)
# Sanyo Projector (Untested)
# Soundbars / Amplifiers & Receivers:
# Soundcore Soundbar (Untested)
# JBL On Air 2.4G Control (Untested)

# Address List:
a_LGTV = 0x20DF
a_GENERICTV = 0x00FE
a_ACERKPROJ = 0x10C8
a_SANYOPROJ = 0xCC00
a_TLCNECTV = 0x57E3
a_SOUNDCORE = 0xFD25
a_JBLONAIR = 0x5385
a_SHARPTV = 0x20DF

power = [
    (a_LGTV, 0x10EF), # LG TV
    (a_GENERICTV, 0xA857), # Generic TV
    (a_TLCNECTV, 0xE817), # TLC TV
    (a_SHARPTV, 0x10EF), # Sharp TV
    (a_ACERKPROJ, 0xE11E), # Acer K132 Projector
    (a_SANYOPROJ, 0x00FF), # Sanyo Projector
    (a_SOUNDCORE, 0x02FD) # Soundcore Soundbar
]

vol_up = [
    (a_LGTV, 0x40BF), # LG TV
    (a_GENERICTV, 0xD827), # Generic TV
    (a_TLCNECTV, 0xF00F), # TLC TV
    (a_SHARPTV, 0x40BF), # Sharp TV
    (a_ACERKPROJ, 0xC639), # Acer K132 Projector
    (a_SOUNDCORE, 0x6897), # Soundcore Soundbar
    (a_JBLONAIR, 0x21DE) # JBL On Air Soundbar
]

vol_down = [
    (a_LGTV, 0xC03F), # LG TV
    (a_GENERICTV, 0x58A7), # Generic TV
    (a_TLCNECTV, 0x04FB), # TLC TV
    (a_SHARPTV, 0xC03F), # Sharp TV
    (a_ACERKPROJ, 0x26D9), # Acer K132 Projector
    (a_SOUNDCORE, 0x58A7), # Soundcore Soundbar
    (a_JBLONAIR, 0x20DF) # JBL On Air Soundbar
]

mute = [
    (a_LGTV, 0x906F), # LG TV
    (a_GENERICTV, 0x6897), # Generic TV
    (a_TLCNECTV, 0x08F7), # TLC TV
    (a_SHARPTV, 0x906F), # Sharp TV
    (a_ACERKPROJ, 0x8679), # Acer K132 Projector
    (a_SOUNDCORE, 0x18E7), # Soundcore Soundbar
    (a_JBLONAIR, 0x23DC) # JBL On Air Soundbar
]

prog_up = [
    (a_LGTV, 0x00FF), # LG TV
    (a_GENERICTV, 0x9867), # Generic TV
    (a_SHARPTV, 0x00FF), # Sharp TV
    (a_SOUNDCORE, 0x0AF5) # Soundcore Soundbar
]

prog_down = [
    (a_LGTV, 0x807F), # LG TV
    (a_GENERICTV, 0x18E7), # Generic TV
    (a_SHARPTV, 0x807F), # Sharp TV
    (a_SOUNDCORE, 0x8A75) # Soundcore Soundbar
]

# Only for projectors
freeze = [
    (a_ACERKPROJ, 0x718E) # Acer K132 Projector
]