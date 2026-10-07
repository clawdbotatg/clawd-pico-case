# stl/current change log


2026-10-02: Austin tested J24-A in the V1.9 test lid (+0.3) with S2 buttons:
holds against a hard pull, diagonals don't click centre, centre clicks
cleanly, screen gap right: "everything is good". The v1.9 lid is that test
lid without the logo. Base unchanged (v1.7). J24-A also seemed fine in an old
v1.7 lid on a quick try; the v1.9 lid gives it 0.3 more room. These paths never change: when a newer version wins
a physical test, `cad/current.py` replaces the files and `current.json`.

| File | Part | From | Per case |
|---|---|---|---|
| `lid.stl` | Lid, face down: v1.7 0.3 taller inside, bezel back down to 0.3 over the screen, no logo | v1.9 | 1 |
| `base.stl` | Base, floor down: 6 locking catches, pry slot | v1.7 | 1 |
| `joystick.stl` | J24-A joystick: J22's flat-top 7.4 ball, round 10.0 flange (thin 0.24 edge, no tabs), hole 1.9 deep: round 3.1 for 0.35, then the 1.90 square | J24-A | 1 |
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
tabs are meant to keep it in the lid, and 1.9 deep is the depth Austin picked.

Known limits (V1.8-FEEDBACK, 2026-10-01): J22 sometimes clicks N + W + centre
on a NW push, and a hard push or pull can take it out of the case. The +0.3
test lid is better but not fixed. It is current because it is the best tested,
not because it meets these requirements. See `JOYSTICK-PLAN-2026-10-02.md`.

v1.9 drops (2026-10-02, copies on request): lid `20261002-145626-lid`, joystick `20261002-145627-joystick` (J24-A; replaces J22's `20260930-211620-joystick`). Base stays v1.7 `20260927-112055-base-floor-down`.
