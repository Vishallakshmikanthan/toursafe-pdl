# 15 — Hardware Integration

> Specification for the ESP32 / Raspberry Pi Pico W hardware prototype.

---

## 1. Purpose

The hardware prototype provides a tangible demonstration of TourSafe's core sensor-to-AI pipeline. It validates:
- High-frequency IMU data collection.
- GPS positioning.
- Crash and immobility detection.
- Offline buffering.
- Geo-fence breach detection.

---

## 2. Components

| Component | Model | Role |
|-----------|-------|------|
| Microcontroller | ESP32 DevKit V1 or Raspberry Pi Pico W | Edge compute, Wi-Fi, Bluetooth |
| IMU | MPU6050 | 3-axis accelerometer + gyroscope |
| GPS | NEO-6M | Latitude/longitude |
| Power | 18650 Li-ion + TP4056 | Portable rechargeable power |
| Feedback | RGB LED + active buzzer | Visual/audio status indication |
| Input | Momentary push button | Manual SOS override |

---

## 3. Wiring (ESP32)

| ESP32 Pin | Component | Pin |
|-----------|-----------|-----|
| 3.3V | MPU6050 | VCC |
| GND | MPU6050 | GND |
| GPIO21 | MPU6050 | SDA |
| GPIO22 | MPU6050 | SCL |
| 3.3V | NEO-6M | VCC |
| GND | NEO-6M | GND |
| GPIO16 (RX2) | NEO-6M | TX |
| GPIO17 (TX2) | NEO-6M | RX |
| GPIO18 | RGB LED | R (via resistor) |
| GPIO19 | RGB LED | G |
| GPIO23 | RGB LED | B |
| GPIO25 | Buzzer | + |
| GPIO26 | Button | one side |

---

## 4. Firmware Responsibilities

### Sensor Polling
- MPU6050: 50 Hz via I2C.
- NEO-6M: 1 Hz via UART.
- Compute A_mag locally.

### Wi-Fi / Backend
- Connect to configured Wi-Fi.
- Send telemetry windows to FastAPI WebSocket or HTTP endpoint.

### Offline Buffer
- If Wi-Fi disconnected, store windows in SPIFFS or SD card.
- Flush on reconnect.

### Status Indication
- Green: normal tracking.
- Amber: geo-fence breach.
- Red: confirmed anomaly / SOS.
- Buzzer: alert on SOS or geo-fence breach.

---

## 5. Software Stack

### ESP32
- Arduino Framework or ESP-IDF.
- Libraries: `Wire`, `TinyGPS++`, `WiFi`, `WebSocketsClient`, `ArduinoJson`, `FS`.

### Raspberry Pi Pico W
- MicroPython or Arduino-Pico.
- Libraries: `machine`, `network`, `umqtt` / `urequests`, `mpu6050`, `micropyGPS`.

---

## 6. Validation Tests

### Test 1: Crash Detection
- Subject device to sharp high-G impulse.
- Verify dashboard receives CRITICAL incident within 5 seconds.

### Test 2: Offline Buffer
- Disable Wi-Fi during session.
- Re-enable after 5 minutes.
- Verify queued telemetry flushes and timeline is complete.

### Test 3: Geo-Fence Breach
- Spoof or move GPS coordinates across a test fence.
- Verify amber alert on dashboard and buzzer/LED feedback.

### Test 4: Manual SOS
- Press button.
- Verify immediate CRITICAL incident.

---

## 7. Deliverables

- `hardware/firmware/` source code.
- Wiring diagram.
- Bill of materials.
- Validation test log.
- Demo script.
