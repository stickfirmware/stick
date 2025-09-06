# Buzzer Guide for Developers

Buzzer module is made to help developers play buzzer sounds.

> [!TIP]
> This will only work on devices with buzzer, please check HAS_BUZZER in os_constants. You can use speaker instead if device has it.

---

## API Reference

### `set_volume(volume: float)`

Sets buzzer duty (65536 * volume), max 1.0

---

### `play_sound(buzzer: PWM, freq: int, duration: float)`

Plays sound with a buzzer

> [!WARNING]
> This function is blocking, it will block your code for the time it plays sound!

**Example:**

```python
import modules.io_manager as io_man
import modules.buzzer as buzzer

buzzer = io_man.get("buzzer")
buzzer.set_volume(0.7)
buzzer.play_sound(buzzer, 356, 0.1) # Plays 356 freq for 0.1s on buzzer
```

---

### `play_sound_ms(buzzer: PWM, freq: int, duration: int)`

Play sound with a buzzer, duration in ms

> [!WARNING]
> This function is blocking, it will block your code for the time it plays sound!

---

### `startup_sound(buzzer: PWM)`

Plays startup sound with a buzzer, blocking, total duration: 0.7s

---