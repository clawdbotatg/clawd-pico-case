# Low-lid experiments — not print approval

D7 side-tab experiment: lid exactly1 mm above glass. Nominal assembly and
5-degree lid motion clear;16 required10-degree lid motion checks fail.
Preserve this failed checkpoint, not a printable solution. Review-only
builder generates viewer/validation but no print artifacts, and leaves the
strict standard export gate intact. All motion assumptions remain explicit.

## D8 rear-tab revision — current review

The lid is now **1.00 mm above the glass**, at z=3.05. Body height is
23.69 mm, versus 29.24 mm in the rejected tall V3 draft. There is no raised
collar. USB alignment/closed opening, pry notches and bottom access remain.

The joystick keeps the earlier full-case socket and the V2-sized ball with
its printing flat. A single arm behind the joystick ends in a retaining
tab beyond the PCB edge. It fits inside a pocket in the rear wall, allowing
it to tilt below the PCB plane without hitting the board. No external USB
tab returns; this is a different, internal feature belonging to the cap.

Button footprints and 1.8 mm protrusion remain. Their retaining wings now
run beside the switch bodies, below the plunger tops. This lets the lid sit
lower. Underside relief still contacts each plunger at its measured height.

The failed side-tab experiment is preserved at commit2587340. The rear-tab
draft is a separate revision, not a claim that the earlier failures passed.

### Review and limitations

Current D8 result: **495 required CAD checks passed**. The full chosen
10-degree scenarios now clear the lid, base and PCB; the new rear arm also
clears the modelled fixed hardware. The earlier neck still has48 intersections
in guessed-body scenarios, recorded separately, so this is not proof of
actual joystick fit. Browser controls passed a Chromium smoke test with no
JavaScript errors. Review manifest hashes were independently checked.

LAN preview path: `/v3-low/viewer.html` on the existing server, port8793.
The existing `/viewer.html` path also serves the same low-lid model.

- Browser: `renders/v3-low/viewer.html` or the existing `renders/viewer.html`.
- Audit: `renders/v3-low/validation.json`; source and viewer hashes beside it.
- No new print files or printer submissions. Existing `stl/print/` files
  are the OLD tall draft, **not this revision**. Do not print them.
- The rear tab and its arm have thin sections. Mechanical strength and
  slicer continuity are unverified; the tip's clearance at the most extreme
  sampled angle is small. Do not call this production-ready.
- The body/pivot/travel of the real joystick remain unmeasured. Required
  motion checks test chosen 0/5/10-degree angles, two pivot heights and
  0/0.3 mm press. They do not establish the actual travel specification.
- Legacy socket/neck intersections with the guessed hardware body remain
  separate unresolved diagnostics. New rear-arm/hardware intersections are
  required checks, as are complete cap/lid, cap/base and cap/PCB clearance.
- Still no support-free slicer verification. Planned lid, joystick and cap
  orientations are flat top down. Small bridges/overhangs need inspection.
- Browser approval comes before any print request. Physical motion and
  retention still need a fit test even after the CAD checks pass.
