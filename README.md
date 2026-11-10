# clawd-pico-case

## What to print (v1.9)

> **⚠️ Printing the joystick cap? Use [these settings](stl/current/JOYSTICK-PRINT.md).**
> On normal settings it comes out fragile and breaks.

Files are in [`stl/current/`](stl/current/README.md). One case:

| File | Copies | Colour |
|---|---|---|
| [`lid.stl`](stl/current/lid.stl) | 1 | White |
| [`base.stl`](stl/current/base.stl) | 1 | Black |
| [`joystick.stl`](stl/current/joystick.stl) | 6 or more (use 1, rest are spares) | Grey. [Special settings](stl/current/JOYSTICK-PRINT.md) |
| [`button.stl`](stl/current/button.stl) | 4 | 2 grey (middle two), 1 green (top right), 1 red (bottom right) |

Button positions: hold the case sideways, screen facing you, joystick on
the left. The four buttons are the column on the right.

All PETG. 0.16 mm layers, 4 walls, no supports, no brim, no raft. Lid:
elephant-foot compensation 0.15. Don't rotate the parts; they are already the
right way up (lid face down, base floor down, caps flange down).

**The joystick cap needs its own settings.** On normal settings it comes out
fragile. Read [JOYSTICK-PRINT.md](stl/current/JOYSTICK-PRINT.md) before printing it.

**"Buttons" means `button.stl`** (the four front caps by the screen). The RESET plunger (`stl/atomic-wedgie/aw-reset-plunger.stl`) is a different part. Its only use: one, in black, for the red Atomic Wedgie base. Don't print it unless someone asks for the Atomic Wedgie or the RESET plunger by name.

**Atomic Wedgie** (RP2040-Plus with a battery): red base with a battery
channel and a black RESET plunger. See [`stl/atomic-wedgie/`](stl/atomic-wedgie/README.md).

`full-set.stl` is all seven parts on one plate, in one colour. Its one joystick cap
prints on the case settings and comes out weak; print caps separately with
[the joystick settings](stl/current/JOYSTICK-PRINT.md). Skip it for a
coloured case.

Everything else in `stl/`, `renders/` and `prints/` is old tests, kept as the
design record. Don't print it.

An MIT-licensed 3D-printed case for a USB-C RP2040 Pico clone (the pink board) plugged into a
Waveshare Pico-LCD-1.3 (240x240 screen, joystick, four buttons). Buttons and
joystick get caps. Made to be printed and sold.

A micro-USB Pico fits too: Austin tested one in the v1.9 case on 2026-10-07,
and the cable and BOOTSEL both work
([log](prints/2026-10-07-micro-usb-fit.md)).

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

## Old development history (before v1.0, don't use)

**Last pre-v1.0 review: low-lid V3, with the lid 1 mm above the glass.**
[Interactive model](renders/v3-low/viewer.html) · [Low-lid design and limitations](reports/2026-09-25-low-lid-experiments.md).
Rear retaining tab replaces the failed side-tab experiment. Not print-approved.
`stl/print/` still contains the OLD tall draft; do not print those files.

### Superseded tall V3 review

**V3 is ready for browser review only; not approved for printing.**
[Interactive model](renders/viewer.html) · [V3 changes and limitations](reports/2026-09-25-v3-review.md).
Flat lid (+4 mm uniformly), restored earlier joystick interface, internal lip,
closed USB port without the lid tab. No V3 print request has been sent.

### Earlier V2 result

**V2 failed its physical fit test. Do not reprint unchanged.**
[What worked, what failed, and correction goals](reports/2026-09-25-v2-review.md).
The V2 description below records the submitted design, not a ready replacement.

Saved designs and print history: [iteration register](ITERATIONS.md).

V1 feedback is [saved with photos](prints/2026-09-24-v1-feedback.md).
V2 / R5 implements all five changes: captive ball joystick, pry notches,
higher/tighter USB-C, wider/taller rectangular buttons and scan-positioned
bottom button access. Fit-test candidate; physical fit unverified. Original geometry;
no third-party case models used. The current target is the measured pink
USB-C board, not an official Pico W/Pico 2 W.

See [V2 preview](renders/r5-preview.png), [interactive assembly](renders/viewer.html),
and [critical review / assembly instructions](REPORT.md). R4 was submitted
to the print inbox; a hold/superseded request was subsequently posted.
Operator acknowledgment and V1's exact printed commit remain unconfirmed.
V2 dispatch and eventual result are recorded in [its print log](prints/2026-09-24-v2.md).
CAD validation is not physical validation; remaining measurements are in the report.

## Build

With Python 3.12 and dependencies in requirements.txt:

```sh
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python cad/v1_production.py
```

This checks the v1.0 geometry, then writes `stl/v1.0/` and `renders/v1.0/`
(STEP, viewer, validation and hashes). `cad/build.py` and `stl/print/` belong
to the old R4/R5 prototype. Do not print them.

`stl/current/` is written by `.venv/bin/python cad/current.py`.

## License

MIT. See `LICENSE`. "Raspberry Pi" and "Waveshare" are their owners'
trademarks. This case is made for their boards and says so descriptively. It
carries no logo but our own.
