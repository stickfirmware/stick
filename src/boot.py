import machine

import modules.os_constants as osc

# Hold power
if osc.HAS_HOLD_PIN:
    power_hold = machine.Pin(osc.HOLD_PIN, machine.Pin.OUT)
    power_hold.value(1)
    
import modules.buzzer as buzz
if osc.HAS_BUZZER:
    buzzer = machine.PWM(machine.Pin(osc.BUZZER_PIN), duty_u16=0, freq=500)
    buzz.set_volume(0.1)
    buzz.play_sound(buzzer, 2000, 0.0125)