# clawd-pico-case v1.0 — first production version

Released 2026-09-25 under the MIT license (see `LICENSE`, © 2026 Austin Griffith).
Anyone may use, change and sell it.

## What it is

A 3D-printed case for a USB-C RP2040 Pico board plugged into a Waveshare
Pico-LCD-1.3. It has seven printed parts: lid, base, joystick cap and four
button caps. The two shells snap together with hidden catches, and a single
notch on the side lets you pry them apart.

## Files

| File | Print |
|---|---|
| `stl/v1.0/v1.0-full-set-seven-parts.stl` | One full set on one plate |
| `stl/v1.0/lid-face-down.stl` | Lid, outer face down |
| `stl/v1.0/base-floor-down.stl` | Base, floor down |
| `stl/v1.0/joystick-j2.stl` | Joystick cap, flange down |
| `stl/v1.0/button-1..4.stl` | Button caps, flange down |

Print with no supports and no raft. The tested set was PLA at 0.16 mm layers
with 4 walls. For several sets, print copies of the plate in the slicer.
Hashes are in `renders/v1.0/manifest.json`. Check against the 3D model at
`renders/v1.0/viewer.html`. Rebuild with `.venv/bin/python cad/v1_production.py`.

## How it got here

Over two days (2026-09-24 and 09-25) there were more than a dozen prototype rounds: V1–V3, R4/R5, J1–J3,
L1–L4, S1 and S2, all saved in `ITERATIONS.md`, `prints/` and Git.
S2 passed Austin's hands-on test. V1.0 is S2 plus three 0.25 mm nudges he
asked for after that test:

1. Joystick hole moves 0.25 mm toward the USB-C end, away from the screen.
2. USB-C opening moves 0.25 mm up, toward the lid.
3. Reset hole in the base moves 0.25 mm away from the USB-C end.

Only those openings changed (checked in CAD). The buttons and joystick cap
are byte-identical to the tested parts.

## Not yet verified

- The three nudges have not been printed. Austin chose to go straight to PETG.
- PETG has not been tried. It shrinks and flexes differently from PLA, so
  check the snap fit and button feel on the first PETG set before printing a
  batch.
- MIT covers what this project authored. It is not a legal clearance; see
  `reports/2026-09-25-provenance-audit.md`.
