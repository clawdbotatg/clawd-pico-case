# Measurements

Every number the design uses lives here first. Rows have an ID. `cad/` cites
the ID. Blank means not measured yet. Units are mm.

Sources: `cal` = caliper on the bench, three readings, photo in
`measurements/` where useful. `ds` = datasheet or drawing, name the document
and page. When cal and ds disagree, write both and say which we use.

## P. Raspberry Pi Pico 2 W

Datasheet values below are from the Raspberry Pi Pico 2 W datasheet, mechanical
drawing section. Confirm each with calipers before Phase 2.

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

## C. USB-C clone board (pink), if we support it

| ID | Dimension | Value | Source | Notes |
|---|---|---|---|---|
| C1 | Board length | | cal | |
| C2 | Board width | | cal | |
| C3 | USB-C shell width | | cal | |
| C4 | USB-C shell height | | cal | |
| C5 | USB-C overhang past board edge | | cal | |
| C6 | USB-C centre offset from board centreline | | cal | |
| C7 | Mounting holes present and matching P4..P8 | | cal | yes/no |
| C8 | Tallest part above PCB, bottom side | | cal | |

## L. Waveshare Pico-LCD-1.3, board

| ID | Dimension | Value | Source | Notes |
|---|---|---|---|---|
| L1 | Board length | | cal / ds Waveshare drawing | |
| L2 | Board width | | cal / ds | |
| L3 | PCB thickness | | cal | |
| L4 | Corner radius of PCB | | cal | |
| L5 | Mounting hole diameter | | cal / ds | |
| L6 | Mounting hole positions, each, from one chosen corner | | cal / ds | list all |
| L7 | Female header socket height above PCB, Pico side | | cal | sets stack gap |
| L8 | Female header position from edges | | cal / ds | |
| L9 | Tallest part on the Pico side other than headers | | cal | |

## S. Screen

| ID | Dimension | Value | Source | Notes |
|---|---|---|---|---|
| S1 | Glass outline length | | cal | |
| S2 | Glass outline width | | cal | |
| S3 | Glass top height above PCB | | cal | |
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
| B5 | Plunger top height above PCB, at rest | | cal | |
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
| J6 | Stem top height above PCB, centred | | cal | |
| J7 | Stem tilt angle, full deflection | | cal / ds | |
| J8 | Stem top travel at full deflection, horizontal | | cal | |
| J9 | Centre press travel | | cal / ds | |
| J10 | Centre from chosen corner, x, y | | cal / ds | |
| J11 | Clearance around stem before it hits the body or nearby parts | | cal | |

## A. Assembled stack

| ID | Dimension | Value | Source | Notes |
|---|---|---|---|---|
| A1 | Total stack height, Pico bottom-most part to glass top | | cal | |
| A2 | Gap between Pico PCB top and LCD PCB bottom | | cal | should match L7 + P18 |
| A3 | Pico USB position relative to LCD board edges | | cal | |
| A4 | Anything sticking out past the LCD board outline | | look | |

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

Origin: not chosen yet.
