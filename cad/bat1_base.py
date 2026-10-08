"""BAT1: v1.7 base with a slot for the RP2040-Plus battery plug (Austin,
2026-10-08, the red Atomic Wedgie). The plug sits centred on the end away
from the USB and its wire runs down to the battery under the Pico. The slot is
cut into the inner face of that end wall, from the floor to the seam, so the
lid tongue and its end catch stay whole. Lid, joystick, buttons unchanged.
Rows BAT1-* in MEASUREMENTS. Run: .venv/bin/python cad/bat1_base.py
"""
import hashlib
import json
import v1_7_lock as L
M,S,P,J,V=L.M,L.S,L.P,L.J,L.V

ROOT=L.ROOT
STL=ROOT/'stl/bat1'
PLUG_W=4.45   # BAT1-PLUG-W: caliper, plug width
SLOT_W=5.0    # BAT1-SLOT: PLUG_W + ~0.27 a side
SLOT_D=1.0    # BAT1-SLOT: Austin, 1 mm into the wall

def slot():
    y=M.IY0  # inner face of the non-USB end (USB_END is top, so Y0 end)
    return M.box(M.PICO_CX-SLOT_W/2,M.PICO_CX+SLOT_W/2,y-SLOT_D,y+P.EPS,M.Z_FLOOR_TOP-P.EPS,S.SEAM)

def main():
    STL.mkdir(parents=True,exist_ok=True)
    L.W.shorten()  # as v1.7 was built
    old,_=L.base()
    b=old-slot()
    def vol(s):return sum(x.volume for x in s.solids())
    gone=vol(old)-vol(b)
    checks=dict(base_valid_single_solid=b.is_valid and len(b.solids())==1,
        removed_is_the_slot=abs(gone-SLOT_W*SLOT_D*(S.SEAM-M.Z_FLOOR_TOP))<.1,  # EPS overlaps
        wall_left_behind_slot=round(M.IY0-SLOT_D-S.Y0,2)>=1.9,
        slot_wider_than_plug=SLOT_W>PLUG_W)
    out=STL/'base-floor-down.stl'
    J.export(V.origin(b),out)
    ref=STL/'_v1_7_check.stl';J.export(V.origin(old),ref)
    checks['v1_7_rebuilds_identical']=ref.read_bytes()==(ROOT/'stl/v1.7/base-floor-down.stl').read_bytes();ref.unlink()
    report=dict(checks=checks,passed=all(checks.values()),wall_behind_slot=round(M.IY0-SLOT_D-S.Y0,2),
        slot_z=[round(M.Z_FLOOR_TOP,2),round(S.SEAM,2)],sha256=hashlib.sha256(out.read_bytes()).hexdigest())
    print(json.dumps(report,indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
