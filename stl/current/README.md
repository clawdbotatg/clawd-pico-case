# Current best version: v1.7 + J22 joystick

Print from this folder. These paths never change: when a newer version wins
a physical test, `cad/current.py` replaces the files and `current.json`.

| File | Part | From | Per case |
|---|---|---|---|
| `lid.stl` | Lid, face down: rounded, taller inside, crush ribs, smooth edges, locking pockets | v1.7 | 1 |
| `base.stl` | Base, floor down: 6 locking catches, pry slot | v1.7 | 1 |
| `joystick.stl` | J22 joystick: flat-top 7.4 ball, 8.6 round flange thinned under the lid with four diagonal tabs, hole 1.9 deep (wide 3.2 mouth for the first 0.5, then the 1.90 square) | J22 | 1 |
| `button.stl` | Button cap, flange down | v1.0/S2 | 4 |
| `full-set.stl` | All seven on one plate | — | — |

PETG, 0.16 mm, 4 walls, no supports, no raft, no brim (caps can't be removed
from a brim or raft). Lid: elephant-foot compensation 0.15. For N copies, use the slicer's
copies setting (or `copies=N` on the print inbox).

Austin tested this set on 2026-09-26 and said "everything works fine". The
v1.5 lid is the only new part. On 2026-09-30 the joystick became J14-2: no
centre click on direction pushes, the cleanest centre press, and it stays on
the stick best. It fits the v1.5-v1.7 lids (same roof under the joystick).

The v1.7 lid and base are what Austin batch-prints (print Mac, 2026-09-30):
lid drop `20260927-115641-lid-face-down`, 24 in white PETG; base drop
`20260927-112055-base-floor-down`, 24 (12 black, 12 grey); four plates of six
each, 2026-09-27 to 29. The v1.5 lid / v1.3 base listed here until today
were stale: v1.7 was never written back after it passed. The bases and buttons are the ones already
printed. Hashes and sources are in `current.json`.

Stable links:
`https://raw.githubusercontent.com/clawdbotatg/clawd-pico-case/main/stl/current/<file>`

## On the print Mac

v1.5 reference drops (2026-09-26, not printed): `20260926-213136-lid`, `20260926-213137-base`, `20260926-213137-joystick`, `20260926-213137-button`, `20260926-213138-full-set`.
A message tells the print Claude to reprint them on request with `copies=N`,
and that they replace the v1.3 CURRENT drops.

J22 joystick drop (2026-09-30, no raft, copies on request): `20260930-211620-joystick` (replaces the J15 drop `20260930-122840-joystick`).

On 2026-09-30 evening the joystick became J22 (J21-1 with a flat top): the
wide mouth clears the stick's collar so a press clicks only the centre, the
tabs keep it in the lid, and 1.9 deep is the depth Austin picked.
