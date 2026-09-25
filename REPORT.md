# R4 engineering review — 2026-09-24

R4 corrects the existing original design. It is a **fit-test prototype**, not
a validated product. It targets the measured **PINK USB-C RP2040 board** with
the Waveshare Pico-LCD-1.3. Official Pico W/Pico 2 W compatibility is not
established. No physical fit results have been recorded.

- [CAD preview](renders/r4-preview.png)
- [Interactive assembly](renders/viewer.html) (network needed for three.js)
- [Print parts](stl/print/) and [joystick fit samples](stl/fit_samples/)
- [Geometric check results](renders/validation.json)
- [Source and output hashes](stl/manifest.json)

## Findings and corrections

| Finding in test 2 | Why it matters | R4 response |
|---|---|---|
| Lid and tongue have coincident mating surfaces. | Zero intersection is not printable clearance. | 0.20 radial gap; wall 2.20, tongue 1.20, skirt 0.80. |
| Bumps require flexing a continuous skirt. | Static catch checks establish neither closing force nor release. | 4 mm bumps, 0.25 engagement, slits above four 14 mm flexible skirt bands. Force/fatigue need testing. |
| USB shell projects beyond base pocket. | Connected stack cannot drop vertically through the old end wall. | Open insertion channel; lid fin closes channel above USB. Continuous insertion envelopes pass. |
| Rounded USB slot checked against only one shell height. | Rounded corners can cut into a rectangular clearance envelope. | Square aperture checked against both recorded heights. |
| Flanges 5.30 wide, nearest pitch about 5.59, each cap slides 0.25. | Neighbours can collide when displaced toward each other. | Flanges 5.00; tests at opposite lateral limits. Smaller retention overlap needs print inspection. |
| Button y positions averaged; joystick body placed at stem centre. | Recorded offsets discarded. | Individual button centres and independent silver-body centre from scan JSON. |
| Ø12 joystick opening based on concentric body only. | Silver-body centre differs from stem by 0.505. | Ø12.80 opening, Ø14 disc. Actual body/tabs still unmeasured. |
| Joystick socket 0.15 oversized, roof 0.30 above tip. | No proven grip or axial seating datum. | Roof seats on tip; 0.05 nominal allowance plus three fit samples. Retention remains unverified. |
| Shelf starts with a 2.81 flat overhang. | Unsupported underside. | 45-degree underside and 0.80 bearing strip. |
| Only two top hold-down pads. | Button-end lift/rock insufficiently constrained. | Four corner contacts above side shelves, 0.05 nominal play; check bare landing areas. |
| R0.80 pocket marginal with sharp PCB corners. | ±0.10 diagonal shift produced corner interference. | R0.50 pocket checked against sharp PCB and XY sensitivity. |
| Report assigns success percentages and calls all readings photo-backed. | No basis for percentages; some photos miss the measurement. | Explicit evidence limitations and physical acceptance tests. |

## Evidence review

Reviewed repository instructions, measurements, reports/handoff, provenance,
both print logs, CAD/helper scripts, scan JSON, overlay, full scan, and all
23 caliper photographs. No other case files/listings were consulted.
Test-2 geometry remains in git at 4010773 and its print log at 28f6932.

Reproduced directly from HEAD's original CAD before revision: neighbouring
flanges at opposite lateral limits intersect by 0.258 / 0.712 / 0.326 mm³;
the vertical USB insertion envelope intersects the base by 172.701 mm³.
These are geometric failures of those specific poses, not estimates of
physical force or proof that no tilted assembly path could exist.

| Nominal plane | z, mm |
|---|---:|
| LCD PCB front | 0 |
| LCD PCB back / shelf | -1.97 |
| Pico face toward LCD | -14.26 |
| Pico component-side PCB face | -15.49 |
| Deepest USB shell using P15 | -18.74 |
| Inside floor | -19.04 |
| Outside floor | -20.64 |
| Lid top | 4.60 |
| Button top at rest | 5.60 |
| Joystick top | 7.90 |

Body: **31.44 × 57.50 × 25.24 mm**; overall height including joystick:
**28.54 mm**. Plugged headers drive most of this thickness. A substantially
thinner case needs a different measured electrical assembly.

The scan's absolute corner coordinates used its blurred 26.5835 × 52.6773
outline. CAD preserves centre-relative offsets against the caliper
26.44 × 52.50 outline (SC1/BC1/JC1/JC2), without rescaling feature spacing.
Scan-centre registration and glass orientation remain uncertain.

Photo limitations are recorded in MEASUREMENTS.md. L3 contains no measurement;
S3/B6 miss contact; L7 does not clearly substantiate the shared 10.66 datum;
B4/B2 digits differ slightly from recorded values. Austin's readings are
retained pending confirmation. Heights sharing the socket datum also share
its error; they are not independent high-confidence readings.

A1's glass contact is not unambiguous in its photos. Its 17.54 value sets A2
and the base depth. P15 and A1 additionally disagree by 0.84 on USB height.
Accommodating both USB heights does **not** resolve a possible stack-datum error.

PINK-P11's projection came from segmentation that also reports USB width
20.95, versus caliper 8.87. Its claimed ±0.2 precision is not established.
At nominal centring, the shell face is 0.76 inside R4's wall; the inherited
1 mm recess leaves 0.24 reach margin. Plug dimensions remain guessed at
12.5 × 7.0. Confirm the actual cable.

## What validation establishes

Run `.venv/bin/python cad/build.py` from the repository root. It runs the
geometric audit first and refuses export after a failed required check.
validation.json includes source hashes so results can be tied to the model.

Executed R4 result: **171 checks passed**. Independently read all seven
print/sample binary STLs: every undirected mesh edge has two incident faces,
and each file has z-min zero. Source and exported-output hashes match the
manifest. This mesh check does not replace slicer review. The unresolved
blue flag intersects the lid by 5.28 mm³ and is explicitly excluded from
required nominal-fit passes.

Checks cover solid validity/count; planar bed contact for every part;
nominal pairwise intersections; sharp PCB/XY displacement; nine button
positions through measured 0.38 travel; opposite lateral cap limits; upward
cap retention; continuous vertical board/USB insertion envelopes; sampled
lid approach; both USB heights; and positive snap engagement.

Joystick scenarios sample 0/5/10 degrees, eight directions, assumed pivot
heights 0/3, and 0.30 press against lid and fixed hardware. These are
**chosen scenarios, not measured joystick specifications**. Body height
remains guessed at 3.0. Lip/taper and socket retention are not verified.
Shortening engagement to 1.20 clears the assumed body in these scenarios,
but retention needs particular attention.

Checks do not prove snap force, creep, fatigue, drop resistance, cap
friction, printing accuracy, electrical function, or clearance of omitted
solder/components. No slicer toolpath was validated.

The blue flag still intersects the lid (reported separately in JSON).
Its identity is unconfirmed. **Do not close the case on it or cut it.**
Remove only if identified as removable protector packaging; otherwise the
enclosure needs a clearance feature.

## Print and assembly

R4 exports are local and **not sent to a printer**. Test 2 was sent according
to its historical log; the result remains blank. R4 base/lid are a matched
pair; do not mix them with test 2.

Start with the lid/caps against the loose hat. Base upright; lid and joystick
face-down; buttons flange-down. Print STLs already use these orientations
and z-min zero. Separate the four button solids on the bed to prevent
first-layer joining. Keep joystick samples identified by filename.

Trial profile: existing P2S / 0.4 nozzle / grey PLA / 0.16 layer. Inspect
bridging over the 14 mm latch slits and catch windows in the slicer. Bands
are attached at both ends to bridge when inverted; a free-ended horizontal
arm would start in air. Bumps retain small overhangs. Support-free success
and dimensional fit still need an actual print. Check the long lid fin for
straightness and adhesion.

1. Identify the blue flag and inspect four pad landings plus long-edge
   shelf strips for components/solder.
2. Try joystick samples gently on the bare stick, starting largest.
   Select light finger-pressure seating, free return, and retention when
   inverted. Do not force an undersized socket.
3. Lay lid face-down on a soft surface. Insert button caps from inside and
   check independent sliding and captivity.
4. Place the hat face-down into the lid, watching buttons and joystick.
   Leave the Pico connected to the headers.
5. Lower base over stack; its USB channel must pass the socket without
   loading header pins. Engage snaps progressively. Stop if force is high.
6. Turn upright, install chosen joystick cap, and compare all button,
   directional, centre and tilted clicks with uncased hardware.
7. Fully insert the actual USB cable and verify connection. Check gentle
   cable loads for board movement. Open the case for BOOTSEL access.
8. Release skirt bands outward through their relief slots using a thin
   plastic tool, lifting a side slightly as catches clear. Do not push
   rigid base bumps into the PCB. Log repeated opening, whitening/cracking,
   rattle, retention, and accidental inputs.

There is no separate button overtravel stop. The short guides and small
flange overlap need tactile testing; a motion check does not prove protection
against excessive pressing force.

## Inputs needed to finish

Most useful: the actual test-2 or R4 fit result. For remaining geometry,
capture both jaw contact points while measuring LCD PCB front to Pico
component-side PCB face; USB projection from hat edge and shell z extremes;
actual cable width/height; joystick metal body X/Y/Z, lip height, exposed
square length, full directional motion and centre press. Confirm bare
support locations and blue-tab identity.

## Originality and license

R4 uses this repository's measured hardware and original parametric
construction only. No third-party enclosure/cap geometry was imported or
consulted. MIT LICENSE is unchanged; provenance records this session.
Tools/viewer dependencies retain their own licenses. This is an engineering
record, not a legal clearance opinion or a product-release approval.
