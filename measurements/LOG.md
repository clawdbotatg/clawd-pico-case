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
- Two ATECC608 breakout boards (the crypto chip). One component side down,
  one connector side down. Not yet in the board register.

Boards were laid loose, not squared to the platen; the analysis fits each
outline's angle. Flatbed depth of field is a few mm: surfaces on the glass
are sharp, anything lifted by a connector or the joystick is soft. Good for
X/Y centres and outlines, useless for Z. Backs: rows P21, L-series plan
view, S/B/J centres (pending analysis, see next entry).
