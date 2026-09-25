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

Live sessions with the iPad camera on the bench, one row at a time: the agent
names the row, Austin measures and shows the caliper, the agent reads it,
saves the frame to `measurements/<ID>-<name>.jpg`, fills the row. Three
readings where it matters. Plan-view positions on the LCD hat come from a
1200 dpi flatbed scan of the bottom side, calibrated against a caliper
reading, if a flatbed is around. The Pico 2 W comes from the official Pico 2
STEP plus caliper rows for the wireless module and USB. Details and why in
`research/scanning.md`.

Also decide and write down in `DESIGN.md`:

- Which boards the case must fit. Pico 2 W with micro-USB. Any USB-C clone
  boards, measured separately.
- Whether the Pico stays plugged into the LCD's headers or is soldered.
- Whether there is a battery, a switch, a strap loop, a lanyard hole.
- Which surfaces must stay reachable: BOOTSEL, USB, reset if any.

Done when every row the design needs has a number and a source.

## Phase 2. Design.

A fresh session, started in this directory, builds the case in build123d
(Python code CAD, imports and exports STEP) from `MEASUREMENTS.md` and the
official Pico 2 STEP alone.

Order of work:

1. `cad/params.py`. Every number, one line each, comment with the
   measurement row. Nothing else.
2. `cad/pico.py`, `cad/hat.py`, `cad/stack.py`. The Pico from the STEP plus
   measured extras, the hat drawn from the rows, the two stacked at the
   measured gap. This is the thing the case wraps.
3. `cad/testframe.py`. A thin plate with the stack's outline, holes and
   cutouts. Print it. If the boards drop in and the buttons and stick line up,
   the model is right. No case until this passes.
4. `cad/base.py`, `cad/lid.py`. Our own closure. Decide it in `DESIGN.md`
   before drawing: screws, snap, slide, magnets, friction. Give the reason.
5. `cad/caps.py`. Button caps and joystick cap, from the switch and stick
   measurements. Our own profile.
6. `cad/plate.py`. All parts laid out for one print bed.
7. `cad/build.py`. Exports every STL and STEP to `stl/` and renders a PNG of
   each part and the assembly to `renders/`. Outputs are always rebuilt from
   source, never hand-edited.

Rules during design:

- No dimension enters `cad/` without a row in `MEASUREMENTS.md`.
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
- Publish the STLs and build123d Python source under MIT, with a
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

## R4 status correction, 2026-09-24

The actual implementation is params.py/model.py/build.py, with validate.py
and render.py. No official STEP was imported; all hardware proxies were
constructed locally. Current target is PINK, not P2W. Phase 1 and the physical
fit gate remain incomplete. R4 CAD corrections were explicitly requested by
Austin before those tests; preparing outputs does not close that gate or
authorize a production release. Use REPORT.md for the current test sequence.
