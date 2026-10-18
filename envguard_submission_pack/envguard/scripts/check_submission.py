#!/usr/bin/env python3
"""Pre-submission gate. Exits non-zero if required real evidence is missing."""
import glob, json, os, re, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
f = json.load(open(f"{R}/facts.json"))
errs, warns = [], []
def has(pat): return [p for p in glob.glob(f"{R}/{pat}") if os.path.getsize(p) > 0]
def need(label, pat):
    if not has(pat): errs.append(f"MISSING {label}: {pat}")

if not (has("firmware/CMakeLists.txt") or has("firmware/*/CMakeLists.txt") or has("firmware/main/*.c")):
    errs.append("MISSING firmware project (push the FirmGen project into firmware/ via FirmGen's Git view)")
need("frozen requirements", "evidence/frozen_requirements.*")
need("traceability report", "evidence/traceability_report.*")
need("wiring photo", "evidence/wiring_photo.*")
need("BLE scan screenshot", "evidence/ble_scan.*")
if not (has("demo/board_demo.mp4") or f.get("board_demo_video_url")):
    errs.append("MISSING board demo video (demo/board_demo.mp4 or board_demo_video_url in facts.json)")

u = f"{R}/evidence/uart_output.txt"
if not os.path.exists(u) or os.path.getsize(u) == 0:
    errs.append("MISSING evidence/uart_output.txt")
else:
    t = open(u, errors="ignore").read()
    if "BOOT_OK" not in t: errs.append("uart_output.txt has no BOOT_OK line (REQ-01)")
    if len(re.findall(r"^READ,\d+,", t, re.M)) < 5: errs.append("uart_output.txt needs at least 5 READ lines (REQ-03)")
    if "ALARM" not in t: warns.append("uart_output.txt has no ALARM line (REQ-04 evidence)")
    if "FAULT" not in t: warns.append("uart_output.txt has no FAULT line (REQ-08 evidence)")
if f.get("telemetry_enabled"):
    need("telemetry monitor screenshot (Live Intelligence)", "evidence/telemetry_monitor.*")

if not f.get("repo_url"): errs.append("repo_url empty in facts.json")
fin = f"{R}/docs/SUBMISSION_FINAL.md"
if not os.path.exists(fin): errs.append("Run scripts/build_description.py first")
elif "{{" in open(fin).read(): errs.append("SUBMISSION_FINAL.md has unfilled placeholders")

for w in warns: print("WARN:", w)
for e in errs: print("FAIL:", e)
if errs:
    print(f"\nNOT READY: {len(errs)} problem(s)."); sys.exit(1)
print("READY: all required evidence is present. Open the repo link in a private window, then submit.")
