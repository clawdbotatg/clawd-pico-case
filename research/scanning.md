# Getting real hardware into 3D. Research, 2026-09-20.

Question: can we scan the Pico and the LCD hat instead of measuring them, get an
exact 3D model, and build the case around it?

## Short answer

Not for the numbers that matter. Scan for the picture, measure for the fit.
The pro workflow for small electronics is: manufacturer CAD where it exists,
flatbed scan for the board outline and hole positions, calipers and part
datasheets for heights and buttons, then a CAD assembly of the stack, then the
case around that assembly. Test prints check it.

## What the options give you

| Method | Accuracy on a 50 mm board | Cost | Verdict |
|---|---|---|---|
| iPad LiDAR (Polycam, Scaniverse) | about 5 mm | free | Useless at this size |
| Phone photogrammetry (Polycam, Kiri, RealityScan) | 0.5 to 1 mm on a good day, worse on dark PCB and glass | free | Nice picture, not a fit reference |
| Desktop photogrammetry (Meshroom, RealityCapture) | similar; needs matte spray, dozens of photos | free | Same |
| Structured light or blue laser scanner (Revopoint MINI 2, Creality Raptor) | 0.02 to 0.05 mm claimed on a matte object | 500 to 1500 USD | Works, but needs scanning spray on the PCB and glass, and outputs a mesh you still have to redraw as solids |
| Flatbed document scanner, 600 to 1200 dpi | about 0.05 mm in X and Y, no Z | free if you have one | Best cheap trick for outline, holes, button and stick centres |
| Calipers | 0.02 mm | have one | Heights, diameters, travel. Slow but exact |
| Manufacturer STEP file | exact | free | Pico 2 has one. The hat does not |
| Component datasheets | exact | free | Tact switch and joystick drawings once the parts are identified |

Why scanners disappoint here: a snap fit or a cap in a hole cares about 0.1 mm.
Consumer scanners are 5 to 10 times worse than that on a small dark object, and
even the good ones give a noisy mesh, not the clean holes and edges CAD wants.
People who reverse-engineer parts with a scanner still redraw them as solids over
the mesh. For a rectangular PCB with round holes, drawing from measurements is
faster and more accurate than scanning and redrawing.

## What exists for our two boards

- Raspberry Pi Pico 2: official STEP model, "openly available with no
  limitations, for any purpose". Pico 2 W has the same outline, holes and USB
  position, plus the wireless module, so the Pico 2 STEP is the base and we
  measure the module height. URL in `SOURCES.md`.
- Waveshare Pico-LCD-1.3: no 3D drawing on the wiki. Only the schematic (no
  part numbers, switches are just SW3 to SW6 and "Joystick") and the ST7789VW
  controller datasheet. So the hat gets modelled by us from a flatbed scan,
  calipers and datasheets of the switch and joystick once we identify them by
  measuring. There is a community model of the hat on GrabCAD; it is someone
  else's work under GrabCAD terms, so we do not use it. Ours will be better
  sourced anyway.

## The pipeline we will use

1. Pico 2 W: import the official Pico 2 STEP. Caliper the wireless module
   height, the USB shell, BOOTSEL. Log rows P11 to P18.
2. LCD hat, plan view: flatbed scan the bottom side at 1200 dpi with a steel
   rule in frame. Calibrate the image against a caliper reading of board
   length. Read off outline, holes, and the centres of the screen, the four
   switches and the joystick. Log rows L, S8, B8, J10 with the scan as the
   photo. If there is no flatbed, calipers do it, slower.
3. LCD hat, heights: calipers for every Z. Rows L3, L7, S3, B3 to B6, J3 to J9.
4. Identify the tact switch and the joystick by body size and look, find the
   datasheets, add them to `SOURCES.md`, use their drawings for plunger and
   stem shapes.
5. Build the hat as a parametric solid in code CAD. Build the stack: Pico STEP
   plus hat, at the measured header gap (A2).
6. Print a test frame: a thin plate with the outline, holes and cutouts of the
   stack. Costs 5 g. If the boards drop in and the buttons and stick line up,
   the model is right. Only then draw the case.
7. Case around the stack. Iterate with prints, log in `prints/`.
8. Render every part and the assembly to PNG from the CAD source on every
   build, so the docs always show what the source says.

## Tool change: build123d instead of OpenSCAD

OpenSCAD cannot import STEP, so the Pico model would have to be redrawn.
build123d (Python, same kernel as CadQuery and FreeCAD) imports and exports
STEP, exports STL and 3MF, and can render PNGs headlessly. It is code, so it
diffs in git and an agent can drive it. Same clean-room rules: every number
comes from `MEASUREMENTS.md`. Install with `uv` in this repo.

## Live measurement sessions

Austin points the iPad camera at the bench. One measurement at a time:

1. Agent names the row, say "S1, glass length, calipers across the long side of
   the glass".
2. Austin measures, holds the caliper display to the camera, says the number.
3. Agent reads the display, confirms it matches what Austin said, saves the
   frame as `measurements/S1-glass-length.jpg`, fills the row, notes anything
   odd.
4. Three readings when it matters. Commit every few rows.

That gives every row a photo and a sentence, which is the paper trail we want.
