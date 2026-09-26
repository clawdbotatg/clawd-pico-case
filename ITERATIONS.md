# Design and print iteration register

## J2 stepped joystick socket — 2026-09-25

cap only, unchanged J1 exterior, deeper round-to-square bore per Austin.
Source cad/joystick_j2.py; STL stl/joystick-j2; checks renders/joystick-j2.
Physical seating trial precedes lowered lid/hole-centre adjustment.

## V3-FLAT — 2026-09-25

Correct upright-print failure: uniform outer lid facez5.1, face-down STL,
supports/raft OFF,699 checks. Existing buttons still1.3 mm proud. Lid only;
no cap/base reprint. Sources cad/v3_flat.py, artifacts stl/v3-flat and
renders/v3-flat; print log prints/2026-09-25-v3-flat.md. Austin explicitly
allows whole-face height increase for fitting. Upright revision preserved.

Every saved design revision belongs in git with its original CAD, generated
STL/STEP files, rationale, evidence and validation results. Print jobs must
reference an immutable commit/tag and record slicer settings, artifact hashes,
delivery/start status and the eventual fit result. Never replace a failed
version's history with a corrected version or describe a queued job as printed.

## Historical designs (2026-09-24)

## Current: V3 fitted shells — 2026-09-25

Builder cad/v3_fit.py; files stl/v3-fit and renders/v3-fit. Only two shells.
V2 buttons and J1 cap reused without change.697 required checks, inherited
J1 motion uncertainty retained. JOYSTICK-REVIEW.md is the single review
handoff. Dispatch recorded in prints/2026-09-25-v3-fit.md. Upright lid needs
operator slice review before start; no supports/raft authorized.

## Historical designs (2026-09-24, continued)

| Commit | Iteration / change | Print evidence |
|---|---|---|
| `30ecec9` | First original board proxies, snap case, caps and viewer | No recorded result |
| `9260716` | Correct USB orientation to joystick end | No recorded result |
| `f178c19` | Square flanged button caps and individual holes | No recorded result |
| `6469436` | Print-oriented exports | Test 1 source; request logged at `752fcb4` |
| `f3eb689` | Thicker tongue, Ø10.5 joystick opening | Intermediate lid revision; see historical REPORT.md |
| `29e74e1` | Working snap windows/wedges, corner and documentation audit | Intermediate corrected geometry |
| `4010773` | Test 2: Ø12 joystick opening, neck/disc cap, USB envelope/recess, two pads | Request logged at `28f6932`; fit result pending |
| `prototype-r4` tag | R4: mating gap/flexible bands, USB insertion channel/fin, sloped shelves, four pads, cap clearance fixes, 171 geometric checks | Test 3 submitted to HTTP inbox; IDs and pending result in its log |

Setup, measurement and report commits are also preserved in the full git
history. This register identifies meaningful design states; it does not imply
that every intermediate state was physically printed. Earlier unsaved edits
cannot be reconstructed as separate revisions.

## V1 feedback / R5 checkpoint

Austin identifies the photographed first-principles case as V1; its exact
print commit is not established. Three photos and five requested changes
are saved in `prints/2026-09-24-v1-feedback.md`.

Tag `r5-wip-joystick-pry`: captive ball joystick and two pry notches;
273 CAD checks pass. Not submitted; not ready to print. USB-C and
rectangular/taller buttons and bottom button access remain pending.
Earlier history is preserved.

## Artifact reproducibility

## V2 print candidate / completed R5

Tag `prototype-v2`: completes all five V1 requests. Adds scan-derived bottom
button hole, rectangular/taller buttons, higher/tighter USB-C; retains
checkpoint joystick and notches. Includes measurement script/overlay,
mesh degenerate-facet removal, geometry checks, STL/STEP, preview and hashes.
Print status and eventual results: `prints/2026-09-24-v2.md`. V2 is not a
physical-fit certification. Older WIP remains saved under its own tag.

## Hash records

## V3 browser review — 2026-09-25

Tag `v3-review-1`: original4010773 lower joystick interface, V2-sized ball
with printing flat, tapered inside lip, uniformly flat lid4 mm higher, longer
button stems, closed USB base port without fin. V2 USB alignment retained.
Browser viewer includes orbit, explode, part toggles and shell transparency.
See `reports/2026-09-25-v3-review.md`; requires Austin's approval before print.
No printer submission. Geometry/tag are a review checkpoint, not print success.

## Hash records (all revisions)

## V3 low-lid revisions

- `2587340`: D7 side-tab experiment. Screen recess1 mm;16 required
  ten-degree lid-motion cases failed. Saved explicitly as failed, not printed.
- `v3-review-2`: D8 rear retaining tab and internal rear-wall pocket. Keeps
  screen recess1 mm and earlier socket; lowers button retaining wings.
  Review viewer only: no replacement print files or printer request.
  See `reports/2026-09-25-low-lid-experiments.md` and `renders/v3-low/`.

The older tall `v3-review-1` and all failed versions remain in Git history.

2026-09-25 physical result: Austin reports V2 joystick socket failure and
support-related button-hole problems. Pry access, bottom access alignment
and rectangular cap shape worked. `reports/2026-09-25-v2-review.md` records
the results and flat-lid, support-free correction goals. V2 tag unchanged;
this is a documentation-only review, not a new printable revision.

- Source and output SHA-256 hashes: `stl/manifest.json`.
- Geometric checks and source hashes: `renders/validation.json`.
- Reasoning and limitations: `DESIGN.md`, `REPORT.md`, `MEASUREMENTS.md`.
- Clean-room input record: append-only `PROVENANCE.md`.
- Physical trial: `prints/2026-09-24-test3-r4.md`.

The generated manifest's `git` field identifies the pre-commit parent with
`-modified`, because artifacts were built before committing. Its source
hashes identify the exact CAD in the R4 tag; do not rebuild merely to change
that label. Future geometry changes get a new commit and a new iteration tag.
Printer-profile or status changes get separate commits so the geometry tag
stays fixed. Keep printer credentials and machine-local configuration out of
this public repository.
# J1 isolated round-lip review — 2026-09-25

Source cad/joystick_test.py; outputs stl/joystick-j1 and renders/joystick-j1.
Complete handoff: JOYSTICK-REVIEW.md. Two test parts, known motion failures,
review before printing. Historical whole-case files remain unchanged.
## J3 / L1 — 2026-09-25

J2 round hole too tight per Austin. J3: round 3.50 × 1.10 mm, deeper square
unchanged. L1: flat lid face 0.90 mm lower, existing base/buttons retained.
Original source cad/j3_low_lid.py; isolated artifacts stl/j3-low-lid and
renders/j3-low-lid. 18 checks pass. Physical travel and fit pending.
Only lid and joystick authorized; supports/raft off. See JOYSTICK-REVIEW.md
and prints/2026-09-25-j3-low-lid.md for full handoff and dispatch.
### J3 / L1 pre-dispatch correction

Review caught the initial top-trimming box also truncating the skirt.
Corrected its lower bound to preserve the full skirt; strengthened validation
to compare both material differences and minimum Z. Initial 8b0fc03 artifacts
were never dispatched. Only the corrected full-skirt revision is printable.
## J2 restore / lower another 1.50 mm — preflight only

User rejects J3 socket, selects J2 unchanged. Requested face z2.70 conflicts
with existing button pocket roof z3.56. No geometry or print produced; details
and required scope decision recorded in JOYSTICK-REVIEW.md. Prior print files
unchanged. Await choice on retention redesign versus height target.
## L2 / exact J2 — one-millimeter physical trial

Austin supersedes 1.50 mm with 1.00 mm and explicitly authorizes printing
despite fit uncertainty. Roof translated, not shaved. J2 byte-identical.
Seven structural checks pass; hat/button overlaps remain diagnostic warnings.
Files: cad/l2_j2_trial.py, stl/l2-j2/, renders/l2-j2/. Full handoff in
JOYSTICK-REVIEW.md; dispatch in prints/2026-09-25-l2-j2.md.
## L3 — restore L1 height and shift round hole toward LCD

Austin confirms L2 cannot close with caps installed. Revert height to L1 and
move 8 mm opening 1.00 mm toward LCD using his new photos/direction. Pocket
and all other L1 geometry unchanged. Lid only print. Isolated original source
cad/l3_shifted_hole.py and stl/renders/l3-shifted-hole artifacts.
## L4 — halfway back plus photo-up, not yet printed

L3 feedback/photos show overshoot. Aperture moves +0.50 Y and +0.30 X from
L3, leaving centre (13.4671,45.6292). Isolated source cad/l4_alignment.py,
STL and viewer under l4-alignment. All prior versions preserved. No dispatch.
## S1 — stronger matching shells with 2:1 visible height split

User requests seam lower, smooth stronger sides, one pry notch, L4 alignment,
and interactive rendering before print. Original cad/s1_strong_shell.py.
Artifacts stl/s1-strong-shell and renders/s1-strong-shell. 21 geometry checks
and browser smoke test pass. Joint force/strength/physical assembly untested.
New pair required; reuse J2/buttons. No printing until review. Full handoff in
JOYSTICK-REVIEW.md, including internal rails and exact wall/joint dimensions.
## S1 full-case print approval / packaging

Austin approves reviewed S1 and requests joystick plus buttons too. No shell
geometry change. Package seven pieces with lid face down, base floor down,
J2 and V2 buttons flange down. cad/s1_full_plate.py exports individual parts
and one plate; byte-check shells/J2 against original reviewed exports.
Print log prints/2026-09-25-s1-full-case.md. Preserve original review artifacts.
## S2 — base-only closure fix and rounded buttons

Physical S1 nearly works but drops roughly0.25mm and opens too easily. New
base catch shape targets minimal axial play using existing S1 lid pockets.
Four button caps have tops0.50mm taller, rounded radius1.20, same interfaces.
Original isolated cad/s2_tight_base.py, stl/renders/s2-tight-base. 36 checks
pass. Reuse S1 lid and J2; physical force and tactile test pending. IMG_0840
archives assembled S1 baseline, duplicate uploads stored once with hashes.
## V1.0 — first production release

The earlier V1/V2/V3, R, J, L and S rounds were development prototypes (0.x).
S2 passed Austin's test. V1.0 = S1 lid + S2 base + S2 buttons + J2, plus three
0.25 mm nudges: the joystick hole moves toward USB-C, the USB-C opening moves
up, and the reset hole moves toward the centre. Source: cad/v1_production.py.
Outputs: stl/v1.0 and renders/v1.0, with 35 checks passing and the browser
viewer tested. Not printed in PLA, at Austin's request; the next prints are in
PETG. Photos: prints/v1.0-photos. Tag: v1.0.
## V1.1 — USB-end spacer

PETG v1.0 works well, but the board slides about 1.2 mm along the case.
V1.1 = v1.0 plus a 1.0 mm stop at the USB end: a lid lip between the rails
and base stops on the rails. The openings are unchanged. Source:
cad/v1_1_spacer.py. Outputs: stl/v1.1 and renders/v1.1, with 16 checks
passing and the viewer tested. The caps are unchanged; reuse the v1.0 caps.
## V1.2 — half spacer

The v1.1 1.0 mm spacer was too big (the board would not sit flush). V1.2 is
the same design with 0.5 mm. Source: cad/v1_2_half_spacer.py. Outputs:
stl/v1.2 and renders/v1.2. All checks pass.
## V1.3 — USB end wall 0.5 mm in, no spacer

This replaces the V1.1/V1.2 spacer trials. It is v1.0 with the USB-C end wall
0.5 mm inward on the lid and base; the case is 58.60 mm long. Source:
cad/v1_3_short_end.py. Outputs: stl/v1.3 and renders/v1.3, with 19 checks
passing. The caps are unchanged.
## Current best: v1.3 (2026-09-26)

v1.3 passed Austin's test: nothing rattles, and everything clicks.
`cad/current.py` copies it to `stl/current/` (lid, base, joystick, button,
full-set plate) at stable paths, and it is tagged v1.3. For future winners,
update CURRENT/PARTS and rerun.
## V1.4 — rounded top and LCD window edges (review only)

v1.3 with a 1.5 mm top-perimeter fillet and a 0.7 mm LCD-window fillet on the
lid. The fit is unchanged, and the base and caps are the same as v1.3.
Source: cad/v1_4_rounded.py. Outputs: stl/v1.4 and renders/v1.4, with 8
checks passing and the viewer tested. Not printed. Face-down printing puts
both roundings at the bed, so a slice check is needed.
V1.4 review 3: the top edge is rounded 3.0 mm and the window 1.2 mm (review 1:
1.5 and 0.7). Base check: byte-identical to the v1.3 base.
V1.4 review 4: the window is 1.0 mm smaller on each side (covering 0.6 mm of
the glass border) with a rounded bezel 0.3 mm above the glass. Base unchanged.
J4 joystick (v1.4): J2 with a 5 mm flat top, so pressing in is easier. It is
1.05 mm shorter, and the socket and tilt are unchanged. File:
stl/v1.4/joystick.stl. Not printed.
J4 review 2: the flat top becomes a hat (5.5 mm waist, 45° flare, 7 mm disc,
about 6 mm flat), at the same height as J2. Not printed.
J4 review 3: a 7.4 mm half ball with a flat top all the way across (the hat
version was dropped). It passes the 8 mm hole with 0.3 mm each side, and no
new tilt contact versus J2. Not printed.
