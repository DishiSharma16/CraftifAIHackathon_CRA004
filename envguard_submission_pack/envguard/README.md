# EnviroGuard: Fail-Safe ESP32 Environmental Monitor
Embedded SF: CraftifAI Physical AI Hackathon, Track B (FirmGen).

An ESP32 node that samples temperature and humidity, flags thresholds on LEDs, advertises readings over BLE, and detects and reports its own sensor failure. Firmware was generated, built, flashed and traced with CraftifAI FirmGen from a frozen PRD.

## Repository map
| Path | Contents |
|---|---|
| `firmware/` | FirmGen project (pushed via FirmGen's Git view) and `PRD_EnviroGuard.md` |
| `evidence/` | Frozen requirements, traceability report, UART output, BLE scan, wiring photo, telemetry (see `EVIDENCE_INDEX.md`) |
| `demo/` | Board demo video, optional pitch video |
| `docs/SUBMISSION_FINAL.md` | The project description submitted to the form |
| `docs/design_rehearsal/` | Browser simulator and clip: a labelled rehearsal, NOT hardware evidence |
| `scripts/` | `build_description.py`, `check_submission.py` |

## Requirements
REQ-01 to REQ-10 are listed in `firmware/PRD_EnviroGuard.md`, with an acceptance criterion each.

## Reproduce
Open the project in FirmGen v0.4.1 (ESP-IDF v5.5), build, flash to an ESP32, open the monitor at 115200 baud.
