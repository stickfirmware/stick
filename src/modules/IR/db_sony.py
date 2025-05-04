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

# Supported devices:
# TVs:
# Sony TV (Untested)
# Sound / Amplifiers:
# Sony BD/DVD Players (Untested)



power = [
    (0xA90, 12), # Sony TV
    (0xA8B47, 20) # Sony BD/DVD Players
]

vol_up = [
    (0x490, 12) # Sony TV / Sony BD/DVD Players
]

vol_down = [
    (0xC90, 12) # Sony TV / Sony BD/DVD Players
]

mute = [
    (0x290, 12) # Sony TV / Sony BD/DVD Players
]

prog_up = [
    (0x090, 12) # Sony TV
]

prog_down = [
    (0x890, 12) # Sony TV
]

# Only for projectors
freeze = [
]
