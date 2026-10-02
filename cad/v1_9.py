"""v1.9 PRODUCTION lid + J24-A joystick (Austin, 2026-10-02: "everything is good").
Lid = the V1.9 test lid without the logo: v1.7 stretched 0.3 taller (V1.8-RAISE),
bezel back to 0.3 over the glass (V1.9-BEZEL). Austin: no underwear logo.
Joystick = J24-A: J24-FIT-2 hole, round 10.0 flange with J22's thin edge.
Base (v1.7) and buttons (S2) unchanged.
Rows V1.9-*, J24-* in MEASUREMENTS. Run: .venv/bin/python cad/v1_9.py
"""
import hashlib
import json
from build123d import Pos, Rot
import v1_9_test as T9
import joystick_test as J
import joystick_j24 as J24
M,P=T9.M,T9.P

ROOT=J.ROOT
STL=ROOT/'stl/v1.9'
OUT=ROOT/'renders/v1.9'

def lid():
    # Call only after T9.build(): W.shorten() moves the USB end each time it runs.
    l,_=T9.T8.lid(T9.RAISE)
    gx,gy=M.GLASS_C
    under=(l & M.box(gx-P.S2/2+.1,gx-P.S2/2+.5,gy-5,gy+5,P.S3,10)).bounding_box().min.Z
    return l+T9.bezel_fill(under)

def main():
    STL.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    def vol(s):return sum(x.volume for x in s.solids())
    test,lg,_,_,_=T9.build()  # shortens the case once
    l=lid()
    logo=sum(vol(s) for s in lg.solids())
    c=J24.cap(True)
    checks=dict(lid_valid_single_solid=l.is_valid and len(l.solids())==1,
        lid_is_v1_9_test_without_logo=abs(vol(l)-vol(test)-logo)<.01 and vol(l-test)>0,
        joystick_valid_single_solid=c.is_valid and len(c.solids())==1)
    fd=Rot(180,0,0)*l;bb=fd.bounding_box()
    J.export(Pos(-bb.min.X,-bb.min.Y,-bb.min.Z)*fd,STL/'lid-face-down.stl')
    J.export(Pos(0,0,-J.BOTTOM)*c,STL/'joystick-j24.stl')
    files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(STL.glob('*.stl'))}
    checks['joystick_same_as_tested_J24_A']=files['joystick-j24.stl']==hashlib.sha256((ROOT/'stl/test/j24/joystick-j24-A.stl').read_bytes()).hexdigest()
    report=dict(checks=checks,passed=all(checks.values()),sha256=files)
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
