# Finish in this order
1. FirmGen: freeze requirements, build, flash, run the 10 acceptance tests, export the traceability report.
2. Save into evidence/: frozen_requirements.*, traceability_report.*, uart_output.txt, ble_scan.*, wiring_photo.* (+ telemetry_monitor.* if claiming Live Intelligence).
3. Record the board demo with your phone: warm sensor, unplug/replug, mute button -> demo/board_demo.mp4 (or upload it and put the link in facts.json).
4. Push the FirmGen project with FirmGen's Git view; make sure firmware/ in your repo holds it. Upload this whole folder to the same repo (GitHub "Add file > Upload files" works). Videos over 25 MB: host elsewhere and link them.
5. Fill facts.json (team, sensor_model, repo_url, frozen_requirement_count, one pass/fail per requirement, telemetry_enabled).
6. python3 scripts/build_description.py
7. python3 scripts/check_submission.py   (must print READY)
8. Open the repo link in a private window. Submit at https://forms.gle/bnocK9CNLndiZLwf8 using docs/FORM_ANSWERS.md.
