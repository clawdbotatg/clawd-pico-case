# V2 print candidate / R5 CAD — 2026-09-24

Original MIT case for the measured pink USB-C RP2040 board and LCD hat.
[V1 feedback and photos](prints/2026-09-24-v1-feedback.md) drove five changes:

1. Smaller, taller ball joystick. Fits onto the board first; internal lip
   is captured when the lid passes over the ball.
2. Two seam pry notches for a thin plastic tool.
3. USB-C aperture higher and tighter.
4. Wider, taller rectangular button caps, keyed against sideways insertion.
5. Bottom tool-access hole aligned to the pink board button from its scan.

This is a fit-test candidate, not physically validated. V1's exact printed
commit remains unmatched. Internal CAD revisions and physical V1/V2 print
names are recorded separately in [ITERATIONS.md](ITERATIONS.md).

## Geometry and evidence

- Footprint 31.44 × 57.50 mm; flat lid z=4.60, raised joystick collar z=8.
  Body height including collar 28.64; ball-inclusive height 35.54 mm.
- Joystick ball Ø7, shaft Ø4.2, flange Ø10.4 × 0.8, throat Ø8.8.
  Socket 1.91 across flats, engagement 1.2. Neutral flange clearance 1.0
  leaves only 0.2 nominal socket engagement at the retaining stop.
- Side notches 6 × 1.6 × 1 deep, rounded R0.5, between catches; wall behind
  remains 1.2 nominal. Opening force remains untested.
- Buttons: posts 4.2 along row × 5.4 perpendicular; flanges 4.85 × 6.3.
  Stand 1.8 above lid (was 1.0). Holes 4.7 × 5.9 reject 90-degree insertion.
  Top/bottom lips in Austin's landscape photo shrink from .4 to .325.
- USB shell uses higher A1 stand-off 2.41, not lower P15 stand-off 3.25.
  Aperture 9.57 × 3.71; centre .42 higher than R4 and .84 above P15-only
  placement. Cable recess 12.5 × 6, depth1.0. Conservative floor unchanged.
  **Lower P15 shell placement no longer fits:** this is an explicit trial
  supported by V1's photo, not resolution of the conflicting measurements.
- Bottom hole Ø4 at x=16.5068, y=39.6870 in LCD-front coordinates.
  Derived from scan centroid with opposite-face lateral reflection; see
  [overlay](measurements/2026-09-24-pink-button-fit.png) and
  [estimate](measurements/2026-09-24-pink-button-estimate.json).
  Button identity/function and height remain unconfirmed. This provides
  access to that button; it does not establish that the button resets.

## Validation

Build runs required checks before exporting. Current results and source
hashes record **276 passed checks**. All seven print/sample meshes have
closed edges, no duplicate-vertex triangles and z-min zero. Current source
hashes: [validation.json](renders/validation.json). Checks include assembly
clearance, cap retention, full measured button travel, rectangular keying,
joystick scenarios, continuous lid installation over the mounted cap, USB
insertion, bottom tool path and pry-tool clearance. Joystick scenarios are
0/5/10 degrees, 0/.3 press, two assumed pivot heights, eight directions;
these are not measured movement specifications.

The exporter removes duplicate-vertex sphere-pole triangles and requires
two incident faces per mesh edge. Print/sample files have z-min zero.
[Manifest](stl/manifest.json) ties sources and artifacts together.
[Preview](renders/r5-preview.png), [viewer](renders/viewer.html).

No slicer toolpaths or physical fit have been validated locally. The printer
operator must inspect supports, bridges, tiny features and first-layer contact.

## Printing and assembly

See [V2 print log](prints/2026-09-24-v2.md) for exact dispatch status.
Print only stl/print, not the hardware proxies. One base, one lid, four
buttons and one joystick: seven pieces. Do not mix earlier base/lid/caps.

Base upright; lid inverted; joystick upright; buttons flange-down.
The raised collar lifts the inverted lid face off the bed: **support that
face**. Review supports under cap flange/ball; keep socket and control
clearances free. Separate the four button solids on the plate. Trial PLA,
0.16 layer, 0.4 nozzle, textured PEI. Actual slicer settings are pending.

1. Identify blue flag; inspect board support landings and solder clearance.
2. Gently seat joystick onto bare board stick; do not force the socket.
3. Put button caps inside lid. Lower lid over the ball: flange stays inside.
4. Mate base over connected stack; USB must pass its channel freely.
5. Check all button directions/clicks, joystick return and retained caps.
6. Try actual USB cable; inspect bottom-hole alignment before inserting a
   nonconductive toothpick. Do not blindly push a metal screwdriver inside.
7. Open using seam notches and a plastic tool. Stop if force is excessive.
   Record wear, whitening, cracks, rattle and unintended presses.

Unresolved blue flag intersects lid by 5.28 mm³. Do not close on or cut it;
remove only if confirmed removable protector packaging. Board stack datum,
USB projection, cable overmould, bare pad landings, solder, joystick body/
lip/pivot and snap fatigue remain unverified. [R4 audit](reports/r4-engineering-review.md)
preserves the full earlier measurement review; its old assembly instructions
do not apply to V2.
