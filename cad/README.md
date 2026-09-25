Original build123d CAD. Read `../CLAUDE.md` and `../PROCESS.md` first.
Hardware inputs and R4 choices cite `../MEASUREMENTS.md`; reasons in DESIGN.md.

From repository root: `.venv/bin/python cad/build.py`.
`params.py` defines hardware/choices; `model.py` constructs parts;
`validate.py` checks collision/motion scenarios; `render.py` produces a static
preview from CAD tessellation; `build.py` audits then exports all outputs.
Dependencies are pinned in requirements.txt. Validation is conditional on the
recorded measurements and explicit assumptions; see REPORT.md before printing.
