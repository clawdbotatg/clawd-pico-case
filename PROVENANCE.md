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
