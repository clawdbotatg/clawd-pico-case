# Measurement log

One entry per capture: scans, caliper photos, iPad frames. Newest at the
bottom. Every file in this directory is listed here with what it shows and
which rows in `../MEASUREMENTS.md` it backs. Files are named
`YYYY-MM-DD-<kind>-<nn>-<what>.<ext>`.

Scanner: HP Color LaserJet Pro MFP 3301 flatbed, driven over eSCL
(`tools/scan.py`). 600 dpi optical maximum (the driver's 1200 is
interpolated), so 600 dpi it is: 0.0423 mm/px nominal. Scale is always
calibrated against the steel rule in frame, never trusted from the dpi.

## 2026-09-24 scan 01 — every board, top and bottom, 600 dpi

`2026-09-24-scan-01-all-boards-600dpi.jpg` (2834×4694 px, region 25–145 mm
× 0–200 mm of the platen). On the glass, left to right, top to bottom:

- Steel rule (Pittsburgh 12", cm on the left edge, inches on the right),
  the scale reference for this scan.
- PINK Pico clone, component side down (USB-C, BOOTSEL, RP2040, crystal,
  four mounting holes). Then the same board, back side down.
- Waveshare Pico-LCD-1.3, screen side down (joystick, glass, four tact
  switches, blue FPC tape at the right edge). Then back side down (two
  20-pin female headers, so the PCB sits ~8 mm off the glass and is out of
  focus — heights come from calipers, not this).

Boards were laid loose, not squared to the platen; the analysis fits each
outline's angle. Flatbed depth of field is a few mm: surfaces on the glass
are sharp, anything lifted by a connector or the joystick is soft. Good for
X/Y centres and outlines, useless for Z. Backs: rows P21, L-series plan
view, S/B/J centres (pending analysis, see next entry).

## 2026-09-24 scan 01 — analysis

`tools/measure_scan.py` on the scan above → `2026-09-24-scan-01-analysis.json`
and `2026-09-24-scan-01-lcd-top-fit.png` (red = fitted rectangles, green =
fitted discs; look before trusting a number). Scale from the rule's mm ticks:
196 ticks, RMS 0.03 mm. Filled: L1, L2, S1, S2, S4, S5, B4, B8a–d, J4, J10,
J1/J2 — all tagged `scan01`, all "confirm cal". Pink Pico rows
not filled: that board sat tilted on their connectors and scanned soft.
Lesson for scan 02: put each board's FLAT side on the glass, or shim the
connector end so the PCB lies parallel to the glass.

## 2026-09-24 caliper session, on the iPad camera

Files `2026-09-24-cal-<ROW>-<what>-<n>.jpg`, one per reading, frame grabbed
the moment Austin read the number. Every row says "cal 2026-09-24". Filled:
LCD L1 L2 L3 L7, S3, the whole button B1–B7, J4 J5 J6; PINK P1 P2 P3 P12 P13
P15 P18; the stack A1 A2. Method for heights: hat on its long edge, one jaw on the
socket top, the other on the feature; 10.66 (socket top to PCB front) is
the common offset. Scan-vs-caliper: the scan over-reads outlines by 0.14 to
0.18 mm from edge blur; feature centres were not re-checked (no need, the
scan was sharp there).

## 2026-09-24 R4 evidence audit

Codex inspected all 23 existing caliper frames, full scan and overlay.
No new measurement was taken. See MEASUREMENTS.md R4 section for missed
contact frames, ambiguous shared height datum, slight digit differences,
and the suspect USB segmentation. Recorded values were preserved rather
than silently replaced from ambiguous photographs. Derived centre-offset
rows SC1/BC1/JC1/JC2 come from the existing analysis JSON.
