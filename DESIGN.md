# Design decisions — V2 print / R5 CAD

2026-09-24. Original MIT geometry from our own hardware measurements and V1
feedback. No third-party enclosure geometry. D4/D5 rows in MEASUREMENTS.md
distinguish our choices from hardware measurements.

Keep the existing footprint, stack height below the lid, USB insertion
channel/fin, four flexible snap bands, sloped shelves and four corner pads.
Austin says most of V1 is good; change only his five requested features.

## Captive joystick

Fit cap onto board before lid. Ø7 ball passes Ø8.8 throat; Ø10.4 flange
cannot, so it stays inside. Ø4.2 shaft, flange bottom z5 and thickness .8.
Motion pocket Ø13, ceiling z6.8, collar Ø15.8, roof1.2. Ball centre z11.4.
Raised collar clears chosen movement scenarios, but increases height and
requires support below the inverted lid face. Cap upright needs flange/
ball support review. Do not fill the socket with support material.

Socket1.91, engagement1.2, roof seated on tip. Only .2 nominal engagement
remains at the retaining stop; actual movement and retention need testing.
Fit samples1.86/1.96/2.06 remain available but are not part of the main print.

## Pry access

Two rounded 6 × 1.6 × 1-deep notches across the skirt/base seam, centred
on each long side between catches. R.5 and 1.2 nominal wall behind.
Clearance checked for a 4 × .6 plastic tip inserted .7. This establishes
tool access, not opening force or durability.

## Rectangular buttons

Posts4.2 along row ×5.4 perpendicular, flanges4.85×6.3, protrusion1.8.
Pitch limits row-axis widening, so broaden perpendicular to row. Smaller
row-axis lips (.325) and matching4.7×5.9 holes make the orientation clear:
rotating90 degrees cannot fit. Inherit .25 sliding gap and .8 flange
thickness; verify neighbouring clearance, measured .38 travel and retention.
Thin overlap, short guide and no overtravel stop still need tactile testing.

## USB-C correction

Select higher A1 stand-off2.41 instead of P15's3.25, consistent with the V1
photo's extra space below the connector. Keep P15 for conservative floor.
Aperture clearance .35 per side; outer cable recess height6 instead of7.
Opening centre .42 higher than R4 and .84 above P15-only placement.
This intentionally drops compatibility with the conflicting lower shell
position. Test actual cable/stack before further shrinking.

## Bottom button access

Use the existing pink-board scan, not a new guessed board layout.
Detected plunger at u13.4370,v-3.2868 relative to PCB centre. Component side
faces opposite LCD front; mirror lateral coordinate, retain USB-ward axis.
Ø4 floor hole at installed x16.5068,y39.6870. Scan is blurred and board
centering assumed; Austin explicitly authorized a fit-test estimate.
Proxy button height1.8 is unmeasured. Hole accesses this button without
asserting it is RESET rather than BOOTSEL. Use a nonconductive tool.

Physical print naming: photographed V1, next candidate V2. Internal CAD
revision R5 follows R4 and the saved r5-wip-joystick-pry checkpoint.
