# Current best version: v1.5

Print from this folder. These paths never change: when a newer version wins
a physical test, `cad/current.py` replaces the files and `current.json`.

| File | Part | From | Per case |
|---|---|---|---|
| `lid.stl` | Lid, face down: rounded, 0.5 mm taller inside, crush ribs | v1.5 | 1 |
| `base.stl` | Base, floor down | v1.3 | 1 |
| `joystick.stl` | J9 joystick: flat-top 7.4 ball, rounded edge, printable socket | v1.5 | 1 |
| `button.stl` | Button cap, flange down | v1.0/S2 | 4 |
| `full-set.stl` | All seven on one plate | — | — |

PETG, 0.16 mm, 4 walls, no supports, no raft. For N copies, use the slicer's
copies setting (or `copies=N` on the print inbox).

Austin tested this set on 2026-09-26 and said "everything works fine". The
v1.5 lid is the only new part. The bases and buttons are the ones already
printed. Hashes and sources are in `current.json`.

Stable links:
`https://raw.githubusercontent.com/clawdbotatg/clawd-pico-case/main/stl/current/<file>`

## On the print Mac

v1.5 reference drops (2026-09-26, not printed): `20260926-213136-lid`, `20260926-213137-base`, `20260926-213137-joystick`, `20260926-213137-button`, `20260926-213138-full-set`.
A message tells the print Claude to reprint them on request with `copies=N`,
and that they replace the v1.3 CURRENT drops.
