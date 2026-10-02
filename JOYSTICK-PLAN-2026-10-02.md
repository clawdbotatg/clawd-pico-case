# Joystick + lid plan, 2026-10-02 (for review before anything is printed)

> **Read the FINAL section at the end first.** It supersedes the numbers, the socket design and the print plan below (revised after Codex review).

Austin's three requirements:

1. Each of the 8 directions clicks only its own switches; a centre press clicks only centre.
2. A hard push in any direction, or a hard pull, never takes the cap out of the case.
3. The cap pushes on snug and stays on the stick upside down.

Lid in white, cap in grey, separate prints. No logo: v1.7 lid geometry plus
the changes below.

## What the record actually proves

Rows are in `MEASUREMENTS.md`, results are in `prints/`.

| Fact | Evidence |
|---|---|
| The bare switch is clean. Double clicks happen only with the lid on | V1.5-FEEDBACK ("only with the lid on; with the lid off the stick is clean"), J18-FEEDBACK (bare stick clicks only centre) |
| So double clicks come from the cap touching the lid during a push. Flange edge behind the push rises into the lid underside, pivots there, drives the stem down | J10-FEEDBACK (Austin hears click, then centre click a little farther) |
| More room under the lid helps | V1.5 (+0.5) and V1.8-RESULT (+0.3 "works pretty darn well") |
| Diagonals are the worst with J22. Its four tabs sit on the diagonals at r 5.08, so a NW push lifts the SE tab, the longest lever on the cap | V1.8-FEEDBACK (NW gives N+W+centre); J18-TAB; model below |
| Retention is weak. The disc is 0.3 past the 8.0 hole; the tabs are 1.08 past but only 0.24 thick, so they bend through | J13-ROUND, J17-B / J18-TAB, J13-THIN |
| Grip is short: 0.75 mm of straight square, then the mouth and funnel | J21-DEPTH |
| Socket depth sets whether pressing hits all five (cap bottom lands on the stem's collar) or is loose | J17–J21 results; J4c (collar about 2 mm below the tip, **estimate**) |

## Why the guesses kept missing

Every number that controls requirement 1 was never measured:

| Row | What | Status |
|---|---|---|
| J3 | Switch body top height above PCB | now ~2.8 from photos (J3-PHOTO, ±0.2) |
| J4c | Stem tip to collar top | now ~1.7 from photos (J4c-PHOTO); collar top ~3.35 |
| J5 | Does the stem widen toward its base | photos show it straight (J5-PHOTO) |
| J7 / J8 | Tilt angle and tip travel at full push | never measured |
| J9 | Centre press travel | never measured |
| — | Where the cap actually sits on the stick | **never measured** |

The last one is the worst. `j10_tilt` positions J22 two ways in our own code:

- `v1_8_test.py` uses lift 0.6: cap bottom at z 2.65 above the PCB. On the +0.3 lid it reports **17.1° push, 16.5° diagonal**.
- The J18 rule (stem tip seated on the socket roof; J6 tip 5.00 − depth 1.9) gives lift 1.1: cap bottom at z 3.10. Same cap, same lid: **12.5° push, 10.4° diagonal** (rerun today).

Half a millimetre of ride height moves the answer 5°. The model can't rank
designs until the ride height is measured.

The side photos (J5-PHOTO) show a straight stem, so the tip most likely seats
on the roof: J22's bottom at about 3.10, the collar (top ~3.35) inside the
0.5 deep wide mouth, the body top (~2.8) 0.3 below. That fits J22 working and
J18 (1.7 deep) reaching the collar. M1 confirms it in one reading.

## Design principle

Requirement 1 holds by construction if **no part of the cap touches the lid
anywhere in the switch's full travel**. The bare switch is already clean, so
it becomes the only stop.

Requirement 2 needs a stiff flange well past the hole, and a grip that doesn't
lever off.

These two conflict only because the gap between the flange and the lid
underside is small: about 0.9 mm on the +0.3 lid if the tip seats (lid
underside z 4.30, J22 thin flange top z 3.34). The flange edge on the far
side rises about `r_hole × tan(tilt)` where it passes under the hole edge (r 4.0):

| Tilt | 12° | 15° | 17° | 20° |
|---|---|---|---|---|
| Rise at r 4.0 | 0.85 | 1.07 | 1.22 | 1.46 |

So the fix is room, not a new flange shape:

**Lid (V2.0 test).** v1.7 lid stretched taller by R, with the same prismatic
stretch as V1.5/V1.8 (board hold, seam and catches unchanged). Bezel filled
back to 0.3 over the glass (V1.9-BEZEL). No logo. R is set from the measured
tilt: gap ≥ 4.0·tan(θmax) + 0.3 margin. **Expected R ≈ +1.0 over v1.7, if the
tilt is around 17°.**

**Cap (J24).**
- **Round flange, no tabs**: the same in all 8 directions. Ø10.0 (1.0 past the hole), 0.5 thick everywhere (3 layers; (0.5/0.24)³ ≈ 9× stiffer than J22's edge).
- **Neck longer by R − 0.3**, so the top sits as high above the lid as J22 does on the +0.3 lid (the height Austin liked). This also keeps the ball off the hole's top edge, which limited the +0.5 lid (V1.8-TILT: 15.5° everywhere from the ball).
- **Socket set by a hard stop, not by friction**: the stem tip seats on the roof. The square is sized from the measured stem taper, so it can't jam early. Grip comes from 4 small vertical crush ribs on the top ~1 mm, which print well flange-down and absorb print-to-print size variation (requirement 3). The cap bottom stays a measured margin above the collar and switch body (J3, J4c), so a press can't hit all five.
- Flat top and 1.2 edge, as J22.

**Pull and hard push.** Pulled hard, the cap slides off the stem and the stiff
flange catches under the lid. The next press reseats it. Pushed hard, the
switch's own stop takes the load (the bare switch survives this). The cap
can't tip out, because a Ø10 × 0.5 disc can't pass an 8.0 hole while the neck
keeps it centred.

## Cost

- **Buttons.** Raising the lid more than 0.3 needs new button caps. V1.5 needed taller posts and thicker flanges for +0.5 (V1.5-BUTTON), so this test needs a button set with posts and flanges +R. That makes it 3 prints, not 2.
- **Case height.** The case grows by about R − 0.3 over the +0.3 test lid, roughly 0.7 mm.
- A cheaper option that keeps the case height, a smaller hole (gap needed ∝ hole radius), means a smaller top than the 7.4 Austin chose (J4-BALL). Not proposed unless the measured tilt is small.

## Measurements needed before building (one sitting, about 15 min)

| # | What | How |
|---|---|---|
| M1 | J22 cap top height above the lid top, case closed, +0.3 lid (and v1.7 lid if one is handy) | caliper depth rod. Model: 3.20 if the tip seats, 2.75 if it rides lower |
| M2 | Lid off, J22 on: cap top above the LCD PCB face. Bare stem tip above the PCB (recheck J6 5.00) | depth rod beside the switch |
| M3 | Side photo, level with the PCB, caliper or ruler in frame: bare stick at rest, pushed hard N, pushed hard NE. Same with J22 on | Austin's photos of our board. I read tilt and pivot from them (J7/J8) |
| M4 | Optional: caliper check of J3-PHOTO and J4c-PHOTO | caliper |
| M5 | Centre press: cap top drop when pressed (J9) | depth rod at rest and pressed, or a photo |
| M6 | Does J22 stay on upside down today? Was the +0.5 lid tried with J22? With the +0.3 lid, do the buttons rattle or sit low? Is the cap centred in the hole at rest (photo from above)? | answers |

## Print plan after M1–M6 (one plate)

- 1 lid V2.0 (R from M3), white.
- 3 J24 caps that differ **only in crush-rib interference**: 0.05 / 0.10 / 0.15 per side, 1–3 dice dots. Grey. Everything that sets requirements 1 and 2 is the same on all three, so one plate answers requirement 3 without retesting 1 and 2.
- 1 button set +R, white or grey.

Pass test with the case closed: 20 pushes in each of the 8 directions with no
centre click; 20 centre presses with no direction click; hard push each way;
hard pull; cap upside down on a bare stick for 1 minute.

## Confidence

- **Requirement 1: high**, once M1–M3 are in. It follows from no contact, and we'd have the real tilt to size against. Without M3 it's a guess, and I'll say so.
- **Requirement 2: high** for pulls (stiff, round, 1.0 past the hole). Medium for very hard side pushes: it depends on the grip, and on the switch, which we can't change.
- **Requirement 3: medium.** Crush ribs are the standard fix for FDM tolerance, which is why the plate varies only that.
- **Risk.** If M3 shows tilt above ~22°, R grows past ~1.3. Then I'll propose the smaller-hole option instead and tell you before building.

## FINAL (revised after Codex review, 2026-10-02). Supersedes the numbers and the socket/print plan above.

**Measured** (MEASUREMENTS M1-CASE, M1-CAP, M1, J9, J8):
- J22 sticks up 3.44 above the +0.3 lid (model said 3.20 if the tip seats).
- Press travel is 0.30.
- Tip side travel is ~0.3, by eye.

**Seating.** J22's bottom is ~3.34 above the PCB, not the 3.10 a tip-seated cap would give. The real stop is unknown: friction, collar or tip, ±0.12, since the closed case measured 25.76 against the model's 25.64. Not resolved, and not needed (see Cap).

**Tilt.** Not bounded. ~0.3 travel with the pivot at the body top (~2.8, photo) gives ~8°. That's an estimate, not a maximum. So the design is sized as an envelope: it must clear well past 8°.

**Rise uses the flange's outer edge, not the hole edge.** The flange is under the roof out to its tip. At tilt θ the far edge rises ≈ R·sin θ.

| Cap | Outer radius | Rise at 8° | Gap now (+0.3 lid) | Margin |
|---|---|---|---|---|
| J22 diagonal tab | 5.075 | 0.71 | 0.72 (4.30 − 3.34 − 0.24) | ~0 |
| J22 disc (push N/S/E/W) | 4.3 | 0.60 | 0.72 | 0.12 |

That fits what Austin sees: diagonals double-click, straight pushes mostly don't. It's consistent, but it rests on the 8° estimate, so it isn't proof.

**Old model numbers.** Don't use the logged J22 tilt numbers (V1.8-TILT used lift 0.6). Codex reran `j10_tilt` with the bottom placed at 3.10 (13.1° / 11.0°) and at 3.34 (9.8° / 8.3°); I haven't re-checked these. `j10_tilt` rotates before it translates, so the pivot moves with the lift. The J24 build will place the cap and the pivot in PCB coordinates, separately.

**Cap J24.**
- J22's socket, unchanged. J24 sits on the stick exactly as J22 does, whatever the real stop is.
- Flange: round Ø10.0 (R 5.0), 0.5 thick, no tabs. Bottom face the same as J22's.
- Neck +0.85, matching the lid raise, so the top sticks up 3.44 either way.
- The tip-seated hard stop and the crush ribs proposed above are **dropped**. They add untested changes to the ride height.

**Gap and lid.**
- Flange top ~3.84. Gap target 1.3, so the lid underside goes to ~5.14: **+0.85 over the +0.3 lid** (+1.15 over v1.7).
- Clearance envelope: R·sin θ ≤ 1.3 holds up to **15° (≈2× the 8° estimate)**. The pivot height changes this only slightly at these angles. The J24 build reruns a PCB-referenced sweep at 8°, 12° and 15°, pivots 0 to 3, all 8 directions, cap at bottom 3.22 to 3.46. That covers the flange, neck and ball against the lid.

**Lid stretch.**
- One `T5.stretch(lid, 1.0, 1.15)` copies a slab below the prismatic band (Codex found a 4.0 mm³ omission). The build uses two 0.575 stretches instead, or a verified constant section, and checks the inserted wall against a safe reference by volume.
- Bezel fill as V1.9. No logo.

**Push side.** At 8° the near flange edge drops ~0.70, to ~2.64, near the switch body top (~2.8 ±0.2). J22's disc already drops to ~2.74. Contact on the push side makes a pivot that lifts the stem, not one that presses it, so it shouldn't cause a centre click. It's still unverified: a caliper reading of the switch body top (J3) would settle it.

**Grip (requirement 3).** Still unanswered: does J22 stay on upside down today? 3 caps, square 1.90 (= J22) / 1.87 / 1.84, 1–3 dots. A tighter square may ride higher, so clamp each one's height (M1 method).

**Buttons.** A new set, taller by +0.85 (V1.5-BUTTON method).

**Acceptance: the FULL test on EVERY cap**, case closed:
- 20 pushes in each of the 8 directions, no centre click
- 20 centre presses, no direction click
- hard push each way
- hard pull, then check that the cap reseats and every switch still works
- upside down on a bare stick for 1 minute
- clamp the height

Reseating after a pull is only an assumption until this test.

**Confidence.**
- Requirement 1: medium-high. Clears ~2× the estimated tilt, with no reliance on the old model.
- Requirement 2: medium-high for pulls, medium for hard side pushes.
- Requirement 3: medium. It depends on Austin's answer and the 3 squares.
