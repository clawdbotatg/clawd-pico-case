# clawd-pico-case

An MIT-licensed 3D-printed case for a USB-C RP2040 Pico clone (the pink board) plugged into a
Waveshare Pico-LCD-1.3 (240x240 screen, joystick, four buttons). Buttons and
joystick get caps. Made to be printed and sold.

## Why this repo exists

The cases we used before are not ours to sell:

- Tomáš Plass, "Waveshare Pico 1.3 LCD Case", Printables model 1322102, CC BY-NC 4.0.
- Zez0000, "Raspberry Pi Pico 2 Case - Waveshare 1.3\" LCD", MakerWorld model
  3230142, CC BY-NC 4.0. A remix of the Plass case with button and joystick caps.
- Every case file in the `austintgriffith/picowallet` repo derives from those two.

NC means no commercial use. So this case is designed from scratch, from the
hardware and its datasheets only, and released under MIT.

## The rule

Nobody working on this repo opens the designs above, or any other case for
this board, while designing. Not the files, not the photos, not the listing
pages. Every dimension comes from a caliper or a datasheet and is written down
in `MEASUREMENTS.md` before it is used. Every design input is logged in
`PROVENANCE.md`. See `PROCESS.md` for the full protocol and `CLAUDE.md` for the
rules AI agents follow here.

A case for this board will look like the others because the board decides the
size, the screen window, the button holes, the joystick hole and the USB
cutout. That is fine. Shape forced by the hardware is not anyone's property.
What we do not copy is their files and their styling choices.

## Layout

| Path | What |
|---|---|
| `PROCESS.md` | The clean-room protocol, phase by phase |
| `SOURCES.md` | Allowed inputs and forbidden inputs |
| `MEASUREMENTS.md` | The measurement sheet. Every number the design uses |
| `PROVENANCE.md` | Dated log of every design input and who added it |
| `DESIGN.md` | Design decisions, written during the design phase |
| `REPORT.md` | Current state: measurements, design, confidence, open questions |
| `cad/` | build123d source. The design is the source, not the STL |
| `renders/` | `viewer.html`: every part in 3D in a browser, rebuilt from source |
| `research/` | Notes on method: how to get real hardware into 3D |
| `stl/` | Built outputs |
| `prints/` | Print log: what was printed, what fit, what did not |
| `measurements/` | Caliper photos and datasheet drawings |

## Status

Phase 0 done 2026-09-19. Method research done 2026-09-20. Measuring and a
first model done 2026-09-24; not yet printed or fitted. Where it stands, every
number and what is still unknown: `REPORT.md`.

## License

MIT. See `LICENSE`. "Raspberry Pi" and "Waveshare" are their owners'
trademarks. This case is made for their boards and says so descriptively. It
carries no logo but our own.
