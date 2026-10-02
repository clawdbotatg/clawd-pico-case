# Current: V3 fitted shells

J2 socket-first trial: preserve J1 exterior; roundØ3×1 deep then existing
2.01 square×2 deep, exactly as Austin requests. Print cap only before lowering
lid. Pending lowered-lid/hole-centre changes must not alter old print files.

SUPERSEDED by V3-FLAT: whole outer face atz5.1, print FACE DOWN, no supports
or raft. Austin explicitly allows greater screen depth for this trial.
Builder cad/v3_flat.py; reuse button/joystick geometry; lid-only correction.
See JOYSTICK-REVIEW.md for current status; upright plan below is historical.

Complete review and evidence: JOYSTICK-REVIEW.md. Builder cad/v3_fit.py.
Reuse V2 button caps and unchanged J1 joystick; only base/lid print.
Closed V2-aligned USB aperture, no fin; retain pry/reset. Low screen side
rails, local J1-height joystick roof and V2-height button deck. Upright lid
print intent, no supports/raft; mandatory slice review. Historical D7/D8
below are rejected designs, not the current print candidate.

# Historical V3 low-lid revision — D7/D8

Original MIT geometry from this repository's hardware measurements and
Austin's feedback. No external case geometry. Review only, no print approval.

Hard constraint: lid top is glass top +1 mm, z3.05. No joystick collar or
uniform case raise. The rejected tall draft remains saved in v3-review-1.

D7 side retaining tabs cleared5 degrees but failed16 ten-degree lid cases;
that unsuccessful experiment is saved in commit2587340.

D8 uses one rear arm/heel on the joystick cap. The heel is behind the PCB
edge, allowing downward tilt into a local interior pocket, without changing
case height. Earlier full-case4010773 lower socket/neck remain unchanged.
V2 ball diameter7 and small top print flat remain. The cap is still installed
before the lid. The rear heel's thin sections need slicer and strength review.

Button retaining wings now sit beside the switches, below the plunger tops.
The central underside contacts each plunger at measured z2.61. Outside cap
footprint and1.8 mm protrusion remain. Flat top-down printing is planned.

Keep V2-aligned closed USB port, no external lid fin, successful pry notches
and bottom access. Changes and all trial coordinates are recorded in
MEASUREMENTS.md. Required motion scenarios include the full10 degrees,
presses, both pivot assumptions and cap/base/PCB clearance. Inherited
socket/neck versus guessed metal-body collisions remain disclosed.

See reports/2026-09-25-low-lid-experiments.md. Browser review comes before
printing, and no new print artifacts have been produced for this revision.
# J1 isolated joystick test — 2026-09-25

See JOYSTICK-REVIEW.md for the complete current review packet. Original
round-lip cap plus hand-held lid gauge only; D8 rear arm rejected. J1 preserves
the selected V1 socket, has known10-degree motion failures, and is not sent
to the printer. Full-case geometry is unchanged.
## J3 / L1 trial — 2026-09-25

Widen round socket to Austin's 3.50 × 1.10 mm; keep square 2.01 × 2.00 mm
and exterior unchanged. Lower whole flat face 0.90 mm to z4.20, pocket roof
to z3.50. Existing buttons limit further lowering: 0.64 mm roof now remains.
No local boss, supports, USB fin, new base or new buttons. Lip height z2.45
is Austin's estimate for visualization, not proven seating. Iteratively find
motion limit then back off. Full details in JOYSTICK-REVIEW.md.
## L2 / J2 authorized physical trial — 2026-09-25

Move L1 upper roof down 1.00 mm, retaining roof thickness. Keep lower wall
geometry through original glass-clearance height and union translated upper
geometry; preserve contacts, mating skirt and snaps. Face z3.20, joystick
underside z2.50, button underside z2.56. Same base/buttons; exact J2 socket.
User accepts possibly unsuccessful fit; predicted overlaps remain in report,
not suppressed or counted as passes. Print face down with no supports/raft.
## L3 opening correction — 2026-09-25

L2 failed physical closure. Restore L1 thickness/height/pockets and shift only
round opening 1.00 mm toward LCD (CAD negative Y). Fill old throat crescent,
recut at new centre; retain 8 mm diameter and existing lip cavity. No base,
button or joystick changes. Print lid only, face down, supports/raft off.
## L4 alignment refinement

L3 physically overshot. New aperture centre is original X+0.30, Y-0.50:
halfway back from L3 and slightly photo-up with LCD on right. Keep diameter,
height and lip pocket unchanged. Photo-up magnitude is explicitly a trial
choice, not a calibrated measurement. Prepared lid only, not dispatched.
## S1 stronger walls / lower seam — review before printing

Austin's IMG_0834 shows exterior flexible bands and catch windows; he reports
bending during print removal. Replace these with continuous walls and blind
internal detents. Move visible seam to one-third of total height from bottom.
Make walls 3 mm by growing outward, preserving internal board clearances and
fitted control roof heights. A continuous thick perimeter/deeper walls are
intended to improve stiffness without lowering the control pockets again.

Joint uses 3 mm overlap, 1.4 mm socket wall, 0.2 mm gap, 1.4 mm tongue;
small bidirectional ramp catches allow removal without exposed flexible slots.
Minimum exterior skin at blind catches is 1.05 mm. One pry notch remains.
Actual strength, release force and cycle life require testing.

Transfer board support to two base-carried internal rails because the original
wall shelf would otherwise belong to the upper shell and obstruct assembly.
Retain USB port/reset location; extend outside cable recess to compensate for
added wall thickness. L4 opening offset retained. New matching shell pair;
does not fit old base. Interactive review requested; no printer dispatch.
## S2 closure and tactile refinement

S1 field feedback: loose vertical joint and indistinct button tops. Replace
base only: preserve body/rails/ports, swap symmetric triangular detents for
deeper catches with flat holding face, short vertical nose and insertion ramp.
Use existing lid-pocket lower edge to reduce nominal axial travel to0.04 mm;
projection0.50 consumes0.30mm socket flex and leaves0.05mm recess spare.
No claimed FDM accuracy or tested retention force. Small catch overhang needs
slice review. Keep existing lid/pry notch; no new exterior slots.

Caps retain V2 interface, gain0.50mm height and1.20mm rolled top edges to
separate finger contact areas. No change to button spacing or flange height.
Print five parts in PLA; defer PETG/colors until fit iterations finish.
## V1.0 production — final nudges

S2 passed Austin's hands-on test, so the design is frozen apart from three
0.25 mm nudges. Each one moves an opening and keeps its size, so nothing else
in the fit changes. Joystick throat: +y, away from the LCD. It uses L4's
method: fill the old throat through the roof, then cut the new one. The pocket
underneath does not move. USB-C aperture and plug recess: +z. Both stay under
the seam, so the lid needs no change there. The bottom clearance to the
modelled shell drops to 0.10 mm, which is fine because the photo shows the
real receptacle sitting high. Reset hole: -y. Each opening is refilled only
inside the original wall or floor before it is recut, and a check shows
nothing else changed. The buttons and J2 are byte-identical to the tested
parts. PETG shrinks differently from PLA, so the first PETG set is also a
fit check.
## V1.1 USB-end spacer

The v1.0 PETG test showed the stack sliding along the case, and it lines up
best pushed toward the buttons. The holes are therefore right for that
position, so the fix holds the board there and leaves every opening alone.
The USB-end stop face moves 1.0 mm inward: Austin felt about 1.2 mm of play,
and 0.2 mm is kept free so a rigid PCB cannot bind. The model predicts 0.6 mm
of play, so the real board or print differs from the model; his hands win.
The rails would block a full-width lid wall, so the stop is split in two. The
lid gets a lip between the rails that catches the LCD PCB edge; its 45° top
prints face-down with no support. The base gets end stops on top of the rails,
so the board is located before the lid goes on. The USB plug already works
with the board pushed this way, so the plug recess is unchanged.
## V1.3 short USB end (replaces the V1.1/V1.2 spacers)

The spacer added parts (a lid lip and base stops) and still needed both
halves reprinted. Moving the end wall in does the same job with less: the case
gets 0.5 mm shorter, there is no inner lip, and the USB plug sits 0.5 mm closer
to the port. The whole end is rebuilt from the moved datums, so the corners,
the tongue and socket, the rail ends (0.25 mm gap kept), the USB slot and the
plug recess all follow. Everything else is unchanged from v1.0, and a check
confirms that.
## J10 joystick set — 2026-09-29

A direction push on some devices clicks twice. The flange edge behind the push
rises into the lid underside, pivots there and drives the stem down into the
centre switch. Austin wants a joystick-only fix, so the lid is unchanged.
Four caps, numbered I-IV on top, each keep J9's socket and top and change only
what sits under the lid. I and II swap the full disc for four tabs. A tab off
the push axis rises less than the disc rim directly behind the push. I puts
them on the socket diagonals, II on the flats; the stem's turn on the board
is not measured, so one of the two lands on the diagonals. III and IV ride
0.2 lower for more room under the lid, at the risk of a stiffer press (why
J5 raised it). The model gives the tabs 2-3 degrees more tilt before the lid
is touched; the true tilt and seating are unmeasured, so the print decides.
Numerals are engraved, not raised, so the top still feels flat.
## J11 square flange — 2026-09-30

J10 failed: tabs reaching 0.6 past the hole slip through it. Austin's
direction: keep J9 and make its flange a square, thin toward the four push
directions with the corners on the diagonals. The edge behind a push is then a
flat side, which rises less than the old disc rim; the corners sit off the
push axes and still hold the cap in the hole. Two sizes (8.0 and 7.2 across the
flats) and both turns against the socket, because the stem square's turn on
the board is not measured. The pair whose flats face up/down/left/right is the
right turn. A flange that drops lower past the switch body is deferred: it
needs the body height, and it would stop the underside printing flat.
## J12 ride height on J11-III — 2026-09-30

J11-III cured the double click, but the centre press is hard to get without a
direction: the cap sits too low on the stick. J12 raises it the J5 way, with a
shallower round mouth, in four 0.1 steps (V-VIII). Riding higher gives the
press room but lifts the flange toward the lid again, so the set spans both
ends: VIII is back near J9's lid clearance in the model. Austin picks the
lowest one whose centre press is clean.
## J13 split press room from lid room — 2026-09-30

Ride height alone trades press room against lid room, and the working window
sits between VI and VII. The underside of the cap sets press room; the flange
top, where it sits under the lid, sets lid room. J13 thins the flange only
under the lid (0.24 from the hole edge out), so a cap can ride VII-high with
more lid room, and the underside still prints flat on the bed. A smaller square
can't help: its corners must reach past the hole. Round discs just past the
hole close the see-through gap the square leaves; in the model only the 8.6
disc beats VII, and it overlaps the hole by 0.3, so it may be loose. Letters
replace numerals.
## J14 stick fit on J13-O — 2026-09-30

O won J13 on a rough print. J14 prints it clean in three grip sizes around
its 1.90 square (1.85 / 1.90 / 1.95), everything else identical, so the next
test shows both whether O repeats and which grip holds best. Dots replace
letters because small engraved letters print as blobs.
## J16 hard stop and pull-out flares — 2026-09-30

J15's round mouth let the cap slide over the stem's base lip when pushed hard,
and its 0.3 overlap let a hard pull take it out of the lid. J16 cuts the square
grip all the way to the bed face, so the lip stops the cap, and adds four
narrow thin flares on the diagonals. The flares must stay short and thin:
material far out under the lid is what gets caught when the cap tips (the
8.6 disc edge slides into the hole instead), so the chosen flares keep VI's
lid room in the model while reaching 0.8 past the hole.
## J17 gradient on J16 — 2026-09-30

Bigger tabs hold the cap in the lid but get caught under the lid when it tips;
a shallower hole gives a better centre press but lifts the flange toward the
lid. Both push the same way, so J17 walks one path from J16 (tested clean) to
a cap the model is sure double-clicks, in five steps. Austin picks the step
with the best hold and press that still clicks clean.
## V1.8 test: more room for the flange — 2026-10-01

The flange holds the cap in and also causes the centre click when it tips into
the lid. J22's tabs sit on the diagonals, so a diagonal push lifts one straight
into the lid, and they are already too small to hold against a hard pull. The
two needs conflict under the v1.7 roof, so the test gives the flange more room:
lid only (bases unchanged), 0.3 and 0.5 taller, with two J23 caps that hold
harder. A TEST: stl/current stays v1.7 + J22 until Austin picks.
## V1.9 test: screen gap and logo inlay — 2026-10-01

The +0.3 lid works with J22. Two leftovers: the bezel ring had ridden up with
every lid stretch to 1.1 above the glass, so it is filled back to its designed
0.3; and a logo is inlaid in the top face. Face-down printing makes an inlay
natural: the logo is a separate flush part, the slicer prints its first two
layers in a second filament and the lid closes over it. A raised logo would
float the face; an engraving would print as blobs. Still a test.
