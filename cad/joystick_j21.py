"""J21: J20's wide mouth (3.2 x 0.5 + funnel) on deeper holes.
Austin, 2026-09-30: J20's 1.5 "is not nearly deep enough": 1.9 (1 dot) and
2.0 (2 dots), same wide opening and J17-B tabs.
Row J21 in MEASUREMENTS. Run: .venv/bin/python cad/joystick_j21.py
"""
import hashlib
import itertools
import json
from build123d import Pos, Compound
import joystick_test as J
import joystick_j4 as J4
import joystick_j7 as J7
import joystick_j14 as J14
import joystick_j16 as J16
import joystick_j17 as J17
import joystick_j18 as J18
import joystick_j20 as J20

ROOT=J.ROOT
STL=ROOT/'stl/v1.4/joystick-j21'
OUT=ROOT/'renders/v1.4/joystick-j21'
DEPTHS={'1':1.9,'2':2.0}  # J21-DEPTH: dots -> total depth

def main():
    STL.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    def vol(s):return sum(x.volume for x in s.solids())
    checks={};parts={};h=J20.SQUARE/2
    z2=J.BOTTOM+J20.MOUTH_H+(J20.MOUTH_D-J20.SQUARE)/2
    j20=J20.cap();outside=J.M.box(-7,7,-7,7,J.BOTTOM-1,J4.FLAT_Z-1)-J.cylinder(J20.MOUTH_D+.2,J.BOTTOM-2,J4.FLAT_Z)
    for name,depth in DEPTHS.items():
        c=J20.cap(depth,int(name));roof=J.BOTTOM+depth
        checks[name+'_valid_single_solid']=c.is_valid and len(c.solids())==1
        checks[name+'_mouth_clears_collar']=vol(c & J.cylinder(2.94+.02,J.BOTTOM,J.BOTTOM+J20.MOUTH_H))<1e-6
        checks[name+'_roof_at_'+str(depth)]=vol(c & J.M.box(-h,h,-h,h,roof-.02,roof-.01))<1e-6 and vol(c & J.M.box(-.05,.05,-.05,.05,roof+h+.05,roof+h+.15))>0
        checks[name+'_stem_fits']=J.overlap(J.M.box(-J.P.J4/2,J.P.J4/2,-J.P.J4/2,J.P.J4/2,z2,roof),c)<1e-6
        checks[name+'_no_flat_overhang_in_socket']=not J7.overhangs(c)
        checks[name+'_same_as_J20_outside_socket']=vol((c&outside)-(j20&outside))<1e-4 and vol((j20&outside)-(c&outside))<1e-4
        parts[name]=Pos(0,0,-J.BOTTOM)*c
        J.export(parts[name],STL/('joystick-j21-'+name+'.stl'))
    step=2*J17.tab(J20.TAB_SCALE)[1]+J14.GAP
    placed=[Pos(i*step,0,0)*p for i,p in enumerate(parts.values())]
    checks['plate_separate']=all(J.overlap(a,x)<1e-6 for a,x in itertools.combinations(placed,2))
    plate=STL/'joystick-j21-plate.stl';J.export(Compound(children=placed),plate)
    report=dict(checks=checks,passed=all(checks.values()),depths=DEPTHS,straight_grip={n:round(J.BOTTOM+d-z2,3) for n,d in DEPTHS.items()},
        sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(STL.glob('*.stl'))})
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
