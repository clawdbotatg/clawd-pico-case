# Atomic Wedgie: print this

For a Waveshare RP2040-Plus with a battery. Same case as `stl/current/`, with
a different base: a channel in the end wall (away from the USB) for the
battery plug and wire, a BOOT pin hole, and a RESET button.

| File | Copies | Colour |
|---|---|---|
| `base.stl` (this folder) | 1 | Red |
| `reset-button.stl` (this folder) | 1 | Black |
| `../current/lid.stl` | 1 | White |
| `../current/joystick.stl` | 1 | Grey |
| `../current/button.stl` | 4 | 2 grey (middle two), 1 green (top right), 1 red (bottom right) |

All PETG. 0.16 mm layers, 4 walls, no supports, no brim, no raft. Don't
rotate the parts (base floor down, caps flange down).

Assembly: drop the RESET button into its hole from inside the base, flange
up, before the board goes in.

Source: base `cad/aw2_base.py`, RESET button `cad/aw_reset_v3.py`.
