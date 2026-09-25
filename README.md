# clawd-pico-case

**Current: [v1.0, the first production version](RELEASE-v1.0.md).** Print
`stl/v1.0/`, and see the [3D model](renders/v1.0/viewer.html) and the
[photos](prints/v1.0-photos/README.md). Everything else in `stl/`, `renders/`
and `prints/` is development history (0.x prototypes), kept on purpose as
the design record.

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

## Development history (superseded by v1.0)

**Latest: low-lid V3 review, with the lid 1 mm above the glass.**
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

## License

MIT. See `LICENSE`. "Raspberry Pi" and "Waveshare" are their owners'
trademarks. This case is made for their boards and says so descriptively. It
carries no logo but our own.
