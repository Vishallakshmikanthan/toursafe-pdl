# TourSafe Hardware Prototype

ESP32 DevKit V1 or Raspberry Pi Pico W prototype for physical validation.

## Components

- ESP32 / RPi Pico W
- MPU6050 IMU
- NEO-6M GPS
- RGB LED + buzzer
- Push button (SOS)
- 18650 Li-ion battery + TP4056

## Responsibilities

- 50Hz IMU polling.
- 1Hz GPS polling.
- A_mag computation.
- Telemetry transmission or offline buffering.
- Status indication via LED/buzzer.
- Manual SOS trigger.

## Spec

See [docs/15_HARDWARE_INTEGRATION.md](../TriArch_IDL_TourSafe/docs/15_HARDWARE_INTEGRATION.md).
