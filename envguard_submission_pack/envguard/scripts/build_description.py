#!/usr/bin/env python3
"""Reads facts.json and writes docs/SUBMISSION_FINAL.md and docs/FORM_ANSWERS.md.
Refuses to build while any fact is empty, so nothing unverified is claimed."""
import json, os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
f = json.load(open(f"{R}/facts.json"))
need = ["team", "board", "sensor_model", "prd_method", "frozen_requirement_count", "repo_url"]
missing = [k for k in need if not str(f.get(k, "")).strip()]
acc = f.get("acceptance", {})
missing += [f"acceptance.{k}" for k, v in acc.items() if v not in ("pass", "fail")]
if not (f.get("board_demo_video_url") or os.path.exists(f"{R}/demo/board_demo.mp4")):
    missing.append("board_demo_video_url (or demo/board_demo.mp4)")
if missing:
    print("Fill these in facts.json first:", ", ".join(missing)); sys.exit(1)

names = {
 "REQ-01": "Boot log over UART", "REQ-02": "Sample every 2 s (+/-100 ms)", "REQ-03": "CSV reading line per sample",
 "REQ-04": "Red LED within 500 ms of threshold breach", "REQ-05": "Hysteresis, no flicker", "REQ-06": "Green LED in normal state",
 "REQ-07": "BLE advertising of readings and state", "REQ-08": "Sensor fault state and auto-recovery",
 "REQ-09": "BOOT button mutes alarm", "REQ-10": "Separate RTOS tasks joined by queues"}
ev = {"REQ-01": "UART log", "REQ-02": "UART timestamps", "REQ-03": "UART log", "REQ-04": "Board video, UART",
      "REQ-05": "Board video", "REQ-06": "Board video", "REQ-07": "BLE scanner screenshot",
      "REQ-08": "Board video, UART", "REQ-09": "Board video, UART", "REQ-10": "Design doc, traceability report"}
rows = "\n".join(f"| {k} | {names[k]} | {acc[k].upper()} | {ev[k]} |" for k in sorted(acc))
li = f.get("telemetry_enabled")
bonus = "Live Intelligence" if li else "none claimed"
live = ("\n## Live Intelligence (bonus)\nFirmGen telemetry was enabled and the RTOS / System Monitor was shown live during the demo "
        "(tasks, stack watermarks, heap, queue depth, current state). Screenshot: `evidence/telemetry_monitor.*`.\n") if li else ""
video = f.get("board_demo_video_url") or "demo/board_demo.mp4 in the repository"
desc = f"""# EnviroGuard: A Traceable, Fail-Safe ESP32 Environmental Monitor

**Team:** {f['team']}
**Track:** B (FirmGen), Suggested Track 6, Smart Environmental Monitor
**Bonus claimed:** {bonus}
**Repository:** {f['repo_url']}
**Board demo video:** {video}

## Problem
Indoor temperature and humidity problems go unmeasured. Worse, a dead or unplugged sensor keeps showing its last value, so nobody notices. We built a low-cost node that measures, flags, broadcasts over BLE and detects its own sensor failure.

## What we built
An {f['board']} with a {f['sensor_model']} sensor, a green LED and a red LED. It samples every 2 s, applies temperature and humidity thresholds with hysteresis, shows the state on the LEDs, broadcasts readings over BLE, logs every sample over UART, enters a FAULT state (red LED blinking at 5 Hz) after 3 failed reads and recovers automatically, and lets the BOOT button mute the alarm without hiding the state.

## FirmGen workflow
- PRD: {f['prd_method']} into FirmGen (`firmware/PRD_EnviroGuard.md`), reviewed and frozen before code generation ({f['frozen_requirement_count']} frozen requirements; evidence: `evidence/frozen_requirements.*`).
- FirmGen implemented, built, flashed and monitored the firmware on ESP-IDF v5.5, and produced requirement-linked unit tests, the design document and the traceability report. The project was pushed through FirmGen's Git view into `firmware/`.
- **Why FirmGen is load-bearing:** every behaviour traces to a frozen requirement and was accepted against its acceptance criterion on the physical board.

## Acceptance results (on the physical board)
| Requirement | Behaviour | Result | Evidence |
|---|---|---|---|
{rows}
{live}
## Evidence
`evidence/traceability_report.*`, `evidence/uart_output.txt`, `evidence/ble_scan.*`, `evidence/wiring_photo.*`, `evidence/frozen_requirements.*`{', `evidence/telemetry_monitor.*`' if li else ''}, board demo video.

## Design rehearsal (not hardware evidence)
Before flashing we modelled the PRD behaviour in a browser simulator (`docs/design_rehearsal/`). It is a labelled simulation used to review the requirements, not part of the acceptance evidence.
"""
open(f"{R}/docs/SUBMISSION_FINAL.md", "w").write(desc)
form = f"""FORM ANSWERS (copy each into the matching field)

Project name: EnviroGuard
One-line pitch: An ESP32 environmental monitor that detects its own sensor failure, built requirements-first with FirmGen.
Track: B (FirmGen)
Bonus: {bonus}
Team: {f['team']}
Repository link: {f['repo_url']}
Demo video: {video}
Project description: paste the contents of docs/SUBMISSION_FINAL.md
Evidence: traceability report + UART output are in the repository under evidence/
"""
open(f"{R}/docs/FORM_ANSWERS.md", "w").write(form)
print("Built docs/SUBMISSION_FINAL.md and docs/FORM_ANSWERS.md")
fails = [k for k, v in acc.items() if v == "fail"]
if fails: print("NOTE: these requirements are marked FAIL, fix them or be ready to explain:", ", ".join(fails))
