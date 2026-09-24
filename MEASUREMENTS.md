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

### PINK rows: (copy the table, all cal, none from datasheet)

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
| L1 | Board length (y) | 52.68 | scan01 | ±0.3, confirm cal |
| L2 | Board width (x) | 26.58 | scan01 | ±0.3, confirm cal |
| S1 | Glass outline length (y) | 26.48 | scan01 | black glass as visible; ±0.2 |
| S2 | Glass outline width (x) | 25.19 | scan01 | ±0.2 |
| S4 | Glass centre x | 13.15 | scan01 | glass spans x 0.56 to 25.75 |
| S5 | Glass centre y | 26.05 | scan01 | glass spans y 12.81 to 39.29 |
| B4 | Plunger diameter | 2.63 | scan01 | fitted disc of the bright top only; a blurred lower bound, confirm cal |
| B8a | Button 1 centre (leftmost) x, y | 4.85, 4.14 | scan01 | |
| B8b | Button 2 centre x, y | 10.58, 4.00 | scan01 | |
| B8c | Button 3 centre x, y | 16.16, 4.02 | scan01 | |
| B8d | Button 4 centre (rightmost) x, y | 21.87, 4.12 | scan01 | |
| B8p | Button pitch | 5.67 | scan01 | mean of the three gaps |
| J4 | Stem diameter at top | 2.41 | scan01 | dark cap only, confirm cal |
| J10 | Joystick centre x, y | 13.24, 46.22 | scan01 | stem top; base centre agrees within 0.4 |
| J1/J2 | Joystick base plan size | 8.81 × 7.22 | scan01 | fitted to the silver diamond, blurred; confirm cal |

Not from this scan: every Z (L3, L7, L9, S3, B3, B5, B6, J3, J6-J9), hole rows L5/L6 (none visible from the top; back side scan was out of focus), and the switch bodies B1/B2 (blurred). The pink Pico and the two ATECC608 breakouts sat tilted on their connectors and only their outlines are usable: PINK 50.8 × 20.9 (under-reads, edge blur), ATECC608 about 27–28 × 18.5–19. Calipers for those.

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

## B. Buttons, four tact switches

Measure the switch, not a cap. Identify the part if you can from the marking or
the schematic and add its datasheet to `SOURCES.md`.

| ID | Dimension | Value | Source | Notes |
|---|---|---|---|---|
| B1 | Switch body length | | cal | |
| B2 | Switch body width | | cal | |
| B3 | Switch body height above PCB | | cal | |
| B4 | Plunger diameter | | cal | |
| B5 | Plunger top height above PCB, at rest | 2.61 | cal 2026-09-24 | Austin read 13.27 socket top to button top, minus L3+L7 10.66. `measurements/2026-09-24-cal-B5-lcd-button-height-1.jpg` |
| B6 | Plunger travel | | cal / ds | |
| B7 | Plunger shape | | look | round, square, with a shoulder? |
| B8 | Centre of each switch from chosen corner, x, y | | cal / ds | four rows, name them by silkscreen label |
| B9 | Actuation force | | ds | for cap weight and return |

## J. Joystick

| ID | Dimension | Value | Source | Notes |
|---|---|---|---|---|
| J1 | Body length | | cal | |
| J2 | Body width | | cal | |
| J3 | Body height above PCB | | cal | |
| J4 | Stem diameter at top | | cal | |
| J5 | Stem shape | | look | round, D, cross, keyed? |
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
| A1 | Total stack height, Pico bottom-most part to glass top | | cal | per tag |
| A2 | Gap between Pico PCB top and LCD PCB bottom | | cal | should match L7 + P18, per tag |
| A3 | Pico USB position relative to LCD board edges | | cal | per tag |
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
the bottom-left corner of the LCD PCB. +x to the right (26.58 wide), +y up
toward the joystick (52.68 long). The 600 dpi scan is not mirrored (the
rule's digits and the Pico's silkscreen read correctly), so scan x, y map
straight onto this frame.
