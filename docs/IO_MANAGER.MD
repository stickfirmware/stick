# IO Manager Guide for Developers

IO Manager is a core firmware module that manages the hardware of the device.  

---

## Basic Hardware Initialized on Boot

> [!WARNING]
> Hardware may differ between devices! Always check `os_constants` before using any hardware.

| Device Name       | Returned Object / Class                        | Notes |
|------------------|-----------------------------------------------|-------|
| `tft`            | `ST7789` class from `/modules/st7789.py`     | TFT display, 240x135 |
| `button_X`       | `Pin` class or `buttonemu` from `/modules/cardputer_kb.py` | ``buttonemu`` only supports `.value()` |
| `clicker_btn`    | `buttonemu` class from `/modules/cardputer_kb.py` | Easter egg button |
| `rtc`            | External RTC class if supported              | Check device type before use |
| `mpu`            | IMU/MPU class if supported                   | Check device type before use |
| `power_hold`     | `Pin` class from `machine`                   | Keeps power on some M5Stack devices |
| `buzzer`         | `PWM` class from machine                     | Buzzer PWM pin, check device type before use |

---

## API Reference

### `get(name: str) -> HardwareObject`
Returns a hardware object for the given device name.

> [!TIP]
> Each device has its own handler, and the class can differ between devices. Handle them according to their methods/properties.

**Returns:**  
- A device-specific object depending on `name`.

**Example:**
```python
import modules.io_manager as io_man

tft = io_man.get("tft")
print(tft.width(), tft.height())

---

### `set(name: str, value: object)`

Set or override a device object in the IO Manager registry.

**Example:**

```python
import modules.io_manager as io_man

custom_rtc = RtcDriver()
io_man.set("rtc", custom_rtc)
```

---

### `clear()`

Clears the IO Manager registry.

> [!WARNING] 
> Not recommended – may break the system until a reboot.

---