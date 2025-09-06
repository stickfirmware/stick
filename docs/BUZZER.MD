# Buzzer Guide for Developers

Buzzer module is made to help developers play buzzer sounds.

> [!TIP]
> This will only work on devices with buzzer, please check HAS_BUZZER in os_constants. You can use speaker instead if device has it.

---

## API Reference

### `get(name: str) -> HardwareObject`
Returns a hardware object for the given device name.

**Returns:**  
- A device-specific object depending on `name`.

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

> [!TIP]
> Each device has its own handler, and the class can differ between devices. Handle them according to their methods/properties.

**Example:**
```python
import modules.io_manager as io_man

tft = io_man.get("tft")
print(tft.width(), tft.height())
