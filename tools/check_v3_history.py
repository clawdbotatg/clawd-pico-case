"""Compare V3 shells/reused caps to our own committed print history only."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import types

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad'))
import v3_fit as V
import joystick_test as J

def source(path):
    return subprocess.check_output(['git','show','prototype-v2:'+path],cwd=ROOT,text=True)

oldp=types.ModuleType('v2_params')
exec(compile(source('cad/params.py'),'prototype-v2:cad/params.py','exec'),oldp.__dict__)
oldm=types.ModuleType('v2_model')
oldm.P=oldp
code=source('cad/model.py')
assert code.count('import params as P')==1
exec(compile(code.replace('import params as P',''),'prototype-v2:cad/model.py','exec'),oldm.__dict__)
new_buttons=V.buttons();old_buttons=oldm.button_caps()
def vol(shape):return sum(s.volume for s in shape.solids())
result={
    'V2_buttons_added_mm3':vol(new_buttons-old_buttons),
    'V2_buttons_removed_mm3':vol(old_buttons-new_buttons),
    'V2_base_material_removed_mm3':vol(oldm.base()-V.base()),
    'V3_base_added_closing_USB_channel_mm3':vol(V.base()-oldm.base()),
    'V2_USB_bounds_identical':all(abs(getattr(V.M,k)-getattr(oldm,k))<1e-8 for k in ('USB_Z0','USB_Z1','USB_HALF_W','PICO_CX')),
}
assert result['V2_buttons_added_mm3']<1e-5 and result['V2_buttons_removed_mm3']<1e-5
assert result['V2_base_material_removed_mm3']<1e-5
assert result['V2_USB_bounds_identical']
# Re-export J1 cap independently and compare its exact saved binary hash.
import hashlib
import tempfile
with tempfile.TemporaryDirectory() as tmp:
    path=Path(tmp)/'cap.stl'
    J.export(J.Pos(0,0,-J.BOTTOM)*J.cap(),path)
    result['J1_printed_cap_identical']=path.read_bytes()==(ROOT/'stl/joystick-j1/joystick-cap.stl').read_bytes()
assert result['J1_printed_cap_identical']
(ROOT/'renders/v3-fit/history-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
