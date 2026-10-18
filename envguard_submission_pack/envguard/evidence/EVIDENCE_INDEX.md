# Evidence index (Track B)
Put these REAL files here. `python3 scripts/check_submission.py` verifies they exist.

| File | What it is | Where it comes from |
|---|---|---|
| frozen_requirements.(png/pdf/md) | The reviewed, FROZEN requirement set | Screenshot or export from FirmGen after you freeze |
| traceability_report.(pdf/html/md) | Requirement -> code -> tests | FirmGen traceability report export |
| uart_output.txt | Boot + readings + ALARM + FAULT lines | Copy from the FirmGen monitor / serial terminal |
| ble_scan.(png/jpg) | Phone BLE scanner showing "EnviroGuard" | nRF Connect screenshot |
| wiring_photo.(png/jpg) | The real board and wiring | Phone photo |
| telemetry_monitor.(png/jpg) | RTOS / System Monitor live (only if claiming Live Intelligence) | FirmGen Live Intelligence panel |
| ../demo/board_demo.mp4 (or a link in facts.json) | Video of the real board doing the acceptance tests | Phone recording |
| ../firmware/ | The FirmGen project (CMakeLists.txt, main/, tests) | Pushed via FirmGen's Git view |
