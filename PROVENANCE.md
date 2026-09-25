# Provenance log

Append-only. Newest at the bottom. Every design input, every session that
touched geometry, and what that session had seen.

## 2026-09-19. Phase 0. Repo created.

- By: Claude (Fable 5.1), session started in `~/picowallet`, on Austin's
  instruction, after he asked how to make a sellable case.
- Contamination statement: this session had, earlier the same day, read the
  picowallet `case/` notes and memory referring to the Zez0000 and Plass
  designs and their derivatives, and had opened the MakerWorld listing page
  for model 3230142 to read its license. It did not open the STLs in this
  session but has their derived measurements in its notes.
- What it wrote: `README.md`, `LICENSE`, `CLAUDE.md`, `PROCESS.md`,
  `SOURCES.md`, `MEASUREMENTS.md`, this file. No `scad/`. No `stl/`.
- Dimensions written: only the Raspberry Pi Pico 2 W rows P1 to P10 in
  `MEASUREMENTS.md`, all from the public Pico datasheet mechanical drawing,
  all marked "confirm cal". No LCD board, screen, button, joystick, stack or
  case dimensions were written.
- Decision: all geometry will be produced by fresh sessions started in this
  directory that have not loaded `~/picowallet` or its memory.
- Austin has handled and seen the earlier printed cases. That is the normal
  position of anyone designing a product in a category that already has
  products. The rule for him is the same as for the agents: measure the
  hardware, do not open the other files, write choices down.

## 2026-09-20. Method research.

- By: the same Claude session as Phase 0 (still contaminated, still no geometry).
- Read: Raspberry Pi Pico series documentation page and the Pico 2 STEP link;
  the Waveshare Pico-LCD-1.3 wiki Resources list and schematic PDF (links and
  part labels only, no case content); general 3D scanner and flatbed
  reverse-engineering articles. Did not open any case design.
- Wrote: `research/scanning.md`. Switched the plan from OpenSCAD to build123d
  so the official Pico 2 STEP can be imported. Added the STEP and the
  schematic to allowed sources. Nothing measured, nothing drawn.

## 2026-09-24. Phase 1 measuring and first geometry.

- By: Claude (Opus 5.5), one session started in this directory. It did not
  load `~/picowallet` or its memory, did not open any forbidden path in
  `CLAUDE.md`, and made no web search or web fetch (checked against the
  session transcript on 2026-09-24). Its only contact with `~/picowallet`
  was one `ls -d` checking that the directory exists.
- Inputs used, all logged in `MEASUREMENTS.md` with row IDs:
  - Flatbed scan 01 of Austin's boards, 600 dpi, scale from a steel rule in
    the same scan (`measurements/2026-09-24-scan-01-*`). Our own image.
  - Caliper readings taken by Austin on the bench, read aloud, one iPad
    camera frame saved per reading (`measurements/2026-09-24-cal-*.jpg`).
  - Austin's statements: USB-C at the joystick end (A3); PINK board only;
    snap fit; square caps with a web and a lip.
  - Datasheet: header row spacing 17.78 = 7 x 2.54 (P10), the standard Pico
    pinout, used only to place the sockets and the Pico in the render.
- No third-party geometry. Tools only: build123d (Apache-2.0) generates the
  shapes; three.js (MIT) is loaded from cdnjs by the viewer and not copied in.
- Wrote: `cad/params.py`, `cad/model.py`, `cad/build.py`, `stl/`,
  `renders/viewer.html`, `REPORT.md`, first test print drops.

## 2026-09-24. Independent revision R4, Codex.

- Session started in this repository at Austin's request to critically review
  all measurements and correct or redesign the case. Read this repository's
  documents, code, scan analysis, overlay and caliper photographs. No other
  case listings, geometry, picowallet files or memory were opened. No imported
  third-party geometry. Existing MIT license retained.
- Inputs: the recorded caliper values and scan01 already listed above.
  Photo review identifies evidence limitations; it does not silently replace
  Austin's readings with uncertain image readings. New derived coordinate
  rows and explicit design/verification assumptions are in MEASUREMENTS.md.
- Original engineering changes: clearance between halves, slotted lid snap
  arms, sloped shelf undersides, USB insertion channel with lid closure,
  four PCB hold-down pads, narrower button flanges, and joystick fit samples.
  Choices and remaining physical tests are documented in DESIGN.md/REPORT.md.

## 2026-09-24. R5 captive joystick, Codex.

- Input: Austin's direct feedback from the first physical print. The joystick
  cap must attach to the board before the lid; a lower lip retains it inside
  the case, with a shaft and ball outside. R4's post-lid cap is rejected.
- No external case geometry, photographs, or measurements consulted. Existing
  hardware rows retained; new flange/ball/collar dimensions are original design
  choices D5-JOY. Joystick motion is still an assumed verification envelope.
- Sent a hold request for R4 via the already authorized print inbox workflow.
  Preserve R4 tag/history. R5 changes joystick cap and lid only, with assembly,
  retention and motion checks, matching documentation and rebuilt outputs.
- Additional direct feedback: the first printed case is difficult to open;
  Austin requests a tool notch. Add two original shallow seam notches
  (D5-PRY), preserving the flexible latch bands and underlying wall.

## 2026-09-24. V1 physical feedback and photos, Codex.

- Austin explicitly identifies the photographed case as V1, made from first
  principles without another licensed case. Input is his own printed case,
  not an external enclosure reference. Repo MIT license is unchanged.
- Viewed his uploads paste-f2819d95-IMG_0801.jpg (joystick),
  paste-f925a63a-IMG_0800.jpg (buttons), paste-42cd1b6f-IMG_0799.jpg (USB).
  Saved unchanged in prints/v1-feedback/. No dimensions inferred from the
  perspective photos; no other case sources consulted.
- Additional requested changes: taller/wider rectangular buttons with
  smaller top/bottom lips; smaller USB opening shifted toward lid; bottom
  tool-access hole over pink board button. Button identity, coordinates and
  pad size are not established. These three changes remain pending.
- Saved feedback separately from the R5 joystick/pry CAD checkpoint.
  Physical V1's exact source commit is not established. Preserve all earlier
  commits and tags; do not label the partial draft as ready to print.

## 2026-09-24. V2 candidate from existing scan, Codex.

- Austin explicitly authorizes making a good estimate from the existing pink
  board scan, iterating, completing the next version and sending to printer.
- Revisited scan01 and its original measurement script. Detected the pale
  board button at crop-local (294.0667,409.7847), centre-relative u=13.4370,
  v=-3.2868 mm. Opposite-facing component side requires lateral reflection
  into the LCD-front coordinate frame. Recorded PINK-BTN-SCAN and D5-ACCESS.
- V1 USB photo supports the higher existing A1 placement rather than P15's
  lower placement; selected A1 for shell/aperture but kept conservative
  floor depth. Recorded original button/access/USB trial choices before CAD.
- No third-party case geometry viewed or imported. V2 is the next physical
  print candidate; internal CAD revision remains R5 after its saved checkpoint.

## 2026-09-25. V2 physical review, Codex.

- Input: Austin's direct physical feedback. Pry feature, bottom board-button
  hole alignment and rectangular cap shape worked. V2 joystick does not fit
  PCB stick; raised collar and support layer caused problems at button holes.
  Earlier joystick fit and movement were good.
- Requested correction goals: preserve successful features and earlier
  joystick interface/movement; add internal lip and ball passing through
  opening; restore flat lid, no raised case or problematic supports.
- Austin requested documentation first. Added review/handoff and status
  notices only. No geometry changes, external case references, new hardware
  dimensions or printer actions. Specific socket failure cause and actual
  slicer support construction remain unverified.

## 2026-09-25. V3 browser-review design, Codex.

- Austin reports V2 USB opening aligns but rejects the lid fin/tab and its
  gaps. Restore closed base port style with V2 alignment. Keep working pry
  notches, bottom access and rectangular caps.
- Requests earlier joystick bottom/interface and V2 ball, captured inside a
  flat lid; permits uniform extra lid height and correspondingly taller caps.
  No support layer or raised local collar. Requests interactive browser
  rendering and approval before printing; no printer action authorized now.
- Inspected only this repository's original commits6469436 and4010773.
  Both sockets2.01 and roof5.30 versus V2 socket1.91 and roof5.00. Select
  full-case4010773 lower geometry as explicit provisional V1 baseline;
  exact physical cap source not independently confirmed. No external models.
- Original tapered flange and small ball-top print flat added for support-
  avoiding inverted cap printing; choices logged D6, not hardware readings.

- Final V3 review: flat top4.0 mm higher, original full-case lower shape
  matched by CAD difference checks. Smaller pocket and screen-side web keep
  the joystick relief from opening into the display well. Closed-port
  USB-first assembly checked at19 separate-Pico poses; physical test pending.
- Required geometry checks206 passed;48 intersections with guessed joystick
  body retained as unresolved sensitivity diagnostics rather than changing
  the reported-working earlier neck to satisfy an unmeasured proxy.
- Browser controls tested in local Chromium. Served only renders/ on LAN
  port8765 for user review. No printer interaction. V3 approval remains pending.

## 2026-09-25. Low-lid V3 revision in progress, Codex.

- Austin rejects deep screen recess and requires top at most1 mm above glass.
  Explicitly asks to proceed now. No additional outside geometry consulted.
- D7 tests original side-arm retention around joystick body, retaining earlier
  socket. Button underside relief allows retaining wings below plunger top.
  Measurements unchanged; these are trial constructions requiring checks.
- Five-degree motion is a chosen trial, not established hardware travel;
  retain larger-angle failures explicitly. No print authorized or requested.

- D7 side tabs failed16 ten-degree lid-motion cases; saved as failed
  checkpoint. D8 tests one rear tab beyond PCB edge, using that available
  space rather than adding lid height. Original profile/pocket recorded
  before modelling. No new hardware measurements or outside designs.

- D8 refinement shifts/reprofiles the rear heel and pocket, preserving the
  original lower socket. A small PCB interference in one10-degree pressed
  pose prompted extra relief at the heel's lower edge; full original
  10-degree lid scenarios remain required, not weakened to get a pass.
- Added cap/base, cap/PCB and new rear-arm/fixed-hardware motion checks.
  Button wings are lowered beside switch bodies to retain the1 mm screen
  recess; plunger contact height and outside rectangular shape retained.
- Dedicated review builder updates browser files only; old print artifacts
  are untouched and explicitly labelled obsolete for this geometry.

- Final D8 review:495 required checks pass, including the full10-degree
  lid/base/PCB scenarios and new-arm versus fixed hardware. Inherited48
  guessed-body/neck intersections remain unresolved. Browser render and
  interactions tested; source and listed output hashes verified. No print
  artifacts generated, no printer action. Slicing, thin-junction strength
  and actual hardware movement still need verification after review.

## 2026-09-25. J1 isolated round-lip fit test, Codex.

- Austin supplied IMG_0810, IMG_0811 and IMG_0812 as side photos of his
  hardware in this ongoing fit discussion. Used qualitatively only: body
  and screen tops look similar; perspective photos are not caliper readings.
- Austin rejected D8 rear arm and rectangular opening. Requests ball through
  round hole, wider circular lip underneath, original socket, small test only.
- Latest instruction: prepare CAD viewer, STL and review note for Claude Code.
  No printing in this turn. No outside geometry used; original MIT design.
- J1 dimensions below are explicit design trials, not new measurements.

## 2026-09-25. J1 physical feedback, Codex.

- Austin supplies IMG_0814 showing his printed J1 cap/gauge on his board.
  Reports full motion when hand-held, but gauge too flimsy for confidence.
  No numerical measurement inferred from photo. Original user fit evidence.
- Requests actual lid for existing printed base, retaining unchanged J1 cap.
  Base revision unresolved; no outside designs consulted or geometry changed.

## 2026-09-25. V3 fitted shell, Codex.

- Austin resolves scope: new base with closed V1-style USB aperture at V2's
  working USB position/size, no USB lid fin; new complete lid using existing
  V2 buttons and unchanged physically tested J1 joystick. Explicitly asks
  to send only these two shell parts. Retain pry and bottom access features.
- Inputs: own prototype-v2 source and parameters, current own base/snap
  geometry, J1 cap/gauge, and Austin's reported free hand-held movement.
  No third-party geometry, no new measured dimensions. Original MIT work.
- Lid screen rim remains z3.05; local joystick roof copies J1 z4.4..5.1,
  button region copies V2 z4.6. Upright lid printing proposed to avoid the
  previous raised-top/support-layer failure; operator must review bridges
  and overhangs, and hold rather than add supports or a raft.

## 2026-09-25. V3 flat-face correction, Codex.

- Austin explicitly rejects upright lid printing. Authorizes raising the
  entire face to the joystick's required height for this fit trial, face-down
  with NO supports. Requests immediate print after confirming instructions.
- Keep underside retention at J1 z4.4; entire outer face z5.1. Reuse existing
  base, buttons and joystick. No new hardware measurements or outside inputs.
- This explicitly supersedes the prior1 mm screen-depth constraint for this
  iteration. Button protrusion reduces .5 mm to1.3 mm with unchanged caps.

## 2026-09-25. Matching V3 base print request, Codex.

- Austin reports flat lid looks great and requests matching V3 base.
  Reused unchanged existing base mesh; no new measurements or geometry.
  User report confirms lid print, not yet assembled snap/joystick fit.

## 2026-09-25. J2 stepped socket, Codex.

- Austin supplies his hardware photos IMG_0822..IMG_0827, requesting lower
  cap seating, eventually lower flat lid and a small hole-centre correction.
  Photos show round stem collar below square shaft. Caliper display3.32 mm
  is visible but feature identification remains unconfirmed, not substituted
  for the explicitly requested trial diameter.
- Austin reports collar height less than1 mm, explicitly specifies socket:
  circleØ3 mm for first1 mm, existing square for next2 mm. Existing square
  is2.01 mm across flats. No added diameter allowance silently applied.
- Austin offers printing just the joystick first. Selected this scoped fit
  trial: unchanged outer J1 cap, deeper stepped cavity, no lid/base edits.
  All geometry original from this repository; no external cases consulted.

## 2026-09-25. V3 record photos, Claude (Opus 5.5).

- Austin supplies IMG_0814, IMG_0817, IMG_0822, IMG_0827 "for the record
  books" while working on V3, and asks that the whole process be documented
  from first principles so the design ships MIT with no non-commercial
  licence entanglement.
- Saved byte-identical to `prints/v3-photos/` with hashes and a per-photo
  description. Austin's own photos of this repo's own prints and his own
  boards; MIT with the repo. No third-party design in any frame.
- Record only: no dimension taken from these photos; nothing in `cad/`
  changed. This session opened no forbidden source and no picowallet file.
### 2026-09-25 — J3 / lowered flat lid trial

Austin's own J2 print feedback and two IMG_0828 photos (upload prefixes
961919fc and 583f9050): round socket too tight; request diameter 3.5 mm,
depth 1.1 mm, retain deeper square. Lip estimated 0.4 mm above glass.
Authorized printing a new lid and joystick together and progressively lowering
the lid until motion restricts, then backing off. Photos inspected directly;
not calibrated measurements. Codex input; user-owned hardware/photos, no
third-party case geometry. Original design choices below are trial values.
## 2026-09-25 — J2 restore / further 1.5 mm lowering request

Austin reports J3 socket failed; selects immediately preceding J2 unchanged.
Reports roughly 1.5 mm available joystick clearance and authorizes lowering
latest lid by 1.5 mm and printing lid plus J2. Input is his own physical fit
feedback. Codex inspected only original repository sources. No third-party
geometry. Preflight finds existing button retention incompatible with requested
uniform height; no geometry modified or print submitted pending direction.
