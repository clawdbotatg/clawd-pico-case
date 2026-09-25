# Design and print iteration register

Every saved design revision belongs in git with its original CAD, generated
STL/STEP files, rationale, evidence and validation results. Print jobs must
reference an immutable commit/tag and record slicer settings, artifact hashes,
delivery/start status and the eventual fit result. Never replace a failed
version's history with a corrected version or describe a queued job as printed.

## Historical designs (2026-09-24)

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
