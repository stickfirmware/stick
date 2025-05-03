from machine import Pin, I2C
import modules.UNIT.max30100 as max30100
import gc
import time

# === INIT I2C ===
sda = Pin(32)
scl = Pin(33)
i2c = I2C(0, scl=scl, sda=sda)

# === INIT SENSOR ===
sensor = max30100.MAX30100(
    i2c,
    mode=0x03,              # Heart rate + SpO2
    sample_rate=200,
    led_current_red=17.4,
    led_current_ir=17.4,
)

# === FILTER: moving average ===
def moving_average(data, window_size=5):
    result = []
    for i in range(len(data)):
        window = data[max(0, i - window_size + 1):i + 1]
        result.append(sum(window) / len(window))
    return result

def check():
    samples_ir = []
    samples_red = []
    sample_count = 200
    timestamps = []

    for _ in range(sample_count):
        sensor.read_sensor()
        samples_ir.append(sensor.ir)
        samples_red.append(sensor.red)
        timestamps.append(time.ticks_ms())
        time.sleep_ms(10)

    # === FILTERING ===
    samples_ir = moving_average(samples_ir)
    samples_red = moving_average(samples_red)

    # === AC/DC COMPONENTS ===
    dc_ir = sum(samples_ir) / len(samples_ir)
    dc_red = sum(samples_red) / len(samples_red)

    ac_ir = max(samples_ir) - min(samples_ir)
    ac_red = max(samples_red) - min(samples_red)

    # === SPO2 ===
    if dc_ir != 0 and dc_red != 0 and ac_ir != 0:
        ratio = (ac_red / dc_red) / (ac_ir / dc_ir)
        spo2_value = 110 - 25 * ratio
        spo2_value = max(0, min(spo2_value, 100))
    else:
        spo2_value = 0

    # --- BPM ---
    threshold = max(samples_ir) * 0.8
    MIN_AC_AMPLITUDE = 500
    MIN_PEAK_INTERVAL = 400  # ms
    bpm = 0

    if ac_ir < MIN_AC_AMPLITUDE:
        print("Sygnał za słaby, nie liczę BPM")
    else:
        peaks = []
        for i in range(1, len(samples_ir) - 1):
            if samples_ir[i-1] < samples_ir[i] and samples_ir[i] > samples_ir[i+1] and samples_ir[i] > threshold:
                if not peaks or (time.ticks_diff(timestamps[i], peaks[-1]) > MIN_PEAK_INTERVAL):
                    peaks.append(timestamps[i])

        if len(peaks) >= 2:
            intervals = [time.ticks_diff(peaks[i+1], peaks[i]) for i in range(len(peaks)-1)]
            avg_interval = sum(intervals) / len(intervals)
            bpm = 60000 / avg_interval

    # Minimalny SpO2
    if spo2_value < 90:
        spo2_value = 90  # Ignoruj wartości poniżej 90%

    gc.collect()
    return (str(round(spo2_value)), str(round(bpm)))
