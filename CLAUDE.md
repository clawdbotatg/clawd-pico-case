# Rules for agents in this repo

This is a clean-room design. Read this whole file before doing anything.

## Never do these

1. Do not open, read, fetch, download, screenshot or search for any existing
   case for the Waveshare Pico-LCD-1.3 or the Raspberry Pi Pico. That includes
   Printables, MakerWorld, Thingiverse, Thangs, Cults, GitHub, image search and
   the Waveshare wiki's user gallery. The two designs we must not touch are
   listed in `SOURCES.md`. Do not visit those URLs even to "check something".
2. Do not open `~/picowallet/case/`, `~/picowallet/tools/zezbase`,
   `~/picowallet/tools/zezplate`, `~/picowallet/emu/` mesh or 3D files, or the
   case sections of `~/picowallet/HANDOFF.md`, `case/README.md` or
   `case/BUTTONS.md`. Those derive from the forbidden designs.
3. Do not start a session for this repo from inside `~/picowallet`. Start it
   from this directory. Do not load picowallet memory or notes.
4. Do not use a dimension you "remember" or "know" about the LCD board or the
   case. Every number in `cad/` must reference a row in `MEASUREMENTS.md`,
   and every row there must name its source: a caliper reading with a photo,
   or a datasheet page.
5. Do not bring in third-party geometry of any license, including MIT and CC0
   files, without Austin's written OK in `PROVENANCE.md`. Default is none.

## Always do these

- Design in build123d (Python), parametric, in `cad/`. Every parameter has a comment
  naming the measurement row it comes from.
- Log every design input in `PROVENANCE.md` the moment you use it: what, from
  where, which license, who added it, date. That file is append-only.
- Log every print in `prints/` with the date, material, settings, what fit and
  what did not. Photos welcome.
- Write design decisions in `DESIGN.md` with the reason. Closure method, wall
  thickness, corner treatment, cap shape, tolerances.
- If you notice you have seen a forbidden design in this session, stop, say
  so in `PROVENANCE.md`, and do not write geometry in that session.
- If Austin sends a file or a number, ask where it came from before using it,
  unless he says.

## Why so strict

We want to sell this. Copyright claims turn on access plus copying. We had
access to the other designs in a different repo, so our defense is a paper
trail showing independent creation: source files that grow from measured
numbers, dated commits, and sessions that never had the other files in front
of them. Every shortcut weakens that trail.

## Commit identity

This repo lives in `~/clawd/`. Commit and push as clawdbotatg over HTTPS, per
the global rules. Copyright holder in `LICENSE` is Austin Griffith.
