"""Build a clearly labelled inspection viewer, even when motion checks fail.

NEVER exports print files, invokes a slicer or submits a print. The normal
cad/build.py gate still refuses printing artifacts after required failures.
"""
import base64
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from build123d import export_stl
import model as M
import params as P
import validate
import render

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'renders/v3-low'
OUT.mkdir(exist_ok=True)
audit = validate.run(OUT / 'validation.json')
failures = [c for c in audit['checks'] if not c['passed']]
parts = []
with tempfile.TemporaryDirectory(prefix='pico-low-review-') as temp:
    for name, (fn, color) in M.PARTS.items():
        shape = fn()
        assert shape.is_valid, name
        path = Path(temp) / (name + '.stl')
        export_stl(shape, str(path), tolerance=.02, angular_tolerance=.1)
        bb = shape.bounding_box()
        parts.append(dict(name=name, color=color, stl=base64.b64encode(path.read_bytes()).decode(),
                          bbox=[round(v, 2) for v in (bb.min.X, bb.min.Y, bb.min.Z, bb.max.X, bb.max.Y, bb.max.Z)]))
commit = subprocess.check_output(['git','rev-parse','--short','HEAD'],cwd=ROOT,text=True).strip()
info = dict(commit=commit+'-low-lid-draft', case_mm=[round(M.X1-M.X0,2),round(M.Y1-M.Y0,2),round(M.Z_LID_TOP-M.Z_BOTTOM,2)],split_z=0,
            assumptions=['LOW-LID EXPERIMENT — NOT PRINT READY',
                         'Lid exactly 1 mm above glass; no collar or USB tab',
                         'Single rear retaining tab, not the failed side-tab experiment',
                         'Actual joystick travel is unmeasured; 0/5/10-degree scenarios are design checks only',
                         'Earlier full-case 2.01 mm socket retained; same ball and top printing flat',
                         'Button side wings moved below plunger; support-free slicing not verified',
                         'Pry access, bottom hole and closed USB alignment retained',
                         'No print files generated or sent from this experimental review',
                         'Blue flag and unmeasured joystick body remain unresolved',
                         str(len(failures))+' required checks failed; see /v3-low/validation.json',
                         'Thin rear heel/arm strength and support-free slicing need verification'])
html=(ROOT/'cad/viewer_template.html').read_text().replace('/*__PARTS__*/','const PARTS = '+json.dumps(parts)+';').replace('/*__INFO__*/','const INFO = '+json.dumps(info)+';')
status='CHECKS FAILED' if failures else 'REVIEW ONLY — NOT PRINT APPROVED'
html=html.replace('V3 review · NOT APPROVED FOR PRINT','V3 low lid · '+status)
html=html.replace('V3 Case Review — Not Approved for Print','V3 Low Lid — '+status)
(OUT/'viewer.html').write_text(html)
# Update the existing browser URL, but leave old print artifacts untouched.
(ROOT/'renders/viewer.html').write_text(html)
render.render(OUT/'preview.png')
manifest=dict(revision='v3-low-lid-experiment',print_ready=False,source_sha256=audit['source_sha256'],
              passed_checks=sum(c['passed'] for c in audit['checks']),failed_checks=failures,
              files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.name!='manifest.json'})
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Inspection viewer updated; no print files exported. Failures:',len(failures))
