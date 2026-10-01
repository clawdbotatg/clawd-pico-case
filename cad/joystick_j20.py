"""J20: J19-2 (1.5 total depth, J17-B tabs) with a wide round mouth.
Austin, 2026-09-30: "a total depth of 1.5 ... for the first 0.5, a nice wide
opening ... wide enough to fit over the whole base", as the earlier caps had.
Socket from the bed face up: round MOUTH_D for MOUTH_H (clears the 2.94
collar, J4b), a 45 deg round-to-square funnel (J7's printable step: no flat
ledge over air), the 1.90 square to the flat roof at 1.5, then J7's pyramid.
The straight square grip is what is left above the funnel.
Flat top. Row J20 in MEASUREMENTS. Run: .venv/bin/python cad/joystick_j20.py
"""
import hashlib
import json
from build123d import Pos, Plane, Circle, Rectangle, loft
import joystick_test as J
import joystick_j4 as J4
import joystick_j7 as J7
import joystick_j8 as J8
import joystick_j15 as J15
import joystick_j16 as J16
import joystick_j17 as J17
import joystick_j18 as J18
import j10_tilt as TILT

ROOT=J.ROOT
STL=ROOT/'stl/v1.4/joystick-j20'
OUT=ROOT/'renders/v1.4/joystick-j20'
DEPTH=1.5             # J20: Austin, J19-2's total depth (bed face to the flat roof)
MOUTH_D,MOUTH_H=3.2,.5  # J20-MOUTH: 0.13 per side over the 2.94 collar; Austin's 0.5
SQUARE=J16.SQUARE     # 1.90
TAB_SCALE=J18.TAB_SCALE

def cavity(depth=DEPTH):
    z1=J.BOTTOM+MOUTH_H;z2=z1+(MOUTH_D-SQUARE)/2;roof=J.BOTTOM+depth;h=SQUARE/2
    funnel=loft([Plane.XY.offset(z1)*Circle(MOUTH_D/2),Plane.XY.offset(z2)*Rectangle(SQUARE,SQUARE)])
    # The mouth ends exactly on the funnel's start circle: no sliver ledge.
    return (J.cylinder(MOUTH_D,J.BOTTOM-J.P.TOOL_EXT,z1)+funnel+J.M.box(-h,h,-h,h,z2-J.P.EPS,roof)
            +J7.frustum(SQUARE,0,roof,roof+h))

def cap(depth=DEPTH,n=0):  # J21 passes deeper holes and dice dots
    w,tip=J17.tab(TAB_SCALE)
    c=J15.cap()+(J8.cavity(SQUARE,J16.LIFT) & J.cylinder(J.NECK,J.BOTTOM,J4.FLAT_Z))  # J15 with its socket filled
    fl=None
    for f in J16.flares(w,tip):fl=f if fl is None else fl+f
    c=c+(fl-J16.thin(J16.FLARE_T))-cavity(depth)
    for p in J17.pips(n):c-=p
    return c

def main():
    STL.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    def vol(s):return sum(x.volume for x in s.solids())
    c=cap();h=SQUARE/2;roof=J.BOTTOM+DEPTH;z2=J.BOTTOM+MOUTH_H+(MOUTH_D-SQUARE)/2
    j19_2=J18.cap(1.5,0)  # J19-2 without dots, for comparison
    outside=J.M.box(-7,7,-7,7,J.BOTTOM-1,20)-J.cylinder(MOUTH_D+.2,J.BOTTOM-2,roof+2)
    checks=dict(valid_single_solid=c.is_valid and len(c.solids())==1,
        mouth_clears_collar=vol(c & J.cylinder(2.94+.02,J.BOTTOM,J.BOTTOM+MOUTH_H))<1e-6,
        mouth_wider_than_collar=MOUTH_D>2.94,
        roof_at_1_5=vol(c & J.M.box(-h,h,-h,h,roof-.02,roof-.01))<1e-6 and vol(c & J.M.box(-.05,.05,-.05,.05,roof+h+.05,roof+h+.15))>0,
        square_grip_above_funnel=vol(c & J.M.box(-h,h,-h,h,z2,roof))<1e-6 and roof-z2>0,
        stem_fits=J.overlap(J.M.box(-J.P.J4/2,J.P.J4/2,-J.P.J4/2,J.P.J4/2,z2,roof),c)<1e-6,
        no_flat_overhang_in_socket=not J7.overhangs(c),
        same_as_J19_2_outside_socket=vol((c&outside)-(j19_2&outside))<1e-4 and vol((j19_2&outside)-(c&outside))<1e-4,
        flat_top=abs(c.bounding_box().max.Z-J4.FLAT_Z)<1e-6)
    path=STL/'joystick-j20.stl';J.export(Pos(0,0,-J.BOTTOM)*c,path)
    tilt=TILT.tilt({'J20':(c,J16.LIFT+J18.J16_DEPTH-DEPTH)})
    report=dict(checks=checks,passed=all(checks.values()),straight_grip=round(roof-z2,3),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),tilt=tilt)
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(checks=checks,passed=report['passed'],straight_grip=report['straight_grip'],sha256=report['sha256']),indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
