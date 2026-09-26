# Current best version: v1.3

Print from this folder. These paths never change: when a newer version wins
a physical test, `cad/current.py` replaces the files and `current.json`.

| File | Part | Per case |
|---|---|---|
| `lid.stl` | Lid, face down | 1 |
| `base.stl` | Base, floor down | 1 |
| `joystick.stl` | Joystick cap, flange down | 1 |
| `button.stl` | Button cap, flange down | 4 |
| `full-set.stl` | All seven on one plate | — |

PETG, 0.16 mm, 4 walls, no supports, no raft. For N copies, use the slicer's
copies setting (or `copies=N` on the print inbox).

v1.3 = v1.0 with the USB-C end wall 0.5 mm in. Austin tested it on
2026-09-26: "holds the case just right, nothing rattles, everything clicks".
The hashes and source files are in `current.json`.

Stable links:
`https://raw.githubusercontent.com/clawdbotatg/clawd-pico-case/main/stl/current/<file>`

## On the print Mac

Reference drops (2026-09-26, not printed): `20260926-073507-lid`,
`20260926-073507-base`, `20260926-073507-joystick`, `20260926-073507-button`
and `20260926-073508-full-set`. A message tells the print Claude to reprint
them on request with `copies=N`.
