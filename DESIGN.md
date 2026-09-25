# Design decisions

Filled in during Phase 1 and Phase 2. Each entry: the choice, the reason, the
date. Choices the hardware does not force are ours. Make them on purpose.

## Requirements (Phase 1)

- Boards supported: **PINK** (USB-C RP2040 clone) only, for now. Austin,
  2026-09-24. The official micro-USB Pico 2 W is a later base if wanted.
- One case for all boards, or one base per board: one case, one board (above).
- Pico plugged or soldered: plugged into the hat's female headers.
- Battery / switch / strap: none.
- Must stay reachable: USB-C, screen, four buttons, joystick. BOOTSEL: TBD
  (a hole in the back, or open the case).
- Printer: Bambu Lab P2S, 0.4 mm nozzle, textured PEI plate. Material TBD
  (PLA for the test frame).

## Closure (Phase 2)

- Method: **snap fit**. Austin, 2026-09-24.
- Reason: Austin's call. No hardware to buy or insert, prints in one go,
  no screw heads. Cost: the lips wear; design them thick enough, add a
  pry slot so opening it doesn't break them. Details when drawn.

- Snaps (2026-09-24): four wedge bumps on the base tongue, two per long side,
  0.5 out, 8 long, flat catch face below and a ramp above. They catch windows
  cut through the lid skirt. Windows, not blind notches, because a 0.5 notch
  in a 0.8 skirt leaves 0.3 of skin; and a window lets a fingernail push the
  bump in to open the case. (First build cut the notches on the wrong side
  and they removed nothing; found in the 2026-09-24 audit.)

## Walls, corners, bezel

- Split at the LCD PCB front face: the lid carries every opening, the base
  only the USB-C. Both print flat with no supports.
- Wall 2.0, lid skirt 0.8, so the tongue is 1.2 (3 perimeters at 0.4).
- Floor 1.6. Lid plate 2.25 over the glass, 0.3 air above the glass.
- Outside corners R3.0. Pocket inside corners R0.8, which clears even a
  sharp PCB corner (L4 is unmeasured).
- Screen window = glass + 0.4 each side.

## Caps

- Buttons: square 4.2 post, R0.8 corners, 1.0 proud of the lid, in a 4.7
  hole. 5.3 flange 0.8 thick under the lid rests on the plunger, so the cap
  cannot fall out; 0.15 air above the flange. 1.0 web between holes.
- Joystick: round cap, square blind socket 1.86 + 0.15 on the stem, top disc
  0.5 past the hole. Hole 10.5. Height and tilt clearance depend on J3/J7,
  both unmeasured.

## Branding

None yet.

## Tolerances

- 0.3 PCB to wall. 0.25 per side cap to hole. 0.5 around the USB-C shell.
  First guesses for a P2S in PLA; the T rows in `MEASUREMENTS.md` get the
  real numbers from test prints.
