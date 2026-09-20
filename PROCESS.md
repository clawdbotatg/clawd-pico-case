# Process

Five phases. Each ends with a commit that says which phase it closes.

## Phase 0. Set up the room. Done 2026-09-19.

Repo, rules, this document, the empty measurement sheet. Written by an agent
session that had seen the forbidden designs earlier the same day, in another
repo. That session wrote no geometry and no dimensions except the Pico
datasheet values in `MEASUREMENTS.md`, each marked with its source. It is
logged in `PROVENANCE.md`. From here on, design sessions start fresh from this
directory.

## Phase 1. Measure.

Austin measures both boards with calipers and fills `MEASUREMENTS.md`. Three
readings per dimension, note the caliper, photograph anything not obvious.
Cross-check against the Pico and Waveshare drawings and write both numbers
when they disagree. Photos and drawing screenshots go in `measurements/`.

Also decide and write down in `DESIGN.md`:

- Which boards the case must fit. Pico 2 W with micro-USB. Any USB-C clone
  boards, measured separately.
- Whether the Pico stays plugged into the LCD's headers or is soldered.
- Whether there is a battery, a switch, a strap loop, a lanyard hole.
- Which surfaces must stay reachable: BOOTSEL, USB, reset if any.

Done when every row the design needs has a number and a source.

## Phase 2. Design.

A fresh session, started in this directory, builds the case in OpenSCAD from
`MEASUREMENTS.md` alone.

Order of work:

1. `scad/params.scad`. Every number, one line each, comment with the
   measurement row. Nothing else.
2. `scad/boards.scad`. A model of the two-board stack from the params. This
   is the thing the case wraps. Print a test frame that only checks the stack
   fits before drawing any case.
3. `scad/base.scad`, `scad/lid.scad`. Our own closure. Decide it in
   `DESIGN.md` before drawing: screws, snap, slide, magnets, friction. Give
   the reason.
4. `scad/caps.scad`. Button caps and joystick cap, from the switch and stick
   measurements. Our own profile.
5. `scad/plate.scad`. All parts laid out for one print bed.
6. `tools/build.sh`. Exports every STL. STLs in `stl/` are always rebuilt from
   source, never hand-edited.

Rules during design:

- No dimension enters `scad/` without a row in `MEASUREMENTS.md`.
- Any choice the hardware does not force is ours to make. Make it on purpose
  and write it in `DESIGN.md`: corner radius, wall thickness, lip, screen
  bezel shape, cap top shape, texture, branding.
- Commit small and often. The history is the evidence.

## Phase 3. Print and fit.

Print, try, log in `prints/YYYY-MM-DD-*.md`. Adjust params, rebuild, reprint.
Keep every version's params in git. Done when the full set prints on one
plate without supports, closes cleanly, buttons and stick work, USB fits.

Also test on the printer and material we would sell with. Log the slicer
profile.

## Phase 4. Release.

- Tag v1.0.0.
- Publish the STLs and the SCAD on Printables and MakerWorld under MIT, with a
  link back here and a copy of `PROVENANCE.md` in the listing.
- Product listing says "case for Raspberry Pi Pico 2 W + Waveshare
  Pico-LCD-1.3". Descriptive use of their names only. No Raspberry Pi or
  Waveshare logos on the part or in the listing images.
- Update the picowallet repo to point here, and mark its old `case/` folder
  as CC BY-NC, hobby use only.

## Proving it later

If anyone ever asks, the answer is this repo: dated commits, every number
traced to a caliper photo or a datasheet page, the design in readable source,
and a log showing which sessions touched it and what they had seen. Keep that
true at every step.
