# J24-FIT joystick fit test (caps only, not current)

Three J22 caps. The only difference is how far down the tight 1.90 square goes
(J22-GRIP: the stick never reaches the wide part of the hole).

| Dots | Bottom opening | Tight grip |
|---|---|---|
| 1 | J22's (3.2 × 0.5 + funnel) | 0.75 |
| 2 | 3.1 × 0.35 + funnel | 0.95 |
| 3 | 0.25 chamfer only | 1.65 |

Roof at 1.9 and the J22 outside on all three. PETG 0.16, 4 walls, flange down,
no supports, raft or brim, away from the bed centre.

Test on the bare stick: snug push on, stays upside down, centre press clicks
only centre (3 dots may sit on the collar), clamp the height.

`stl/test/j24-fit/joystick-j24-fit-plate.stl`, SHA256 `f7ae9cd16da29d605313ec9dedb5d89609c1a0caa7c44c2071abd31ee64d96cf` (server hash matches). Drop `20261002-115941-joystick-j24-fit-plate`, no colour or GO.

The printer made 3 of each in a ring (the first try failed at layer 17). The
top dots printed unreadable; caps were told apart by the hole underneath.

## Result (Austin, 2026-10-02)

3 (square almost to the bottom) is ruled out: pressing it also clicks other
directions, so the in-press isn't clean. The wide end has to stay. 1 vs 2 is
pending.
