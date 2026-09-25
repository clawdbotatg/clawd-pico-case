"""Export every part to stl/ and write the browser viewer to renders/viewer.html.

    ../.venv/bin/python build.py

The viewer embeds the STLs (base64) so it is one self-contained file: open it
locally, or publish it. Three.js comes from cdnjs; everything else is inline.
"""
import base64
import json
import os
import subprocess
import hashlib
from pathlib import Path
from importlib.metadata import version

from build123d import export_stl
import model

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STL = os.path.join(ROOT, "stl")
RENDERS = os.path.join(ROOT, "renders")
os.makedirs(STL, exist_ok=True)
os.makedirs(RENDERS, exist_ok=True)

# Never export a new print set after a failed geometric audit.
import validate
audit = validate.run()
if not audit['passed']:
    raise SystemExit('Geometric audit failed; see renders/validation.json')


def git_short():
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                                capture_output=True, text=True).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--", "cad"], cwd=ROOT,
                               capture_output=True, text=True).stdout.strip()
        return commit + ('-modified' if dirty else '')
    except OSError:
        return "?"


parts = []
for name, (fn, color) in model.PARTS.items():
    part = fn()
    path = os.path.join(STL, f"{name}.stl")
    export_stl(part, path, tolerance=0.02, angular_tolerance=0.1)
    bb = part.bounding_box()
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    parts.append({"name": name, "color": color, "stl": data,
                  "bbox": [round(v, 2) for v in (bb.min.X, bb.min.Y, bb.min.Z, bb.max.X, bb.max.Y, bb.max.Z)]})
    print(f"{name:13} {os.path.getsize(path)//1024:5d} KB")

# Print orientation: flat face on the plate, no supports. The lid and the
# joystick cap print upside down (top face on the plate); everything else as
# modelled. Written to stl/print/ with z-min at 0.
from build123d import Rot, Pos
PRINT_FLIP = {"lid", "joystick_cap"}
os.makedirs(os.path.join(STL, "print"), exist_ok=True)
for name, (fn, _) in model.PARTS.items():
    if name in ("hat", "pico", "fpc_tape"):
        continue
    part = fn()
    if name in PRINT_FLIP:
        part = Rot(180, 0, 0) * part
    bb = part.bounding_box()
    part = Pos(-bb.min.X, -bb.min.Y, -bb.min.Z) * part
    export_stl(part, os.path.join(STL, "print", f"{name}.stl"), tolerance=0.02, angular_tolerance=0.1)
    bb = part.bounding_box()
    print(f"print/{name:13} {bb.max.X:6.2f} x {bb.max.Y:6.2f} x {bb.max.Z:5.2f} mm, flat face down{' (flipped)' if name in PRINT_FLIP else ''}")

# Complete caps, not misleading nominal-only hole coupons: same print orientation.
sample_dir = Path(STL) / 'fit_samples'
sample_dir.mkdir(exist_ok=True)
import params as P
for clearance in P.JOY_SOCKET_SAMPLES:
    sample = Rot(180, 0, 0) * model.joystick_cap(clearance)
    bb = sample.bounding_box()
    sample = Pos(-bb.min.X, -bb.min.Y, -bb.min.Z) * sample
    export_stl(sample, str(sample_dir / f'joystick_socket_{P.J4 + clearance:.2f}.stl'),
               tolerance=0.02, angular_tolerance=0.1)

from build123d import export_step, Compound
asm = Compound(children=[model.PARTS[n][0]() for n in model.PARTS])
export_step(asm, os.path.join(STL, "assembly.step"))
print("assembly.step", os.path.getsize(os.path.join(STL, "assembly.step")) // 1024, "KB")

import params as P
info = {
    "commit": git_short(),
    "case_mm": [round(model.X1 - model.X0, 2), round(model.Y1 - model.Y0, 2), round(model.Z_LID_TOP - model.Z_BOTTOM, 2)],
    "split_z": model.Z_SPLIT,
    "assumptions": ["R4 prototype for the measured PINK USB-C board; physical fit unverified",
                    "Pico centring, stack datum and USB projection need confirmation",
                    "Joystick body 3.0 mm assumed; tilt/click and cap retention unmeasured",
                    "Plug recess trial: 12.5 x 7 mm; both USB height readings accommodated",
                    "Blue flag conflicts with lid: remove only if confirmed protector tab",
                    "Bare corner pads, underside shelf clearance and snap flex need bench tests"],
}

with open(os.path.join(os.path.dirname(__file__), "viewer_template.html")) as f:
    html = f.read()
html = html.replace("/*__PARTS__*/", "const PARTS = " + json.dumps(parts) + ";") \
           .replace("/*__INFO__*/", "const INFO = " + json.dumps(info) + ";")
out = os.path.join(RENDERS, "viewer.html")
with open(out, "w") as f:
    f.write(html)
print("viewer", out, os.path.getsize(out) // 1024, "KB")

manifest = {'revision': 'R4', 'git': git_short(), 'source_sha256': audit['source_sha256'],
            'build123d': version('build123d'), 'files': {}}
for path in sorted(Path(STL).rglob('*')):
    if path.suffix in ('.stl', '.step'):
        manifest['files'][str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
(Path(STL) / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

import render
render.render()
print('preview renders/r4-preview.png')
