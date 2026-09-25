# Case report — 2026-09-24

One file: every measurement, the 3D design, why each choice, how sure I am,
what I need. For Austin and for Codex's double-check.

- 3D viewer: `renders/viewer.html`, served on the LAN from the dev laptop, port 8793 (drag to turn, explode slider)
- Source: `cad/params.py` (every number), `cad/model.py` (geometry), `cad/build.py`
- Outputs: `stl/*.stl` (assembled position), `stl/print/*.stl` (print orientation), `stl/assembly.step`
- Evidence: `MEASUREMENTS.md` (row IDs), `measurements/` (scan + one photo per caliper reading)

## Test 2 (best guess, sent to print 2026-09-24)

Built to work even if the unknowns go the bad way:
- Joystick hole 12.0: clears the silver base whatever its height.
- New joystick cap: thin neck on the stem through the hole, 12.8 disc 1.2 above the lid so the stick can tilt ~10°.
- USB-C slot tall enough for both disagreeing readings (4.9 mm).
- 1 mm recess in the end wall for a 12.5 × 7.0 plug (guess).
- Two pads in the lid's top corners hold the LCD board down (0.05 air).
- Assumes the blue tab is peeled off.

Checked: nothing overlaps except the blue tab; snap catches.

## Audit, 2026-09-24 evening (trust nothing, re-check everything)

Method: every part intersected with every other part in the assembled
position (`volume(A ∩ B)`), every number in `cad/` traced to a row, every
doc read against the code, the session transcript checked for web access.

**Fixed in this pass**

| Found | Effect | Fix |
|---|---|---|
| Snap notches were cut on the cavity side of the skirt and removed nothing. Lid ∩ base = 15.7 mm³, all at the bumps. | The lid would never click; it would jam 0.5 mm proud. | Windows through the skirt; bumps are now wedges (ramp on top, flat catch below). Verified: lid ∩ base = 0, and lifting the lid 0.15 mm hits the catch. |
| Bumps were square blocks. | No lead-in; the lid could not be pushed on. | Same fix. |
| Pocket corner R1.0 with a guessed PCB corner. | A sharp PCB corner would have 0.01 mm clearance. | Pocket corners R0.8 (clears a sharp corner by 0.09). |
| Joystick cap and shelf used numbers written straight into `model.py`. | Breaks the rule that every number lives in `params.py`. | Moved to `params.py`. Remaining literals are render-only hardware (socket bodies, USB shell depth). |
| This report said the case is 24.6 mm tall. | Wrong. | It is 25.2 mm (below). |
| `PROVENANCE.md` had no entry for today's measuring and geometry session. `DESIGN.md` had empty sections. README still said Pico 2 W and "no geometry". | Weakens the clean-room paper trail. | Entry added (no web access, no forbidden files, checked against the transcript). DESIGN and README filled in. |
| One crypto-board caliper photo was still in `measurements/`. | Not part of this project. | Removed from the tree. It is still in git history (commit c96ed18). |

**Still wrong, needs a measurement (not guessed around)**

| Found | Why it matters |
|---|---|
| Lid ∩ hat = 0.54 mm³: the silver joystick base hits the edge of the Ø10.5 hole. | Only because J3 (base height) is a guess of 3.0. If the base is lower than 2.35 above the PCB it clears. If higher, the hole must be ~12. **Blocks the lid.** |
| Lid ∩ blue tape = 4.8 mm³. | Looking at the scan again: the blue piece lies on top of the glass and runs off the edge. It is most likely the screen protector's pull tab, not a cable. If so, peel it and the problem is gone. |
| P15 and A1 disagree by 0.84 mm on how far the USB-C shell stands off the Pico (3.25 vs 2.41). | The case depth uses the larger (safe), but the USB-C slot height depends on which is right, and the slot is only 1 mm taller than the shell. |
| The Pico's position along the hat is assumed centred. | Sets how far the USB-C shell is from the end wall. |
| The USB-C shell face sits 0.56 mm inside the outer wall face. | A cable's plastic overmould will hit the wall before the plug is fully in. Needs a recess the size of your plug (ask 4). |
| Nothing holds the LCD board down: the lid doesn't touch the board anywhere. | The stack can lift 0.15 mm until the cap flanges hit, then the buttons take the load. Rattles. Fix: small pads on the lid landing on bare PCB in the four corners (top corners look bare in the scan). Not drawn yet; needs ask 6. |
| The ledge the LCD rests on is a 2.8 mm flat overhang off the wall. | Prints with a droopy underside. Cosmetic inside the case; a 45° chamfer under it would fix it. Not drawn yet. |
| Joystick tilt and press travel (J7 to J9) never measured. | Cap has 0.6 mm side clearance in the hole; that may stop the stick short of its click. |

**Checked and fine:** every hardware number in `params.py` matches its
`MEASUREMENTS.md` row. Button caps ∩ lid = 0, caps ∩ hat = 0, base ∩ hat = 0,
base ∩ Pico = 0. All four printable parts are single solids (caps: 4). Print
orientations are flat-face-down. MIT `LICENSE` in place; no third-party
geometry; three.js is loaded from a CDN, not copied in.

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

Case outside: **31.0 × 57.1 × 25.2 mm**. Two parts plus caps, snap fit.

| Part | What it is |
|---|---|
| Base | Tub. Pocket = LCD outline + 0.3. Floor under the USB-C shell + 0.3. Top 3 mm of the wall is a 1.2 mm tongue with 4 wedge snap bumps (0.5 out, 8 long, 2 per long side). USB-C slot in the joystick-end wall. Shelf that holds the LCD PCB at the right height. |
| Lid | 2.25 mm plate over the glass + 0.3 air. 0.8 mm skirt drops 3 mm over the tongue; windows through it catch the bumps. Screen window = glass + 0.4 each side. 4 square button holes 4.7 mm, 1.0 mm web between. Pocket under the plate for cap flanges. Joystick hole Ø10.5. |
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

All at once, in one sitting:

1. **Blue tab.** The blue strip on the right side of the screen: is it the screen protector's pull tab? If yes, peel it off.
2. **Joystick base.** The silver square under the stick: width left-right, width up-down, and height (hat on its long edge, one jaw on the socket top, the other on the top of the silver square).
3. **USB-C position.** Two readings, cable unplugged: (a) from the hat's joystick-end edge to the front face of the USB-C shell, jaws along the long side. (b) Glass top to the USB-C shell, jaws square across, again (the old reading disagrees with another by 0.84).
4. **Cable plug.** The plastic end of the USB-C cable you'll use: width and thickness.
5. **Gold strip height**, between the glass and the buttons, the same way as 2.
6. **Back of the LCD board.** Any parts within 3 mm of the two long edges? Yes/no. And the board's corners: sharp or rounded?

## For Codex

Check `cad/params.py` against `MEASUREMENTS.md` (every number must cite a
row), `cad/model.py` for geometry that contradicts a measurement (anything
the lid or base intersects in the assembled position), and the print
orientation in `stl/print/`. Do not edit; write findings.

## State

- Print inbox: lid v2 `20260924-185135-lid`, caps `20260924-184357-button_caps`, joystick cap `20260924-184357-joystick_cap`. Old lid `20260924-184357-lid` marked skip. Nothing printing.
- The queued lid v2 has the broken snap notches. It still tests the window, button holes and caps against the hat, but not the snap. On your go I re-drop the fixed lid (v3) and mark v2 skip.
