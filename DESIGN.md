# Design decisions — current R4

2026-09-24. Original enclosure for the measured PINK USB-C RP2040 board,
plugged into the Waveshare Pico-LCD-1.3. No battery, switch, strap or logo.
Official Pico W/Pico 2 W compatibility is not established. Earlier decisions
are retained in git history. R4 values cite D4 rows in MEASUREMENTS.md.

## Construction

Keep the rounded rectangle, user-requested snap closure, four individual
square caps, and capped joystick. Split at the LCD front plane, z=0.
Floor 1.60, clearance under deepest recorded component 0.30. Lid outside
z=4.60. Glass clearance 0.30; window follows full glass plus 0.40 per side
because active-area dimensions are unmeasured.

Body 31.44 × 57.50 × 25.24; cap-inclusive height 28.54 mm. Wall 2.20,
skirt 0.80, mating clearance 0.20, tongue 1.20. Outside R3; pocket R0.50.
Sharp rectangular PCB also tested at ±0.10 XY displacement.

## Closure and insertion

Four 4 mm ramped bumps engage lid windows. Projection 0.45 minus mating gap
0.20 gives 0.25 engagement. Slits define four 14 mm skirt bands attached at
both ends, allowing outward flex and plastic-tool release. Bridging, force
and fatigue require a print. Free-ended horizontal arms were rejected
because they would begin in air with the lid printed inverted.

USB channel extends to the base rim for vertical insertion of the connected
stack. A lid fin closes it above the socket with 0.25 side clearance.
Square aperture contains both recorded shell heights. Inherited 12.5 × 7.0
plug recess, depth 1.0, remains provisional.

## Support and controls

Side shelves carry LCD PCB with 45-degree undersides and 0.80 bearing
strips. Four 1.60 corner pads, inset 0.50, limit lift to nominal 0.05.
They sit over the shelves, outside modelled switches. Verify bare PCB
landing areas and underside solder clearance physically.

Button posts 4.20, R0.80, holes 4.70. Flanges 5.00 × 0.80 avoid collision
at opposite lateral limits. Contact at measured plunger z=2.61; tops 1.00
above lid. Pocket allows 0.15 upward motion. Measured press travel 0.38
checked. Short guides, retention overlap and absence of an overtravel stop
require tactile testing. Individual scan y offsets retained.

Joystick: Ø12.80 opening at stem centre; silver body uses its separate scan
centre. Ø14 disc, 1.50 thick, gap 1.80 above lid. Ø5 neck engages 1.20 of
the square stem; socket roof seats on tip. Default socket 1.91; trials
1.86/1.96/2.06. These are printer fit samples, not a proven press fit.
Shorter engagement avoids assumed body in tilt/press scenarios but increases
the importance of retention testing. No glue specified.

## Printing and acceptance

Base upright; lid/joystick inverted; buttons flange-down and separated on
the bed. Existing P2S / 0.4 nozzle / PLA / 0.16 layer trial profile.
Inspect bridge toolpaths and first-layer expansion. Final material undecided.
BOOTSEL accessed by opening the case until its location is measured.

Release requires no board preload, independent return of all controls,
retained caps, full cable insertion, repeated snap release without damage,
and physical tests in the selected final material/profile. See REPORT.md.
