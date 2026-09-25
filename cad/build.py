"""Export every part to stl/ and write the browser viewer to renders/viewer.html.

    ../.venv/bin/python build.py

The viewer embeds the STLs (base64) so it is one self-contained file: open it
locally, or publish it. Three.js comes from cdnjs; everything else is inline.
"""
import base64
import json
import os
import subprocess

from build123d import export_stl
import model

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STL = os.path.join(ROOT, "stl")
RENDERS = os.path.join(ROOT, "renders")
os.makedirs(STL, exist_ok=True)
os.makedirs(RENDERS, exist_ok=True)


def git_short():
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True).stdout.strip()
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

import params as P
info = {
    "commit": git_short(),
    "case_mm": [round(model.X1 - model.X0, 2), round(model.Y1 - model.Y0, 2), round(model.Z_LID_TOP - model.Z_BOTTOM, 2)],
    "split_z": model.Z_SPLIT,
    "assumptions": ["Pico centred under the hat (rows A3/L8 not measured)",
                    "LCD corner radius 1.5 and joystick body height 3.0 are guesses (L4, J3 unmeasured)",
                    "USB-C cutout fits the shell + 0.5; the cable plug's overmold is not measured"],
}

with open(os.path.join(os.path.dirname(__file__), "viewer_template.html")) as f:
    html = f.read()
html = html.replace("/*__PARTS__*/", "const PARTS = " + json.dumps(parts) + ";") \
           .replace("/*__INFO__*/", "const INFO = " + json.dumps(info) + ";")
out = os.path.join(RENDERS, "viewer.html")
with open(out, "w") as f:
    f.write(html)
print("viewer", out, os.path.getsize(out) // 1024, "KB")
