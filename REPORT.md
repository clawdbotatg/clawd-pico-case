# Case report — 2026-09-24

One file: every measurement, the 3D design, why each choice, how sure I am,
what I need. For Austin and for Codex's double-check.

- 3D viewer: `renders/viewer.html`, served on the LAN from the dev laptop, port 8793 (drag to turn, explode slider)
- Source: `cad/params.py` (every number), `cad/model.py` (geometry), `cad/build.py`
- Outputs: `stl/*.stl` (assembled position), `stl/print/*.stl` (print orientation), `stl/assembly.step`
- Evidence: `MEASUREMENTS.md` (row IDs), `measurements/` (scan + one photo per caliper reading)

## Frame

Looking at the screen, joystick up. Origin = bottom-left corner of the LCD
PCB. +x right, +y toward the joystick, +z out of the screen. z = 0 is the
LCD PCB front face.

## Measurements

Confidence: **H** = caliper, photo on file. **M** = scan, sharp feature.
**L** = scan with edge blur, or a single rough reading. **G** = guess.

### LCD hat (Waveshare Pico-LCD-1.3)

| Row | What | mm | Src | Conf |
|---|---|---|---|---|
| L1 | Board length (y) | 52.50 | cal | H |
| L2 | Board width (x) | 26.44 | cal | H |
| L3 | PCB thickness | 1.97 | cal | H |
| L4 | PCB corner radius | 1.5 | — | **G** |
| L7 | Female socket height below PCB | 8.69 | cal (10.66 − L3) | H |
| S1 × S2 | Glass, y × x | 26.48 × 25.19 | scan | M |
| S3 | Glass top above PCB | 2.05 | cal | H |
| — | Glass centre vs board centre (x, y) | −0.14, −0.29 | scan | M |
| B1 × B2 | Button casing, y × x | 3.34 × 4.42 (4.30 2nd) | cal | H |
| B3 | Casing top above PCB | 1.81 | cal | H |
| B4 | Plunger oval, x × y | 2.38 × 3.00 | cal | H |
| B5 | Plunger top above PCB | 2.61 | cal | H |
| B6 | Travel | 0.38 | cal | H |
| B8 | Button centres (Y X B A), x | 4.78, 10.50, 16.09, 21.79 | scan | M |
| B8 | Button row, y | 3.98 | scan | M |
| J4 | Stem, square across flats | 1.86 | cal | H |
| J4b | Lip at stem base | 2.94 | cal | H |
| J6 | Stem tip above PCB | 5.00 | cal | H |
| J10 | Stem centre (x, y) | 13.17, 46.13 | scan | M |
| J1/J2 | Silver joystick base, plan | 8.81 × 7.22 | scan (blurred) | L |
| J3 | Joystick body height | 3.0 | — | **G** |
| F | Blue FPC tape past the right edge | ~4 out, y 22–30 | scan (soft) | L |
| — | Gold flex strip between glass and buttons, height | — | not measured | **—** |

### Pico clone (PINK, USB-C)

| Row | What | mm | Src | Conf |
|---|---|---|---|---|
| P1 | Length | 51.04 | cal (datasheet 51.0) | H |
| P2 | Width | 20.82 | cal | H |
| P3 | PCB thickness | 1.23 | cal | H |
| P11 | USB-C overhang past edge | 2.47 | scan | M |
| P12 | USB-C shell width | 8.87 | cal | H |
| P13 | USB-C shell height | 3.08 | cal | H |
| P15 | Tallest point above PCB (shell) | 3.25 | cal (4.48 − P3) | H |
| P18 | Pin length below PCB | ~10.0 | cal | L |
| P10 | Header row spacing | 17.78 | datasheet | H |

### Stack

| Row | What | mm | Src | Conf |
|---|---|---|---|---|
| A1 | Glass to Pico PCB back | 17.54 | cal | H |
| A1 | Glass to USB-C shell | 19.95 | cal (jaws offset) | M |
| A2 | Gap LCD PCB back → Pico PCB | 12.29 | derived | H |
| A3 | USB-C end | joystick end | Austin | H |
| A3 | Pico centred under hat in x and y | assumed | — | **G** |

Scan vs caliper: the scan over-reads outlines by 0.14–0.18 mm (edge blur).
Feature centres in the scan are sharp (they touched the glass).

## Design (current build)

Case outside: **31.0 × 57.1 × 24.6 mm**. Two parts plus caps, snap fit.

| Part | What it is |
|---|---|
| Base | Tub. Pocket = LCD outline + 0.3. Floor under the USB-C shell + 0.3. Top 3 mm of the wall is a 1.2 mm tongue with 4 snap bumps (0.5 high, 8 long, 2 per long side). USB-C slot in the joystick-end wall. Shelf that holds the LCD PCB at the right height. |
| Lid | 2.25 mm plate over the glass + 0.3 air. 0.8 mm skirt drops 3 mm over the tongue, notches catch the bumps. Screen window = glass + 0.4 each side. 4 square button holes 4.7 mm, 1.0 mm web between. Pocket under the plate for cap flanges. Joystick hole Ø10.5. |
| Button caps ×4 | 4.2 mm square post, 0.8 corner radius, 1.0 proud of the lid. 5.3 mm square flange 0.8 thick under the lid, rests on the plunger. Can't come out the top. |
| Joystick cap | Round, square blind socket 1.86 + 0.15 onto the stem. |

## Decisions and why

| Decision | Why |
|---|---|
| Snap fit | Austin's call. No hardware, one print. |
| Split at the LCD PCB front face | The lid then carries every opening (screen, buttons, stick); the base only carries USB. Each part prints flat with no supports. |
| Wall 2.0, skirt 0.8, tongue 1.2 | Tongue must be ≥ 3 perimeters (0.4 nozzle) or it cracks. First build had a 0.4 tongue; fixed. |
| Clearance 0.3 around PCBs | Normal FDM slip fit on a P2S. First print will tell (T rows). |
| Square caps, flange under lid | Austin: square, a web between holes, a lip so they can't come out. |
| Cap post 4.2 in a 4.7 hole | 0.25 per side is a free slide in PLA; 1.0 web keeps the lid strong between holes. |
| Joystick hole 10.5 | Silver base 8.81 across and its height is unknown; gives the lid room to seat. |
| USB-C slot = shell + 0.5 | Only the shell is measured. See ask 2. |
| Lid and joystick cap print flipped | Flat face on the plate, no supports, best top finish. |
| No BOOTSEL access | Not asked for. Easy to add a pin hole. |
| PLA, 0.16 mm | Test material. Final material TBD. |

## Confidence

- **Lid fits over the hat: ~60%.** Openings come from measured centres. Risks: the gold flex strip and the joystick base may be taller than the 2.35 mm lid ceiling; the FPC tape.
- **Buttons work: ~70%.** Heights and travel are measured. Flange rests on the plunger with 0.15 air above; if it's too tight they'll be pressed all the time.
- **Base fits the stack: ~40%.** Pico centring is assumed, the USB slot height depends on it, and the FPC tape currently collides with the wall.
- **Snap holds and releases: ~50%.** First cut, no testing.
- **Whole case works first print: ~25%.** Expect 2–3 rounds.

## What I need from you

1. **FPC tape.** The blue tape sticks out ~4 mm past the right edge of the LCD board. Does it fold flat against the board, or does it have to stay out there? (The wall currently hits it.)
2. **USB cable plug.** The cutout fits the metal shell only. Pinch the plastic end of the USB-C cable you'll use: width and height.
3. **Two heights**, board on its edge, one jaw on the socket top, the other on: (a) the top of the **silver joystick base**, (b) the top of the **gold strip** between the glass and the buttons. Read each.
4. **Pico position.** Look at the stack from the USB end: is the pink board centred left-right under the blue one? Yes/no is enough.

## For Codex

Check `cad/params.py` against `MEASUREMENTS.md` (every number must cite a
row), `cad/model.py` for geometry that contradicts a measurement (anything
the lid or base intersects in the assembled position), and the print
orientation in `stl/print/`. Do not edit; write findings.

## State

- Print inbox: lid v2 `20260924-185135-lid`, caps `20260924-184357-button_caps`, joystick cap `20260924-184357-joystick_cap`. Old lid `20260924-184357-lid` marked skip. Nothing printing; waiting on your go.
