# PRD: EnviroGuard, ESP32 Environmental Monitor with BLE and Fail-Safe Alerts

## 1. Purpose
Indoor temperature and humidity problems go unmeasured. EnviroGuard is a low-cost ESP32 node that
samples a sensor, flags threshold violations on LEDs, broadcasts readings over BLE, and logs everything
over UART. It must detect and report a failed sensor instead of showing stale data.

## 2. Hardware (confirm exact parts at the hardware desk)
- ESP32 dev board (BLE required; do NOT use the STM32 boards, they have no BLE), USB cable
- Temperature + humidity sensor from the kit (e.g. DHT22, SHT3x, or BME280; I2C or single-wire)
- Green LED + resistor on GPIO 5 (GPIO_OK_LED)
- Red LED + resistor on GPIO 2 (GPIO_ALARM_LED)
- Onboard BOOT button on GPIO 0 (GPIO_MUTE_BTN)

## 3. Configuration (menuconfig / Kconfig, no magic numbers in code)
- SAMPLE_PERIOD_MS = 2000
- TEMP_HIGH_C = 30.0 (lower to 28.0 for demo), HUMIDITY_HIGH_PCT = 70.0
- HYSTERESIS_C = 1.0, HYSTERESIS_PCT = 3.0
- SENSOR_FAIL_LIMIT = 3 consecutive failed reads

## 4. Functional requirements
| ID | Requirement | Acceptance criterion |
|----|-------------|----------------------|
| REQ-01 | At boot, log firmware version, configured thresholds and "BOOT_OK" over UART at 115200 baud | UART shows BOOT_OK within 3 s of reset |
| REQ-02 | Read temperature and humidity every SAMPLE_PERIOD_MS (+/-100 ms) | UART timestamps of consecutive readings differ by 2000 +/- 100 ms |
| REQ-03 | Log each reading as one line: `READ,<uptime_ms>,<temp_c>,<hum_pct>,<state>` | UART shows one CSV line per sample |
| REQ-04 | If temperature >= TEMP_HIGH_C or humidity >= HUMIDITY_HIGH_PCT, turn the red LED on and the green LED off within 500 ms of the sample | Warm the sensor (finger, hairdryer on low) or breathe on it; red LED on, UART state=ALARM |
| REQ-05 | Apply hysteresis: return to normal only after the value drops below threshold minus hysteresis | No LED flicker when the value hovers near the threshold |
| REQ-06 | In normal state, green LED on and red LED off | Visible at idle |
| REQ-07 | Advertise over BLE with device name "EnviroGuard", exposing temperature, humidity and state, updated every sample | BLE scanner app (e.g. nRF Connect) shows the name and changing values |
| REQ-08 | If SENSOR_FAIL_LIMIT consecutive reads fail, enter FAULT: blink red LED at 5 Hz, log `FAULT,sensor_read_failed`, set BLE state=FAULT, and keep retrying; recover automatically when reads succeed | Unplug the sensor: red blinks, UART FAULT; replug: returns to normal |
| REQ-09 | Pressing the BOOT button mutes (turns off) the red LED while in ALARM; the alarm state is still logged and broadcast; mute clears when the state returns to normal | Press button in ALARM: LED off, UART still shows state=ALARM |
| REQ-10 | Sensor reading and state logic must run in separate RTOS tasks connected by a queue (sensor task, logic task, BLE task) | Design doc shows task/queue structure |

## 5. Non-functional
- No hardcoded secrets; build with ESP-IDF v5.5
- Unit tests for: threshold logic, hysteresis, fault counter, CSV line formatting
- Stack usage and heap free visible via telemetry

## 6. Live Intelligence (bonus)
Enable FirmGen telemetry. During the demo show: task list with stack watermarks, free heap, queue depth,
current state, and last reading in the RTOS / System Monitor, updating live while the sensor is warmed.

## 7. Out of scope
Wi-Fi/MQTT, OTA, display, deep sleep.
