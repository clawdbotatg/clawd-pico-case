# Measurements

Every number the design uses lives here first. Rows have an ID. `cad/` cites
the ID. Blank means not measured yet. Units are mm.

Sources: `cal` = caliper on the bench, three readings, photo in
`measurements/` where useful. `ds` = datasheet or drawing, name the document
and page. When cal and ds disagree, write both and say which we use.

## Boards

There are several Pico-footprint boards on the bench and they differ: micro-USB
vs USB-C, connector overhang, component heights, sometimes hole positions. Each
board gets its own scan, its own caliper rows and its own photo set. The case
either fits all of them or has a base per board, decided in `DESIGN.md` once
the numbers are in.

Board register. Add a row when a new board shows up. The tag prefixes its rows
and files (`P2W-P11`, `measurements/P2W-P11-usb-overhang.jpg`).

| Tag | Board | USB | Marking / colour | Chip | Notes |
|---|---|---|---|---|---|
| P2W | Raspberry Pi Pico 2 W, official | micro-USB | green | RP2350 | official Pico 2 STEP applies |
| PINK | USB-C clone, pink | USB-C | pink | RP2040 | no CAD exists, measure everything |
| | | | | | add more here |

## P. Pico-footprint board rows. One copy per board tag.

Datasheet values below are from the Raspberry Pi Pico 2 W datasheet, mechanical
drawing section, and apply to P2W only. Confirm each with calipers. Copy this
table once per tag; clones must not inherit the datasheet numbers.

| ID | Dimension | Value | Source | Notes |
|---|---|---|---|---|
| P1 | Board length | 51.0 | ds Pico 2 W | confirm cal |
| P2 | Board width | 21.0 | ds Pico 2 W | confirm cal |
| P3 | PCB thickness | 1.0 | ds Pico 2 W | confirm cal |
| P4 | Mounting hole diameter | 2.1 | ds Pico 2 W | confirm cal |
| P5 | Hole centre from short edge | 2.0 | ds Pico 2 W | both ends, confirm cal |
| P6 | Hole centre from long edge | 4.8 | ds Pico 2 W | both sides, confirm cal |
| P7 | Hole spacing along length | 47.0 | ds Pico 2 W | P1 minus 2×P5 |
| P8 | Hole spacing across width | 11.4 | ds Pico 2 W | P2 minus 2×P6 |
| P9 | Header pitch | 2.54 | ds Pico 2 W | |
| P10 | Header row spacing | 17.78 | ds Pico 2 W | 7 × 2.54 |
| P11 | Micro-USB overhang past board edge | | cal | |
| P12 | Micro-USB shell width | | cal | |
| P13 | Micro-USB shell height | | cal | |
| P14 | Micro-USB centre offset from board centreline | | cal / ds | |
| P15 | Height of tallest part above PCB, bottom side (component side facing away from LCD) | | cal | wireless module, BOOTSEL |
| P16 | BOOTSEL button position from short edge | | cal | |
| P17 | BOOTSEL button position from long edge | | cal | |
| P18 | Header pin length below PCB when plugged into LCD | | cal | how far the Pico sits from the LCD board |

| P19 | USB connector type | | look | micro-USB or USB-C |
| P20 | Mounting holes present and where | | cal / scan | clones sometimes move or drop them |
| P21 | Flatbed scan of the bottom side, 1200 dpi | | scan | `measurements/<TAG>-scan-bottom.png` |
| P22 | Flatbed scan of the top side, 1200 dpi | | scan | `measurements/<TAG>-scan-top.png` |

### P2W rows: (table above, fill in)

### PINK rows (USB-C clone, pink, RP2040, male headers soldered). All cal, none from a datasheet.

| ID | Dimension | Value | Source | Notes |
|---|---|---|---|---|
| PINK-P1 | Board length | 51.04 | cal 2026-09-24 | scan01 read 50.75 (edge blur); matches the official Pico outline. `measurements/2026-09-24-cal-PINK-P1-board-length-1.jpg` |
| PINK-P2 | Board width | 20.82 | cal 2026-09-24 | scan01 read 20.95 (edge blur). `measurements/2026-09-24-cal-PINK-P2-board-width-1.jpg` |
| PINK-P3 | PCB thickness | 1.23 | cal 2026-09-24 | `measurements/2026-09-24-cal-PINK-P3-pcb-thickness-1.jpg` |
| PINK-P11 | USB-C overhang past board edge | 2.47 | scan01 | shell past the short edge; the scan edge was sharp here (shell sits on the glass). ±0.2 |
| PINK-P12 | USB-C shell width | 8.87 | cal 2026-09-24 | metal shell, wide way. `measurements/2026-09-24-cal-PINK-P12-usbc-width-1.jpg` |
| PINK-P13 | USB-C shell height | 3.08 | cal 2026-09-24 | metal shell, thin way. Shell top is ~2.4 above the PCB (A1), so ~0.7 of it sits in/below the board line. `measurements/2026-09-24-cal-PINK-P13-usbc-height-1.jpg` |
| PINK-P15 | Tallest part above PCB, component side | 3.25 | cal 2026-09-24 | Austin read 4.48 PCB back face to USB-C shell top = the board's full thickness; minus PINK-P3 1.23. Stack check: A1 19.95 − 17.54 = 2.4 (jaws not exactly opposite there); use 3.25. `measurements/2026-09-24-cal-PINK-P15-board-plus-usbc-height-1.jpg` |
| PINK-P18 | Header pin length below PCB | ~10.0 | cal 2026-09-24 | Austin: 10.5 jaw to jaw including the solder tips on the top face; about 10.0 from the underside to the pin tips. The stack (A rows) is the number that matters. `measurements/2026-09-24-cal-PINK-P18-pin-length-1.jpg` |
| PINK-P18b | Header plastic strip thickness | | cal | |
| PINK-P19 | USB connector type | USB-C | look | |

## L. Waveshare Pico-LCD-1.3, board

| ID | Dimension | Value | Source | Notes |
|---|---|---|---|---|
| L1 | Board length | | cal / ds Waveshare drawing | |
| L2 | Board width | | cal / ds | |
| L3 | PCB thickness | 1.97 | cal 2026-09-24 | one reading, `measurements/2026-09-24-cal-L3-lcd-pcb-thickness-1.jpg` |
| L4 | Corner radius of PCB | | cal | |
| L5 | Mounting hole diameter | | cal / ds | |
| L6 | Mounting hole positions, each, from one chosen corner | | cal / ds | list all |
| L7 | Female header socket height above PCB, Pico side | 8.69 | cal 2026-09-24 | sets stack gap. Read 10.66 socket top to PCB front face, minus L3 1.97. `measurements/2026-09-24-cal-L7-lcd-socket-height-1.jpg` |
| L8 | Female header position from edges | | cal / ds | |
| L9 | Tallest part on the Pico side other than headers | | cal | |

### Scan 01 results, LCD top side (2026-09-24). Source `scan01` = `measurements/2026-09-24-scan-01-all-boards-600dpi.jpg`, fit in `2026-09-24-scan-01-analysis.json`, overlay `2026-09-24-scan-01-lcd-top-fit.png`, code `tools/measure_scan.py`

Scale 23.666 px/mm from 196 rule ticks over 196 mm, fit RMS 0.73 px (0.031 mm); nominal 600 dpi would be 23.622. Origin: see "Chosen corner" below. Outline edges are blurred where the board sits off the glass, so outline rows carry ±0.3 mm until calipers confirm; centres of features that touched the glass (plungers, stem, glass) are good to ~0.1 mm.

| ID | Dimension | Value | Source | Notes |
|---|---|---|---|---|
| L1 | Board length (y) | 52.5 | cal 2026-09-24 | scan01 read 52.68 (edge blur +0.18). `measurements/2026-09-24-cal-L1-lcd-board-length-1.jpg` |
| L2 | Board width (x) | 26.44 | cal 2026-09-24 | scan01 read 26.58 (edge blur +0.14). `measurements/2026-09-24-cal-L2-lcd-board-width-1.jpg` |
| S1 | Glass outline length (y) | 26.48 | scan01 | black glass as visible; ±0.2 |
| S2 | Glass outline width (x) | 25.19 | scan01 | ±0.2 |
| S4 | Glass centre x | 13.15 | scan01 | glass spans x 0.56 to 25.75 |
| S5 | Glass centre y | 26.05 | scan01 | glass spans y 12.81 to 39.29 |
| B4 | Plunger diameter | 2.38 × 3.00 | cal 2026-09-24 | oval: 2.38 across x, 3.00 along y. Cap bears on top; the casing (B1/B2) is what the cap must cover. `measurements/2026-09-24-cal-B4-lcd-plunger-long-1.jpg` |
| B8a | Button Y centre (leftmost) x, y | 4.85, 4.14 | scan01 | |
| B8b | Button X centre x, y | 10.58, 4.00 | scan01 | |
| B8c | Button B centre x, y | 16.16, 4.02 | scan01 | |
| B8d | Button A centre (rightmost) x, y | 21.87, 4.12 | scan01 | |
| B8p | Button pitch (labels Y X B A left to right, from the silkscreen in `2026-09-24-cal-B2-lcd-button-body-1.jpg`) | 5.67 | scan01 | mean of the three gaps |
| J4 | Stem diameter at top | 2.41 | scan01 | dark cap only, confirm cal |
| J10 | Joystick centre x, y | 13.24, 46.22 | scan01 | stem top; base centre agrees within 0.4 |
| J1/J2 | Joystick base plan size | 8.81 × 7.22 | scan01 | fitted to the silver diamond, blurred; confirm cal |

Not from this scan: every Z (L3, L7, L9, S3, B3, B5, B6, J3, J6-J9), hole rows L5/L6 (none visible from the top; back side scan was out of focus), and the switch bodies B1/B2 (blurred).

## S. Screen

| ID | Dimension | Value | Source | Notes |
|---|---|---|---|---|
| S1 | Glass outline length | | cal | |
| S2 | Glass outline width | | cal | |
| S3 | Glass top height above PCB | 2.05 | cal 2026-09-24 | read 12.71 socket top to glass top, minus L3+L7 10.66. Whole hat, socket top to glass top = 12.71. `measurements/2026-09-24-cal-S3-lcd-glass-height-1.jpg` |
| S4 | Glass position from chosen corner, x | | cal | |
| S5 | Glass position from chosen corner, y | | cal | |
| S6 | Active area length | | cal / ds | |
| S7 | Active area width | | cal / ds | |
| S8 | Active area offset within glass, x | | cal | |
| S9 | Active area offset within glass, y | | cal | |
| S10 | Flex cable location and width | | cal | so the lid does not pinch it |
| F1 | Blue tape past the right PCB edge | ~4.0 out, y 22 to 30, at glass level | scan01 | soft edges. In the scan it lies on top of the glass and runs off the edge: probably the screen protector's pull tab, not part of the board. Ask Austin |

## B. Buttons, four tact switches

Measure the switch, not a cap. Identify the part if you can from the marking or
the schematic and add its datasheet to `SOURCES.md`.

| ID | Dimension | Value | Source | Notes |
|---|---|---|---|---|
| B1 | Switch body length | 3.34 | cal 2026-09-24 | metal casing, measured in y (toward the glass). `measurements/2026-09-24-cal-B1-lcd-button-body-1.jpg` |
| B2 | Switch body width | 4.42, 4.30 | cal 2026-09-24 | metal casing, two readings (feet may add to the first); the other plan axis from B1. `measurements/2026-09-24-cal-B2-lcd-button-body-{1,2}.jpg` |
| B3 | Switch body height above PCB | 1.81 | cal 2026-09-24 | Austin read 12.47 socket top to metal casing top, minus 10.66. Oval top (B5 2.61) is 0.80 proud of the casing. `measurements/2026-09-24-cal-B3-lcd-button-casing-height-1.jpg` |
| B4 | Plunger diameter | | cal | |
| B5 | Plunger top height above PCB, at rest | 2.61 | cal 2026-09-24 | Austin read 13.27 socket top to button top, minus L3+L7 10.66. `measurements/2026-09-24-cal-B5-lcd-button-height-1.jpg` |
| B6 | Plunger travel | 0.38 | cal 2026-09-24 | Austin read 12.89 socket top to oval held pressed = 2.23 above PCB; rest is 2.61. `measurements/2026-09-24-cal-B6-lcd-button-pressed-1.jpg` |
| B7 | Plunger shape | oval | look 2026-09-24 | light-coloured oval top; 2.38 across the narrow way (cal), about 2.6 long (scan01) |
| B8 | Centre of each switch from chosen corner, x, y | | cal / ds | four rows, name them by silkscreen label |
| B9 | Actuation force | | ds | for cap weight and return |

## J. Joystick

| ID | Dimension | Value | Source | Notes |
|---|---|---|---|---|
| J1 | Body length | | cal | |
| J2 | Body width | | cal | |
| J3 | Body height above PCB | | cal | |
| J4 | Stem diameter at top | 1.86 | cal 2026-09-24 | across the flats; square section. A cap grips this. A short lip at the very base is 2.94 wide (J4b, cal) — not part of the stick, the cap must clear it |
| J4b | Lip at the stem base, width | 2.94 | cal 2026-09-24 | no photo saved |
| J5 | Stem shape | square | look 2026-09-24 | 1.86 square at the tip, wider at the base |
| J6 | Stem top height above PCB, centred | 5.00 | cal 2026-09-24 | Austin read 15.66 socket top to stem tip, minus L3+L7 10.66. `measurements/2026-09-24-cal-J6-lcd-joystick-height-1.jpg` |
| J7 | Stem tilt angle, full deflection | | cal / ds | |
| J8 | Stem top travel at full deflection, horizontal | | cal | |
| J9 | Centre press travel | | cal / ds | |
| J10 | Centre from chosen corner, x, y | | cal / ds | |
| J11 | Clearance around stem before it hits the body or nearby parts | | cal | |

## A. Assembled stack

| ID | Dimension | Value | Source | Notes |
|---|---|---|---|---|
One block per board tag. The hat is the same; the Pico under it changes.

| ID | Dimension | Value | Source | Notes |
|---|---|---|---|---|
| A1 | Total stack height, Pico bottom-most part to glass top | PINK: 19.95 (glass to USB-C shell); 17.54 glass to the Pico PCB back face | cal 2026-09-24 | Austin: 19.95 is "very close" — jaws not exactly opposite because the plug and glass are at different spots; take as ±0.2. So the USB-C shell stands ~2.4 above the Pico PCB. `measurements/2026-09-24-cal-PINK-A1-stack-glass-to-usbc-1.jpg`, `...-pcb-back-{1,2}.jpg` |
| A2 | Gap between Pico PCB top and LCD PCB bottom | PINK: 12.29 | derived 2026-09-24 | 17.54 − S3 2.05 − L3 1.97 − PINK-P3 1.23. Socket is 8.69 of that; the male header plastic + standoff is the other 3.6 |
| A3 | Pico USB position relative to LCD board edges | joystick end, centred in x (assumed) | Austin 2026-09-24 | USB-C pokes out at the joystick end. x-centring not measured yet |
| A4 | Anything sticking out past the LCD board outline | | look | per tag |

## T. Print tolerances, filled in during Phase 3

| ID | Dimension | Value | Source | Notes |
|---|---|---|---|---|
| T1 | Hole clearance for a free fit | | print | |
| T2 | Clearance for a snug slide | | print | |
| T3 | Cap-to-hole radial clearance | | print | |
| T4 | Printer and nozzle | | | |
| T5 | Material | | | |

## Chosen corner

State here which corner of the LCD board is the origin for all x, y values,
looking at the screen, and which direction is +x and +y. Use the same origin in
`cad/params.py`.

Origin (chosen 2026-09-24): looking at the screen with the joystick at the top
and the four buttons at the bottom, the FPC tape is on the right. Origin is
the bottom-left corner of the LCD PCB. +x to the right (26.44 wide), +y up
toward the joystick (52.50 long, after calipers). The 600 dpi scan is not mirrored (the
rule's digits and the Pico's silkscreen read correctly), so scan x, y map
straight onto this frame.

## R4 audit: derived coordinates and evidence limits

The scan's absolute corner coordinates above used its blurred 26.5835 ×
52.6773 outline. CAD preserves offsets from the fitted board centre and
uses the caliper outline. These are a registration assumption, not new
caliper readings. Do not scale feature spacing to fit the caliper outline.

| ID | Dimension | Value | Source / limitation |
|---|---|---|---|
| SC1 | Glass centre offset x, y | -0.1393, -0.2905 | scan01 JSON glass_centre_uv, reordered v,u |
| BC1 | Button centre offsets x, y, Y/X/B/A | (-8.4400,-22.1949), (-2.7159,-22.3382), (2.8723,-22.3153), (8.5746,-22.2187) | scan01 plungers_uv, reordered v,u; retain individual y values |
| JC1 | Stem centre offset x, y | -0.0529, 19.8792 | scan01 joystick_stem_uv |
| JC2 | Silver base centre offset x, y | 0.2730, 19.4936 | scan01 joystick_base_centre_uv; blurred; differs from stem by 0.505 mm |
| H1 | Header body width/length | 2.54 / 50.8 | provisional render envelope from P9 × 1 / 20; actual plastic and solder envelope unmeasured |
| H2 | Pico corner radius / USB inward depth | 1.0 / 7.0 | inherited render assumptions, not measurements |
| H3 | Silver base orientation / height | 45 degrees / 3.0 | inherited render assumptions, not measurements |
| H4 | PCB corner radius | 1.5 | inherited render only; collision checks also use a sharp rectangle |
| H5 | Blue flag thickness / inboard overlap | 0.3 / 1.0 | inherited illustrative envelope; identity unresolved |

Photo audit: L3's frame shows no board or caliper; S3 and B6 miss the
measurement contact; L7's frame is not a reliable picture of the recorded
10.66 datum. B4's display appears 3.06 rather than recorded 3.00; B2's second
display appears 4.31 rather than 4.30. A1 photos do not unambiguously show
glass contact, so A2 inherits a datum uncertainty as well as the known USB
0.84 discrepancy. PINK-P11 comes from a segmentation that also reports a
20.95-mm USB width (inconsistent with P12 8.87); its ±0.2 claim is not
independently established. Retain all original readings pending recheck.

### R4 design choices (not hardware measurements)

| ID | Choices in mm unless stated | Rationale |
|---|---|---|
| D4-FIT | mating gap 0.20; skirt 0.80; wall 2.20; bump 0.45 × 4 × 1; flexible band span 14; slot 0.60; band roof z=-0.30 | maintain 1.20 tongue; outward flex/release access; bands anchored at both ends to bridge when printed inverted |
| D4-SUPPORT | shelf bearing thickness 0.80, 45-degree underside; pad 1.60, inset 0.50, gap 0.05; shelf gap 0; pocket radius 0.50 | slope from wall to shelf tip; four pads land above side shelves outside switches; sharp corner sensitivity |
| D4-BUTTON | flange 5.00; pocket margin 0.30 | avoid neighbouring flanges colliding when each cap slides sideways by 0.25; no overtravel stop until casing and PCB landing areas are confirmed |
| D4-USB | channel clearance 0.25 for lid fin; shell opening square corners; inherited plug trial 12.5 × 7, recess 1.0 | square envelope contains both rectangular shell bounds; insertion straight down |
| D4-JOY | socket total clearance 0.05 (samples 0, 0.10, 0.20); tip clearance 0; engagement 1.20; disc gap 1.80; hole 12.80; disc 14.0 | seat cap on stem, improve tilt/press room over assumed body and base offset clearance; fit samples are provisional |
| D4-CAD | boolean overlap 0.01; cutter extension 1; bump overlap 0.20; window end clearance 0.30; cavity radius 0.50; window/pocket radius 0.80; plug recess radius 1.0 | construction choices, not hardware facts |
| V4 | joystick sensitivity 10 degrees tilt, 0.30 press, pivot z=0 and 3; XY placement sensitivity 0.10; cap travel sampling 9 positions; insertion sampling 1 mm | diagnostic scenarios only; J7/J9 remain unmeasured |

## R5 user feedback and original choices

Austin reports from the first physical print: joystick must be installed on
the board before the lid and retained by a lower lip; upper control should
be shaft and ball. Also requests a pry notch because the case is hard to
open. No new hardware dimensions supplied. Existing J rows still apply.

| ID | Choices in mm unless stated | Rationale |
|---|---|---|
| D5-JOY | shaft Ø4.20; retaining flange Ø10.40, bottom z=5.00, thickness 0.80; ball Ø7.00, centre z=11.40; throat Ø8.80; flange pocket Ø13.00, ceiling z=6.80; collar outside Ø15.80, roof 1.20 | ball passes opening from inside while wider lip is retained; raised collar clears lip's assumed tilt; socket and engagement inherited from R4 |
| D5-PRY | two side notches centred at y=L1/2, width 6.0 along y, height 1.60, depth 1.0 from exterior, radius 0.50; z centre=-TONGUE_H | gives tool access across skirt/base seam; retains 1.20 of wall behind notch, away from boards |
| V5 | sample press 0 and 0.30, pivots 0 and 3, tilt 0/5/10 degrees; cap pull-up 1.05; assembly clearance with vertical swept envelopes; tool tip 4.0 × 0.60, depth 0.70 | test scenarios, not measured joystick specs or opening-force guarantees |

### V2 print candidate / R5 completed choices

### V3 review choices — 2026-09-25

### V3 low-lid experiment — D7, 2026-09-25

### D8 rear-tab experiment

### J1 isolated round-lip test — 2026-09-25

### V3-FIT fitted shell — 2026-09-25

### V3-FLAT correction — 2026-09-25

### J2 stepped socket trial — 2026-09-25

| ID | Value | Source / limitation |
|---|---|---|
| J2-COLLAR-H | less than1 mm | Austin's direct report after asking collar-only height; not PCB-to-collar height |
| J2-SOCKET | Ø3.00 round opening depth1.00, then2.01 square depth2.00; total3.00 from cap underside | Austin's explicit trial dimensions; square width inherited J1. No extra clearance. IMG_0823 shows3.32 mm on caliper but feature unconfirmed; fit not guaranteed |
| J2-OUTER | identical J1 exterior; blind roof becomes localz3.00 instead of1.90; possible1.10 deeper seating if collar/body allow | Original derived geometry, not measured achievable travel. Do not lower lid until fitted; print flange-down as J1 |

### V3-FLAT parameters

| ID | Choice | Basis |
|---|---|---|
| V3-FLAT | uniform outer facez5.1; underside joystick roof4.4 unchanged; face-down print, rotate180degrees aroundX then translate bedz0; no supports/raft | Austin explicitly approves whole-face raise to fix print orientation. Existing J1 clearance, not new hardware measurement. Screen depth3.05 mm accepted provisionally; unchanged V2 button protrusion1.3 mm, .92 at full press |

### V3-FIT parameters (historical upright print)

| ID | Original design choice | Basis / limitation |
|---|---|---|
| V3-FIT-LID | screen side rails z3.05, local joystick roof4.4..5.1, holeØ8, pocketØ13, outer local bossØ15.8 clipped at screen window; inner pocket clipped window+.4, continuous .4 front wall; button-end top4.6, region ends pocketYmax+.8 | Retain J1's hand-held tested hole/height and V2 buttons; no universal lid-height raise. Local joystick front wall meets upper screen edge, so that small edge segment is higher than side rails. Boss shell dimensions inherited D5/D6; upright print to avoid floating skirt under face-down boss |
| V3-FIT-BUTTON | existing flange z2.61..3.41, pocket ceiling3.56, tops6.4, original4.2×5.4 posts | Exact V2 printed cap parameters; no new caps. V3 low D7 side-wing caps were never printed and must NOT be used |
| V3-FIT-PADS | extend original1.6 square corner pads outward to inner walls, top2.36, bottom.05 | Join pads to shell from first printed pad layer; small corner overhangs still require slicer review |
| V3-FIT-PRINT | both shells upright, bedz0, separation5; PLA .16,3 walls, no supports/raft | Original print plan; actual slice must be checked before start. Lid bottom skirt supplies bed contact, not the raised joystick face |
| V3-FIT-CHECK | inherited0/5/10degree, pivots0/3, press0/.3,8directions; lid-install lifts0..12 in .5 increments; seating shifts0/-.3; mesh tolerance.02/angular.1 | Hypotheses not hardware measurements; compare against J1 to prevent hiding new interference. Additional guessed-body contact reported separately |

### J1 isolated round-lip test parameters

| ID | Choice (mm) | Source / limitation |
|---|---|---|
| J1-CAP | socket 2.01 square, roof5.30, neck Ø5, bottom3.40; flange Ø10.4 × .4 at3.40; ball Ø7 centre8.5 | Original D6-SOCKET baseline; flange and shorter ball are original trial choices, not measurements |
| J1-LID | round hole Ø8, outer disk Ø20, underside4.4, thickness.7; two feet x=±9, width2, y length6, PCB contactz0 | Original hand-held test gauge, not production lid. Local top5.1 =3.05 above glass; surrounding production lid remains undecided. Feet establish height on bare PCB beside joystick; fit needs checking |
| J1-CHECK | tilt0/5/10 degrees; pivotsz0/3; press0/.3; eight compass directions | Stress scenarios only, not measured travel. Preserve failures in report. Print mesh tolerance .02, angular .1; separation5 on plate |

### D8 rear-tab experiment (historical, rejected)

Original follow-up after side tabs failed10-degree tilt. No hardware values changed.

| ID | Choice | Rationale |
|---|---|---|
| D8-JOY | single rear arm, width2.4, y/z relative profile [(1.8,8.7),(2.7,8.7),(6.3,5.1),(6.3,2.5),(7.8,1.0),(7.8,.7),(7.0,.7),(7.0,1.3),(6.0,2.1),(5.8,2.1),(5.8,4.8),(1.8,8.5)] | reaches behind PCB edge so low tab can tilt below PCB plane without entering board; original socket/neck unchanged |
| D8-POCKET | opening x±6.4, y-6.1..+6.9, R.8; rear pocket x±2.5,y+5.5..+8.3, z-1.5..2.6 | clears rear arm and tab motion, retains tab in lid; extends into base inner end wall, leaves outer wall intact |

D8 clearance refinement: opening rear edge+7.4 (centre+.65, length13.5),
pocket ceiling2.45. Upper heel ramp passes (6.3,2.5),(7.3,1.0),(7.8,1.0);
lower return passes (7.8,.7),(7.0,.7),(7.0,1.15),(6.6,1.7),(6.0,2.1).
Adds clearance at the one full-tilt/press PCB contact found in the earlier
trial. Heel capture tested at1.5 mm upward travel. Thin arm/heel junction
must be inspected in slicing; strength is not established.

V8 retains ALL 0/5/10-degree lid checks as required, adds base/PCB and
rear-arm/fixed-hardware checks at all sampled poses; only inherited neck
versus guessed body intersections remain diagnostic. Screen depth <=1 mm
is a required assertion. Current cap retention pull-up check is1.5 mm.

User requires lid no more than1 mm above glass. Previous uniform raise is
rejected. These are original design trials, NOT new hardware measurements.

| ID | Choice | Reason / limitation |
|---|---|---|
| D7-LID | top=S3+1.0=3.05; plate above glass-clearance plane .70 | screen-depth hard limit; no boss |
| D7-JOY | retain previous socket/neck/ball; two side arms, y thickness2.4; right x/z polygon relative to stem [(1.8,8.7),(2.7,8.7),(7.1,4.3),(7.1,1.1),(6.3,1.1),(6.3,4.0),(1.8,8.5)], mirror left; lip tabs x6.3..8.3, y±1.2, z1.1..1.5 | bypass guessed metal body; upper arms expand gradually in inverted printing; test motion, not assumed adequate |
| D7-POCKET | joystick opening15.4×12.2, R.8; underside tab pockets span x±8.8, y±2, ceiling2.4 | ball and upper arms pass opening; side tabs retained; front edge .43 from screen window |
| D7-BUTTON | flange bottom1.8, thickness.4; plunger contact roof2.61; underside switch relief width B2+.5, depth B1+.5; footprint and protrusion inherited | hidden side wings pass beside switch, rather than flange above plunger; flat top printing planned |
| V7 | required trial5-degree tilt, .3 press, pivots0/3; retain10-degree scenarios as diagnostics; cap upward .95 | actual joystick travel is unmeasured; larger-angle clearance must not be falsely claimed |

Austin reports V2 USB alignment good but rejects the tall lid fin/tab and
gaps. Requests V1-style closed port, earlier joystick interface plus V2 ball,
internal retaining lip, flat support-free lid. Uniform extra case height is
allowed if needed; buttons must maintain protrusion. Browser approval before
printing. No new physical measurement supplied.

| ID | Choice | Source / limitation |
|---|---|---|
| D6-SOCKET | square2.01, roof z5.30, bottom z3.40, neck Ø5 | repository's original full-case test2 commit4010773; both earlier submitted caps used2.01 square and roof5.30, but first lid-only cap had bottom4.00 and neck7.8. Exact physical V1 cap source still unconfirmed; select full-case baseline explicitly, not a proven identification |
| D6-JOY | ball Ø7, centre11.4 retained; flatten top .8 for inverted bed contact; flange Ø10.4, bottom5.0, thickness.6; upper flange 45-degree taper from radius5.2 at5.6 to radius2.5 at8.3 | original support-avoiding construction; lower socket unchanged from selected earlier CAD |
| D6-LID | whole flat lid top8.6; joystick pocket Ø13, ceiling7.4; throat Ø9.6; roof1.2; buttons protrude1.8; screen-side pocket wall .4 | uniform lid4.0 higher than V1/V2 flat face, no local boss; clipped pocket keeps a thin wall to screen; inspect wall in slicing |
| D6-USB | closed rectangular base port at V2 bounds, existing cable recess, no lid fin | user reports alignment works; restores closed-port topology, assembly now USB-first rather than straight drop of connected stack |
| V6 | cap pull-up1.55; tilt scenarios inherited; USB-first separate Pico path: rotate0 to -12 degrees around shell-front centre, retreat1.8 in y, lift30; steps2degrees/.3mm/selected lift heights; full lid bed area >300 square mm; flat top tolerance .001 | diagnostics not physical validation; actual USB-first assembly and support-free slicing require review |

Austin authorizes scan-based estimates and iteration (2026-09-24).

| ID | Value | Source / rationale |
|---|---|---|
| PINK-BTN-SCAN | component-face button centre offsets: lateral v=-3.2868, USB-ward u=13.4370 mm from PCB centre; detected light pad bbox 51×70 pixels | scan01 at 23.665753 px/mm; tools/measure_scan.py pink board fit; plunger centroid crop-local (294.0667,409.7847), full scan (1294.0667,859.7847). Scan is readable, not itself mirrored. Component face is opposite LCD front, so installed CAD x=-v, y=u. Registration remains a fit-test estimate. |
| D5-ACCESS | hole Ø4.0; button proxy Ø2.4, height 1.8 below component face | hole around scan pad, tool clearance; proxy height is a GUESS, not measured; no reset-function claim |
| D5-BUTTON | post x=4.2, y=5.4; flange x=4.85, y=6.3; proud=1.8; clearances/radii inherited | widen perpendicular to button row, avoid neighbour collision; reduce row-axis lip from .4 to .325; rectangular post cannot enter turned 90 degrees |
| D5-USB | selected shell stand-off=2.41 (A1_USB-A1_PCB); clearance .35 each side; outer cable recess height6.0, width12.5 unchanged | V1 photo shows socket above hole; choose higher of conflicting recorded placements, not a fabricated caliper update. Centre .42 higher than R4, .84 higher than P15-only model; shell aperture now 9.57×3.71. P15 still governs conservative floor depth. Actual cable fit needs print test. |
### J3 / L1 lowered flat trial — 2026-09-25

| ID | Value | Source |
|---|---|---|
| J3-SOCKET | Round diameter 3.50, depth 1.10; square 2.01 wide, next 2.00 deep | Austin's explicit J2 fit feedback; square retained from J2 |
| J3-LIP | Lip top approximately S3 + 0.40 | Austin's visual estimate, own IMG_0828; not calibrated |
| L1-FACE | Outer face z4.20; joystick underside z3.50 | Original trial choice: 0.90 lower than V3 flat; 0.70 joystick roof; 0.64 roof over retained button pockets |
| L1-KEEP | Base, snaps, holes and button pockets unchanged; joystick outside unchanged | Original design choice, isolate height and socket changes |
| L1-PLATE | 5 mm separation between print parts | Original plate layout choice |
### L2 roof translation — 2026-09-25

| ID | Value | Source |
|---|---|---|
| L2-DROP | 1.00 mm below L1, entire roof thickness retained | Austin explicit fit-trial instruction, supersedes 1.50 mm request |
| L2-JOIN | Preserve original lower geometry through S3 + GLASS_CLEAR; translate upper geometry down, union | Original construction choice preserves base mating and PCB contacts, shortens walls |
| L2-RESULT | Face z3.20, joystick underside z2.50, button underside z2.56 | Derived from L1 minus L2-DROP; roofs remain 0.70 and 0.64 mm |
| L2-CAP | Exact J2, circle 3.00 × 1.00 then square 2.01 × 2.00 | Austin selects prior joystick unchanged |
### L3 alignment — 2026-09-25

| ID | Value | Source |
|---|---|---|
| L3-HOLE | Shift opening 1.00 mm toward LCD (CAD Y minus 1.00); diameter remains 8.00 | Austin's physical fit instruction and own IMG_0831/0830/0829; direction confirmed, amount chosen from his request |
| L3-KEEP | Restore L1 face z4.20, joystick underside z3.50; keep original pocket, button geometry and mating skirt | Austin requests previous height and hole-only correction; original construction choice leaves lip pocket unchanged |
### L4 halfway-back correction

| ID | Value | Source |
|---|---|---|
| L4-OFFSET | From original centre: X +0.30, Y -0.50 mm | Austin requests halfway back from L3 and slightly photo-up; +0.30 trial choice. Photo LCD-right maps up to positive CAD X |
| L4-KEEP | L1 height, 8 mm aperture, existing pocket/skirt/buttons | User hole-only refinement; retain L3 non-aperture geometry |
### S1 lower-seam strong shell — original design choices

| ID | Value | Source |
|---|---|---|
| S1-SPLIT | Z_BOTTOM + (L1.TOP - Z_BOTTOM)/3 = -12.36 | Austin requests visible top 2/3, base 1/3; existing total shell height retained |
| S1-WALL | 3.00 mm, extra 0.80 outward per side; outer radius 3.80 | Original strengthening choice; preserves internal board clearance |
| S1-JOINT | Overlap 3.00, socket wall 1.40, radial gap 0.20, axial gap 0.20, male wall 1.40 mm | Original hidden overlapping joint; no exterior flex slots |
| S1-SNAP | Four ramped bumps, width 6.00, height 1.20, radial projection 0.35; centre seam+1.50 | Original trial internal detents; 0.15 nominal flex after mating clearance, not strength-tested |
| S1-RECESS | Blind recess depth 0.35, end clearance 0.30, height clearance 0.15 | Original hidden catch pockets; minimum outer skin 1.05 mm |
| S1-SUPPORT | Side support rails floor to LCD-back, 0.25 gap from upper inner walls | Original base-carried rails replace old wall-supported shelves, retain PCB height and permit lid installation |
| S1-PRY | One left long-side notch at seam, 6 wide, 1.6 high, 1 deep | Austin requests one opening notch; prior notch dimensions reused |
| S1-FACE | L4/L1 z4.20, all control pockets unchanged; extend solid perimeter outward | Preserve fitted roof/controls; strengthen with continuous 3mm perimeter/deep walls, no local boss |
| S1-PLATE | 5 mm minimum layout gap; 7 parts, no scaling | Original plate arrangement for approved S1 full-set print |
### S2 base retention / tactile buttons — original trial choices

| ID | Value | Source |
|---|---|---|
| S2-FEEDBACK | About 0.25 mm visible base drop; opens too easily; buttons indistinct | Austin's physical observation, approximate, not caliper reading |
| S2-CATCH | Projection 0.50 vs S1 0.35; underside 0.04 above existing pocket bottom; vertical nose 0.30; ramp to original bump top | Original trial to reduce axial slack and improve holding; nominal socket flex 0.30, pocket radial spare 0.05 mm |
| S2-BUTTON | Top z6.90 vs6.40, top-edge rounding radius1.20; unchanged4.2×5.4 post and4.85×6.3 flange | Original trial tactile profile, +0.50 mm height, narrower top contact surface |
| S2-KEEP | Same S1 lid, shell body, rails, USB/reset/pry, J2 joystick, button centres/flanges/contact planes | Minimize reprints; no hardware datum changes |
| S2-PLATE | 5mm spacing; base plus four buttons, floor/flanges down | Original plate arrangement; PLA0.16,4walls, no supports/raft |
### V1.0 production nudges — Austin's final physical test of S2

| ID | Value | Source |
|---|---|---|
| V1-FEEDBACK | S2 base + S2 buttons on S1 lid with J2: "This works." Snap and buttons accepted | Austin, 2026-09-25, hands-on test of printed parts |
| V1-NUDGE | 0.25 mm per nudge | Austin's estimate ("just a hair ... quarter millimeter"), not a caliper reading |
| V1-JOY | Joystick throat +0.25 y (toward USB-C end, away from LCD); x unchanged. Centre now (13.4671, 45.8792) | Austin's feedback + photo IMG_0848 (direction only, no dimension taken) |
| V1-USB | USB-C aperture and outer plug recess +0.25 z (toward lid); size unchanged. Aperture z -18.00 to -14.22 | Austin's feedback + photo IMG_0844: receptacle touches top edge. Bottom clearance to modelled shell drops 0.35 → 0.10 |
| V1-RESET | Base reset hole -0.25 y (away from USB-C end, toward centre). Centre now (16.5068, 39.4370) | Austin's feedback |
| V1-PLATE | 5 mm gap; 7 parts: lid face down, base floor down, J2 + four S2 caps flange down | Same arrangement as S1-PLATE |
### V1.1 USB-end spacer — Austin's PETG v1.0 test

| ID | Value | Source |
|---|---|---|
| V1.1-FEEDBACK | The board stack slides along the case. It lines up best pushed fully toward the buttons, with about 1.2 mm of play ("more than a millimeter") | Austin, 2026-09-25, hands-on test of the PETG v1.0 print; estimate, not a caliper reading. The CAD model shows only 0.6 mm of play (2 × CLEAR); his reading is used |
| V1.1-SPACER | Stop face 1.0 mm in from the USB-end inner wall (y 52.80 → 51.80) | His 1.2 mm, minus 0.2 mm left free so the rigid PCB cannot jam |
| V1.1-LIP | Lid lip between the rails, x 2.76–23.68, z -1.97 to 0 at the face, 45° chamfer to z 1.0 at the wall | Original; catches the LCD PCB edge, and the chamfer prints face-down with no support |
| V1.1-STOP | Base rail end stops, y 51.80–52.55, z -1.97 to -0.30 | Original; locates the board before the lid goes on, stays under the PCB front face |
### V1.2 half spacer

| ID | Value | Source |
|---|---|---|
| V1.2-FEEDBACK | The v1.1 spacer is in the right place but too big: the screen board no longer fits flush | Austin, 2026-09-25, v1.1 white PETG lid on the v1.0 base |
| V1.2-SPACER | 0.5 mm (half of v1.1); stop face at y 52.30; lip chamfer 0.5 | Austin: "let's try a half a millimeter" |
### V1.3 short USB end — replaces the V1.1/V1.2 spacers

| ID | Value | Source |
|---|---|---|
| V1.3-SHORTEN | USB-C end wall moved 0.5 mm inward on lid and base (outer face 55.80 → 55.30, inner face 52.80 → 52.30); case 59.10 → 58.60 long. No lip, no spacer | Austin, 2026-09-25: "Take the wall in. A half millimeter. Get rid of the lip." Amount from the v1.1 test (1.0 mm too much) |
| V1.3-L1-RECHECK | LCD hat length 52.46 (caliper, Austin, 2026-09-25, no photo). The model uses L1 = 52.50 | The 0.04 mm difference is ignored. v1.3 design inside length is 52.60 (v1.0: 53.10), leaving 0.14 mm on the design |
### V1.4 rounded edges — look trial

| ID | Value | Source |
|---|---|---|
| V1.4-FEEDBACK | Round the edges around the LCD and around the top so it looks better | Austin, 2026-09-26 |
| V1.4-TOP-R | 1.5 mm fillet on the lid's top outer perimeter | Original choice; under the 3.8 vertical corner radius |
| V1.4-WINDOW-R | 0.7 mm fillet on the LCD window's top edge | Original choice; under the 0.8 window corner radius |
| V1.4-R-REV3 | Top perimeter 3.0 mm (= wall thickness), LCD window 1.2 mm. They replace the 1.5 and 0.7 above | Austin: "round it a little bit more ... more rounded". A larger window radius fails, because the window step is only 0.7 mm tall |
| V1.4-WINDOW-IN | LCD window 1.0 mm smaller on every side: it was 0.4 mm past the glass edge and now covers 0.6 mm of the glass border | Austin: "the screen has some black, so we can encroach a little bit ... all the way around". The amount is an original choice; the border width is not measured |
| V1.4-GLASS-GAP | The bezel ring reaches down to 0.3 mm above the glass top (S3) | Original; gives the 1.2 mm rounding enough depth and cuts parallax at an angle |
### J4 flat-top joystick (v1.4)

| ID | Value | Source |
|---|---|---|
| J4-FEEDBACK | The fully round ball makes the joystick's press-in click hard to hit. Keep a ball, flat on top | Austin, 2026-09-26 |
| J4-FLAT | 5.0 mm flat pad cut from the J2 7.0 mm ball, 1.05 mm below the old top. Ball centre, neck, flange and socket unchanged | Original choice |
| J4-RIM | 0.6 mm fillet around the pad | Original choice, for comfort |
| J4-WAIST | The ball is cut where it has narrowed to 5.5 mm (J4 review 2; replaces J4-FLAT) | Austin: "a little hat ... comes to a top, then comes back out, then goes flat" |
| J4-HAT | A 45° flare from 5.5 to 7.0 mm, then a 0.6 mm disc edge; the top is 12.02, the same height as J2 (12.00) | Original. 45° prints flange-down with no support; 7.0 mm = ball width, under the 8 mm lid hole |
| J4-RIM-2 | 0.5 mm top edge; flat pad about 6 mm (was about 3.8) | Austin: "make it a little bigger" |
| J4-BALL | Ball 7.4 mm (J2: 7.0), cut flat through its centre: a half ball with a flat top all the way across. 0.3 mm rim edge break. The top is 3.7 mm below J2's | Austin: "make the ball a little bit bigger ... just barely fits through the hole ... at the widest part make it flat all the way across". Largest size without new lid contact in the J1-CHECK tilt scenarios: 7.6 and 7.5 graze the 8 mm hole at 10°/pivot z0; 7.4 leaves 0.3 mm each side |
### J5 — press-in room (v1.4 joystick)

| ID | Value | Source |
|---|---|---|
| J5-FEEDBACK | With the cap off, the stick's press-in click works. With the cap on it barely moves; up/down/left/right are fine. Make the socket narrow sooner so the cap rides higher | Austin, 2026-09-26 |
| J5-LIFT | Round mouth 1.0 → 0.7 mm (cap rides 0.3 higher); square 2.0 unchanged. The outside is identical to J4 | Original choice; press travel J9 still not measured |
| J5-VARIANTS | Test pair: lift 0.3 and 0.5 | In the J1-CHECK tilt scenarios the flange rim meets the roof underside at the hole: 0.5 is clear to ~6°, 0.3 to ~9°, 0.2 to 10°. The pair trades press room against tilt room |
