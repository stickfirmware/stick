# Database of SONY IR codes

# If you would like to help, please make a PR with new IR codes!
# Or you can just test the codes, open issue to help!
# I plan to compress this list so it doesnt take much space

# Format:
# (code, bits) # Device name
# code in format of "0xA50"
# bits as an int

# Source:
# https://tasmota.github.io/docs/Codes-for-IR-Remotes/
# https://github.com/lepiaf/IR-Remote-Code

# Supported devices:
# TVs:
# Sony TV (Untested)
# Sound / Amplifiers:
# Sony BD/DVD Players (Untested)
# Sony Chaine HiFi (Untested)


power = [
    (0xA90, 12), # Sony TV
    (0xA8B47, 20), # Sony BD/DVD Players
    (0xA81, 12) # Sony Chaine HiFi
]

vol_up = [
    (0x490, 12), # Sony TV / Sony BD/DVD Players
    (0x481, 12) # Sony Chaine HiFi
]

vol_down = [
    (0xC90, 12), # Sony TV / Sony BD/DVD Players
    (0xC81, 12) # Sony Chaine HiFi
]

mute = [
    (0x290, 12), # Sony TV / Sony BD/DVD Players
    (0xA81, 12) # Sony Chaine HiFi
]

prog_up = [
    (0x090, 12), # Sony TV
    (0x38B47, 20), # Sony TV / Sony BD/DVD Players (Forward)
    (0x8CB9C, 20) # Sony Chaine HiFi (Track next)
]

prog_down = [
    (0x890, 12), # Sony TV
    (0xEAB47, 20), # Sony TV / Sony BD/DVD Players (Forward)
    (0xCB9C, 20) # Sony Chaine HiFi (Track down)
]

# Only for projectors
freeze = [
]
