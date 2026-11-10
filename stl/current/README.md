# Print this: v1.9 case

> **⚠️ Printing the joystick cap? Use [these settings](JOYSTICK-PRINT.md).**
> On normal settings it comes out fragile and breaks.

| File | Copies | Colour |
|---|---|---|
| `lid.stl` | 1 | White |
| `base.stl` | 1 | Black |
| `joystick.stl` | 6 or more (use 1, rest are spares) | Grey. [Special settings](JOYSTICK-PRINT.md) |
| `button.stl` | 4 | 2 grey (middle two), 1 green (top right), 1 red (bottom right) |

Button positions: hold the case sideways, screen facing you, joystick on
the left. The four buttons are the column on the right.

All PETG. 0.16 mm layers, 4 walls, no supports, no brim, no raft. Lid:
elephant-foot compensation 0.15. Don't rotate the parts; they are already the
right way up (lid face down, base floor down, caps flange down).

**The joystick cap needs its own settings.** On normal settings it comes out
fragile. Read [JOYSTICK-PRINT.md](JOYSTICK-PRINT.md) before printing it.

`full-set.stl` is all seven parts on one plate, in one colour. Its one joystick cap
prints on the case settings and comes out weak; print caps separately with
[the joystick settings](JOYSTICK-PRINT.md). Skip it for a
coloured case.

Everything else in `stl/` is old test parts. Don't print it.
Change log: [HISTORY.md](HISTORY.md).

**"Buttons" means `button.stl`** (the four front caps by the screen). The RESET plunger (`stl/atomic-wedgie/aw-reset-plunger.stl`) is a different part. Its only use: one, in black, for the red Atomic Wedgie base. Don't print it unless someone asks for the Atomic Wedgie or the RESET plunger by name.

Atomic Wedgie (RP2040-Plus with a battery): red base plus one black RESET plunger. See `../atomic-wedgie/`.
