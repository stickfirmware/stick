print("Kitki30 Boot")

class FakeST:
    def text(self, *k):
        return None
    def fill(self, *k):
        return None

import machine, time
import os
machine.freq(240000000)

import boot_settings as setting
secureboot = setting.SECURE_BOOT

# Hold power
print("\nEnable hold pin")
power_hold = machine.Pin(4, machine.Pin.OUT)
power_hold.value(1)

import modules.buzzer as buzz
buzzer = machine.PWM(machine.Pin(2), duty_u16=0, freq=500)
buzz.set_volume(0.1)
buzz.play_sound(buzzer, 2000, 0.0125)

print("Running starting scripts")
for i in setting.STARTING_SCRIPTS:
    exec(open(i).read())

print("Checking boot options...")

# Recovery button
RECOVERY_BTN_PIN = setting.RECOVERY_PIN

rbtn = machine.Pin(RECOVERY_BTN_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
recovery = rbtn.value() == 0

def gethash(file):
    import hashlib
    import binascii

    try:
        h = hashlib.md5()
        with open(file, "rb") as f:
            while True:
                chunk = f.read(512)
                if not chunk:
                    break
                h.update(chunk)
        digest = h.digest()
        return binascii.hexlify(digest).decode('utf-8')
    except Exception as e:
        return "Execution error:\n" + str(e)

try:
    print("Load fonts")
    import fonts.def_8x8 as f8x8

    # Init tft
    print("Init tft")
    import modules.st7789 as st7789
    tft = st7789.ST7789(
            machine.SPI(1, baudrate=31250000, sck=machine.Pin(13), mosi=machine.Pin(15), miso=None),
            135,
            240,
            reset=machine.Pin(12, machine.Pin.OUT),
            cs=machine.Pin(5, machine.Pin.OUT),
            dc=machine.Pin(14, machine.Pin.OUT),
            backlight=machine.PWM(machine.Pin(27), freq=1000),
            rotation=3)
    tft.fill(0)
    # 65535
    tft.text(f8x8, "Kitki30 Boot",0,0,2016)
except Exception as e:
    tft = FakeST()
    print(str(e))

tft.text(f8x8, "Checking boot options...",0,16,65535)

def recoveryf():
    tft.text(f8x8, "Secure boot = " + str(secureboot),0,32,65535)
    if secureboot == True:
        md5sum = gethash(setting.RECOVERY_PATH)
        tft.text(f8x8, "Veryfing file...",0,40,65535)
        if md5sum in setting.ALLOW_LIST:
            tft.text(f8x8, md5sum,0,40,2016)
            tft.text(f8x8, "Hash ok! Booting",0,48,2016)
        else:
            tft.text(f8x8, md5sum,0,40,63488)
            tft.text(f8x8, "Cannot verify the file!",0,48,63488)
            tft.text(f8x8, "Your device will not boot!",0,56,63488)
            time.sleep(1)
            while True:
                time.sleep(60)
    else:
        tft.text(f8x8, "Secure boot disabled!",0,40,63488)
    exec(open(setting.RECOVERY_PATH).read())

while True:
    if recovery and setting.ENABLE_RECOVERY == True:
        tft.text(f8x8, "Recovery",180,127,2016)
        print("Booting recovery")
        recovery = False
        recoveryf()
    elif setting.UPDATE_PATH in os.listdir("/") and setting.ENABLE_UPDATES:
        tft.text(f8x8, "Update script found! Booting..",0,24,65535)
        try:
            print("Update script found! Booting!")
            exec(open(setting.UPDATE_PATH).read())
            machine.soft_reset()
        except Exception as e:
            tft.text(f8x8, "Update failed! Rebooting..",0,32,65535)
            print(e)
            machine.soft_reset()
    else:
        try:
            tft.text(f8x8, "Booting MainOS, please wait!",0,24,65535)
            tft.text(f8x8, "Secure boot = " + str(secureboot),0,32,65535)
            if secureboot == True:
                md5sum = gethash(setting.MAINOS_PATH)
                tft.text(f8x8, "Veryfing file...",0,40,65535)
                if md5sum in setting.ALLOW_LIST:
                    tft.text(f8x8, md5sum,0,40,2016)
                    tft.text(f8x8, "Hash ok! Booting",0,48,2016)
                else:
                    tft.text(f8x8, md5sum,0,40,63488)
                    tft.text(f8x8, "Cannot verify the file!",0,48,63488)
                    tft.text(f8x8, "Your device will not boot!",0,56,63488)
                    time.sleep(1)
                    break
            else:
                tft.text(f8x8, "Secure boot disabled!",0,40,63488)
            print("Booting mainos")
            exec(open(setting.MAINOS_PATH).read())
        except Exception as e:
            print(e)
            tft.text(f8x8, "Booting failed!",0,80,63488)
            print("Booting mainos failed, booting recovery!")
            recoveryf()