# V3 shell and joystick review

## CURRENT: V3-FLAT — face-down correction, 2026-09-25

Sent source145e386 as `20260925-111549-v3-flat-lid-face-down`, lid only,
31.44 ×57.50 ×8.10 mm. Server hash verified; GO request accepted, initial
status `new`. Printing not yet confirmed. Face-down contact934.22 square mm.

Austin explicitly authorizes raising the WHOLE lid face for this trial.
All outer face material is now atz5.1; print FACE DOWN with supports/raft OFF.
No local raised boss. Joystick holeØ8 and under-roofz4.4 remain unchanged.
Screen depth3.05 mm is knowingly accepted for this iteration; reduce later
after the rigid fit test. Existing V2 buttons protrude1.3 mm, .92 at full
press. Buttons, J1 joystick and base geometry are unchanged; send LID ONLY.

699 required CAD checks pass, including coplanar outer faces and broad
face-down bed contact. Known J1 ten-degree motion hypotheses remain16
contacts, not falsely claimed resolved. Printed fit and slicing still need
verification. Preserve export orientation; do not auto-orient or add supports.

Files: `cad/v3_flat.py`, `stl/v3-flat/v3-flat-lid-face-down.stl`,
`renders/v3-flat/viewer.html`, `renders/v3-flat/validation.json`,
`renders/v3-flat/manifest.json`. Main viewer updated as well. Build with
`.venv/bin/python cad/v3_flat.py`. Prior upright files remain historical.

Print server reports the previous job printed LID ONLY, not the base, and
was stopped by Austin at layer34/50. It is on hold. A message explicitly
supersedes that old lid; no restart/reprint requested. The unchanged V3 base
is not assumed physically printed. Current dispatch log:
`prints/2026-09-25-v3-flat.md`.

## Current revision — V3 fitted shells, 2026-09-25

Submitted sourceb4548b3 through HTTP inbox as
`20260925-103637-v3-shells-only`. Exactly two shell parts,67.88 ×57.50 ×20.64 mm
combined plate bounds. Hash verified. GO request accepted subject to slice
checks below; initial status `new`, NOT confirmed printing. Dispatch log:
`prints/2026-09-25-v3-fit.md`.

Austin authorized a NEW base and complete lid, reusing the existing V2
rectangular buttons and J1 joystick. Print exactly two shell parts, not caps.
This resolves the old-base ambiguity below. Historical J1 review is preserved.

### What changed

- Base: closed V1-style USB port at V2's exact working bounds. No lid fin,
  no rim-open USB channel. Existing reset hole, pry notches and snaps retained.
- Lid: actual complete snapping shell. RoundØ8 joystick hole, under-roofz4.4,
  topz5.1, reproducing J1's nominal retaining height around the unchanged cap.
- Screen side rails atz3.05,1 mm above glass. Only joystick and button regions
  are higher. Joystick front wall meets a short central segment of the upper
  screen edge; that segment is3.05 mm above glass, NOT1 mm. No uniform raise.
- Button region remains at V2'sz4.6, with flange pocket ceiling3.56, so the
  existing printed caps retain their original1.8 mm protrusion and travel.
- Both shells print upright, base floor and lid skirt on bed. The lid is NOT
  face-down on its raised boss. No supports/raft are authorized.

### Verification and remaining risks

697 required checks pass. These include static assembly, each button's
retention and measured travel, lid installation, snaps catching on lift,
pry/reset access, closed USB channel and sampled USB-first Pico assembly.
Comparison with our own prototype-v2 source proves identical button geometry
(zero added/removed volume), identical USB aperture bounds, and base changes
only adding265.31868 cubic mm to close the former USB channel. J1 cap re-export
is byte-for-byte identical to the printed file. No joystick/button reprints.

The inherited16 ten-degree cap/lid contacts remain, out of192 poses including
two seating assumptions. There are no new lid contacts beyond the J1 gauge
in these scenarios. Austin reports free hand-held movement, but the rigid lid
still needs a physical test. Guessed-body contacts and a5.28 cubic mm blue
tape proxy conflict remain disclosed; tape identity is not established.

Each shell is a single valid solid with closed-edge STL. Base bed contact
1787.51 square mm; upright lid skirt contact126.57 square mm. Browser render,
orbit, views, exploded view, transparency and part visibility pass.

**Slicing is not verified locally.** Operator must inspect upright lid
button/joystick ceilings, .4 mm front wall, corner pad overhangs,14 mm snap
slot bridges, skirt adhesion and USB bridge. Hold if these need supports or
a raft; do not add them or silently flip the lid. Actual settings/finish/fit
are pending. A geometrically valid STL does not establish printability.

During this build, visual review caught an open slot at the boss front; a
subsequent export caught a zero-thickness edge. The final boss has a continuous
front wall and passes mesh checks. Earlier intermediate files were not sent.

### Current files and reproduction

- Source: `cad/v3_fit.py`; shared helper `cad/model.py` adds an optional switch
  to omit the rejected D8 rear-arm pocket. Historical default is unchanged.
- Send only `stl/v3-fit/v3-shells-only.stl` (base + lid, spaced5 mm, at bedz0).
- Separate shell files: `stl/v3-fit/base.stl`, `stl/v3-fit/lid.stl`.
- Viewer: `renders/v3-fit/viewer.html`, also updated `renders/viewer.html`.
  Existing LAN server port8793, path `/v3-fit/viewer.html`.
- Screenshot and STEP: `renders/v3-fit/preview.png`, `renders/v3-fit/assembly.step`.
- Evidence: `renders/v3-fit/validation.json`, `history-check.json`, `manifest.json`.
- Print dispatch/current status: `prints/2026-09-25-v3-fit.md`.

```sh
.venv/bin/python cad/v3_fit.py
.venv/bin/python tools/check_v3_history.py
```

Do not send old `stl/print/`, J1 gauge, buttons or joystick. Seat the Pico USB
through the closed port first, then connect the LCD board; do not force the
connected stack vertically through the closed opening. Install existing
buttons and J1 cap, lower lid over ball, latch gently, test every direction
and click. Stop if parts bind, press the glass, or load the connector.

## Historical J1 test review

## Physical feedback — 2026-09-25, after printing

Austin reports full joystick movement while holding the gauge on the board.
The gauge is too flimsy to establish fit confidently. IMG_0814 shows the
printed ball cap and gauge on his actual board stack. This is encouraging
physical evidence, not proof of constrained movement under a latched lid;
keep the earlier CAD scenario failures as historical diagnostics.

Next request: a real complete lid fitting his already printed base. Reuse
the unchanged J1 joystick; do not print another joystick unnecessarily.
Base revision must be identified before committing the mating/USB geometry:
V2 has a USB channel open to the rim, unlike the intended closed-port base.
No replacement lid generated or submitted at this feedback checkpoint.

## Dispatch update — 2026-09-25

Austin authorized the small experiment after being told of the10-degree
collision. Submitted unchanged source6bec71a, combined two-part STL, to the
HTTP print inbox. Drop `20260925-100248-two-part-test`; server reports35.4 ×
19.99 ×8.6 mm, fits bed, SHA-256 matches the build manifest. Print request
sent explicitly; initial status `new`, NOT confirmed printing.

Requested PLA, loaded colour acceptable,0.16 mm layers,3 walls, supports OFF,
raft OFF, original orientations. Operator must inspect sliced thin lip,
socket bridge, ball and feet before starting; HOLD if supports/raft would be
needed. Camera-confirmed clear bed required; no interruption of another job.
Actual slice settings, preview, start/completion and physical fit are pending.
The manifest's `submitted:false` and viewer notices reflect build time;
this dated dispatch update is the current status. Detailed log is in
`prints/2026-09-25-joystick-j1.md`. Earlier review below is preserved.

## Conclusion and confidence

The simple round-hole mechanism is worth testing. This draft is **not yet
validated for full movement or ready for production**. Nothing was sent to
the printer. Only two small test parts were exported; no full case changed.

Confidence is moderate in the selected old socket dimensions, low in the new
lip clearance and printed fit. Austin reports V1 worked, but the exact printed
V1 commit is not confirmed. Do not mistake a CAD match for a successful fit.

The current test clears at rest and in all sampled 5-degree poses. It hits
the lid gauge in 16 of 96 motion scenarios: every unpressed 10-degree direction
at both assumed pivots. Maximum intersection is 0.966939 cubic millimetres.
Actual required angle is unknown. Claude Code should review this before slicing.

## What Austin wants

- Keep V1's working stem socket and movement.
- Ball through a round lid hole; wider circular lip retained underneath.
- Install the cap on the PCB first, then lower the lid over it.
- No rear arm, rectangular opening, removable support layer or full-case raise.
- Keep the screen surround about 1 mm above the glass; a local height increase
  near the joystick is acceptable if necessary, subject to review.
- Test only the cap and a small lid section before another full case.

Keep the previously successful pry notches, bottom button access, rectangular
buttons and USB alignment. Restore a closed V1-style USB opening without V2's
lid tab. Those whole-case changes are outside this isolated test.

## Evidence and limits

Original hardware dimensions are in MEASUREMENTS.md. This is independent MIT
geometry; no third-party case was consulted. Source inputs are in PROVENANCE.md.

Austin's side photos IMG_0810, IMG_0811 and IMG_0812 show the bare joystick and
screen. Their tops look roughly level. Perspective and lack of a scale prevent
reliable height measurements; no dimensions were extracted from these photos.
Original uploads have suffixes paste-0d95cf02-IMG_0810.jpg,
paste-962bb905-IMG_0811.jpg and paste-141c541d-IMG_0812.jpg.

Known glass top: z2.05 mm above LCD PCB front. Recorded stem tip: z5.00.
Joystick metal body height3.0, pivot location, click travel and tilt are guesses.
Do not adjust the proven-old interface simply to satisfy that guessed body.

V1 reference selected: original repository commit4010773. It used a2.01 mm
square socket, roofz5.30, lower edgez3.40 and neckØ5. Earlier lid-only commit6469436
had the same socket width/roof but different neck/bottom. V2 narrowed the socket
to1.91; Austin reported failure. The identification uncertainty matters.

## Exactly what J1 contains

All heights below are from the LCD PCB front, not the print bed.

| Feature | Trial dimension |
|---|---|
| Square socket | 2.01 mm, open below; roofz5.30 |
| Neck | Ø5 mm; bottomz3.40 |
| Circular retaining lip | Ø10.4 mm; z3.40–3.80; thickness0.40 |
| Ball | Ø7 mm; centrez8.50; topz12.00 |
| Round lid hole | Ø8 mm |
| Lid test disk | Ø20 mm; undersidez4.40; topz5.10 |
| Two test feet | centresx±9 mm; 2×6 mm; contact PCB atz0 |

The gauge is a hand-held height reference, NOT a new case attachment mechanism.
Its feet are test fixtures, not proposed production supports. Hold it down on
clear PCB areas while moving the joystick. The hardware shown in the viewer
is an illustrative cropped proxy and is not included in the print files.

Ball/hole clearance is0.5 mm per side. Lip overlap is1.2 mm per side when
centred. Vertical lip clearance is0.6 mm. The intended seated position itself
is uncertain: the old socket roof is0.3 mm above the nominal stem tip.
Pressing it fully onto the stem may lower the whole cap; model checks should
consider that and insertion force, not just the displayed nominal position.

**Height tradeoff not resolved:** gauge top is3.05 mm above glass, locally.
That is2.05 mm higher than the desired surrounding screen rim. This test does
NOT meet a universal1 mm lid-height requirement. Keeping an old cap bottom
atz3.40 puts its lip above a z3.05 lid before any movement clearance is added.
The test isolates that conflict; it does not prove this local height necessary
or optimal. The local feature's final shape and connection to the lid are not
designed here. The earlier oversized D8 rear-arm design remains rejected.

The ball is shorter than V2's centrez11.4, but retains itsØ7 round shape.
This is an explicit trial change, not an exact copy of V2's upper geometry.

## Files and preview

Paths here are relative to this document's repository directory.

- Parametric build: `cad/joystick_test.py`
- One plate containing only both test parts: `stl/joystick-j1/two-part-test.stl`
- Separate files: `stl/joystick-j1/joystick-cap.stl`, `stl/joystick-j1/lid-gauge.stl`
- Rotatable browser preview: `renders/joystick-j1/viewer.html`
- Screenshot: `renders/joystick-j1/preview.png`
- Full numerical checks: `renders/joystick-j1/validation.json`
- Source/artifact hashes: `renders/joystick-j1/manifest.json`

The existing LAN preview server serves this viewer on port8793 at
`/joystick-j1/viewer.html`. Use the same host as the previous working preview.
The viewer needs its existing Three.js CDN connection. Browser checks passed:
three parts rendered, no JavaScript errors, orbit, views, transparency,
exploded view and hiding parts. Whole-case preview URLs still show old work.

Rebuild from the repository root:

```sh
.venv/bin/python cad/joystick_test.py
```

Do not use `cad/build.py` or old `stl/print/` files for this test. They refer to
whole-case iterations. This isolated builder does not replace those artifacts.

## Checks performed

- Each test part is one valid CAD solid; exported STL edges are closed.
- Export welds seam noise at0.00001 mm, much smaller than0.02 mm mesh tolerance.
- No static cap/gauge, cap/hardware-proxy or gauge/hardware-proxy overlap.
- Old lower socket cross-section volume agrees with the reconstructed baseline.
  This is not yet an independent BRep difference against the historical commit.
- Ball smaller than hole; flange larger than hole; upward pull meets gauge.
- 96 cap/gauge poses:0/5/10 degrees,8 directions, pivotsz0/3, press0/.3.
  16 failures retained in JSON, not hidden. A pressed pose clearing does not
  establish that the unpressed joystick can safely move through that pose.

Not checked: measured full travel, full swept motion, tilted hardware contact,
printed shrinkage, actual socket seating, lip strength, pull-out under tilt,
slicer layer preview, or integration into the final lid. The 0.4 mm lip may
be fragile. The foot contact locations require actual PCB inspection.

## Claude Code review request

Read CLAUDE.md first and respect the clean-room exclusions. Review our own
measurements/history only; do not search existing Pico cases.

1. Independently compare socket geometry to4010773 and distinguish6469436.
2. Check actual seated height, lip contact and full movement. Determine whether
   the10-degree failures matter before recommending a print.
3. Decide whether lower local height is feasible without changing the working
   socket or adding arms. Do not raise the whole screen rim.
4. Check lip strength, circular retention when tilted, ball assembly clearance,
   the gauge feet, and hardware contact through motion.
5. Verify STL dimensions/orientation and slice preview. Never solve this by
   silently enabling supports, a raft or an extra peel-off layer.
6. State the smallest next change or measurement needed. Keep this a two-part
   experiment; preserve previous iterations and commit any revision separately.

## Proposed printing and bench test — not executed

Cap prints upright, flat flange down, socket opening against bed. Gauge prints
inverted on its flat top with the feet upward. Combined STL already positions
both onz0 with5 mm between bounding boxes. Do not auto-orient.

Intent: no supports, no raft. The2.01 mm socket roof needs a short bridge;
ball overhang and thin lip need slicer review. No material/process chosen or
slicing performed in this turn. Do not call this support-free verified.

After review: fit the cap gently; never force the switch. Check all directions
and click without the gauge, then lower the gauge over the ball, rest its feet
on clear PCB and hold it down. Check movement/click again and gentle retention.
Stop if it binds. Record cap seating, rubbing direction, lip damage and photos.
If height remains uncertain, measure PCB-to-metal-body top and installed-lip
top before redesigning the whole lid. Submit through the established HTTP print
server only after review; no SSH and no printer action has occurred here.
