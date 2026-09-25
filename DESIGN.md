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
