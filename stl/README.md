Built outputs only; run `.venv/bin/python cad/build.py` from repository root.
Never hand-edit meshes. MIT, like the original source.

`print/` holds base, lid, four button caps, and default joystick cap in print
orientation. Separate button solids on the bed. `fit_samples/` holds alternate
joystick caps named for socket width; try largest first without forcing.
Top-level STL/STEP uses assembled positions and includes illustrative hardware.
`manifest.json` records source/output SHA-256 hashes and tool version.
R4 is an unprinted prototype; print/assembly details in REPORT.md.
