# Current state — V1 feedback and next-version draft

Austin calls the photographed first-principles print **V1**. It is this
repository's original MIT case. The exact CAD commit used for that physical
print has not been matched; internal R4/R5 CAD names are not confirmed
physical print version numbers.

See [V1 feedback and photos](prints/2026-09-24-v1-feedback.md).
Most things fit well according to Austin. Five changes are requested:

1. Smaller, taller ball joystick, installed on the board before the lid;
   an internal lip retains it.
2. Small seam notch for prying the case open.
3. USB-C opening higher and smaller, centred on the actual connector.
4. Wider, taller rectangular buttons, with smaller top/bottom flange lips.
5. Bottom access hole over the pink board button; identity, location and
   pad size need confirmation before cutting it.

## Saved draft, not ready to print

Current CAD is an R5 work-in-progress implementing only items 1 and 2.
Items 3–5 remain pending. No R5 files have been submitted to print.

- Joystick: Ø7 ball; Ø4.2 shaft; Ø10.4 internal flange; Ø8.8 lid throat.
  Ball passes through during lid installation; flange cannot. Raised
  collar top z=8; ball top z=14.9. Body height 28.64; overall height 35.54 mm.
- Two rounded seam notches: 6 wide × 1.6 high × 1 deep, centred on the
  long sides between catches. Nominal remaining wall 1.2 mm.
- 273 CAD checks passed, including continuous lid installation over the
  fitted joystick, upward retention, movement scenarios, and clearance
  for a 4 × 0.6 mm plastic tool tip inserted 0.7 mm.
- Sphere tessellation has a zero-area pole triangle. Mesh closure is
  checked excluding degenerate triangles; slicer review remains necessary.
- Lid is inverted and joystick upright for printing. Raised collar leaves
  the broad lid face above the bed: supports are required there. Joystick
  flange/ball also need support review; keep supports out of the socket.

[Preview](renders/r5-preview.png), [viewer](renders/viewer.html),
[checks](renders/validation.json), [hashes](stl/manifest.json).

## Assembly and limitations

Fit the joystick onto the bare board stick first. Insert button caps from
inside the lid, then lower the lid over the installed ball; lip stays inside.
Mate base and lid after checking board supports, USB and free control motion.
Use a thin plastic tool in the seam notch; stop if force is excessive.

Body height, pivot, travel and stem lip remain unmeasured. The chosen
0/5/10-degree and 0/0.3-mm press scenarios are not hardware specs. Flange
lift is 1 mm versus 1.2 mm socket engagement: only 0.2 mm nominal engagement
remains at the retaining stop. Physical retention testing is essential.
Unresolved blue flag intersects the lid by 5.28 mm³. Do not close on or cut
it; remove only if confirmed removable protector packaging. Stack datum,
cable envelope, board support areas and snap forces remain unverified.
See the [R4 evidence audit](reports/r4-engineering-review.md).

R4 has a hold/superseded request posted through the HTTP inbox;
operator acknowledgment is unconfirmed. No running print was interrupted.
