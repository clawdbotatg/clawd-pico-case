"""J24-FIT: three J22 caps that differ only in how far down the tight square goes.
Austin, 2026-10-02 (J22-GRIP): J22 holds upside down "but could be better";
the stick never reaches the wide part of the hole, so make the tight hold go
further down and open up wide only right at the end. Grip length, not width:
  1 dot  J22's opening (3.2 x 0.5 + 45 deg funnel): 0.75 straight square
  2 dots 3.1 x 0.35 opening + 45 deg funnel: 0.95
  3 dots J16's 0.25 x 45 deg chamfer only: 1.65
All 1.90 square, roof at 1.9 (J22), J22 outside. Caps only, no lid needed.
Rows J24-FIT in MEASUREMENTS. Run: .venv/bin/python cad/joystick_j24_fit.py
"""
import hashlib
import itertools
import json
from build123d import Pos, Plane, Circle, Rectangle, Compound, loft
import joystick_test as J
import joystick_j4 as J4
import joystick_j7 as J7
import joystick_j14 as J14
import joystick_j16 as J16
import joystick_j17 as J17
import joystick_j20 as J20
import joystick_j22 as J22

ROOT=J.ROOT
STL=ROOT/'stl/test/j24-fit'
OUT=ROOT/'renders/test/j24-fit'
SQUARE=J20.SQUARE        # 1.90, J22
DEPTH=J22.DEPTH          # 1.9, J22
OPEN={'1':('round',J20.MOUTH_D,J20.MOUTH_H),  # J22
      '2':('round',3.1,.35),                  # J24-FIT-2: 0.08 per side over the 2.94 collar (J4b); 0.35 > its ~0.2 reach (J4c-PHOTO)
      '3':('chamfer',J16.MOUTH_CH,None)}      # J24-FIT-3: J16-SOCKET's chamfer, 2.40 at the bed face

def cavity(kind,a,b):
    roof=J.BOTTOM+DEPTH;h=SQUARE/2
    if kind=='round':
        z1=J.BOTTOM+b;z2=z1+(a-SQUARE)/2
        low=J.cylinder(a,J.BOTTOM-J.P.TOOL_EXT,z1)+loft([Plane.XY.offset(z1)*Circle(a/2),Plane.XY.offset(z2)*Rectangle(SQUARE,SQUARE)])
    else:
        z2=J.BOTTOM+a
        low=(J7.frustum(SQUARE+2*a,SQUARE,J.BOTTOM,z2)
             +J.M.box(-h-a,h+a,-h-a,h+a,J.BOTTOM-J.P.TOOL_EXT,J.BOTTOM+J.P.EPS))
    return low+J.M.box(-h,h,-h,h,z2-J.P.EPS,roof)+J7.frustum(SQUARE,0,roof,roof+h),z2

def cap(name):
    kind,a,b=OPEN[name]
    c=J22.cap()+(J20.cavity(DEPTH)&J.cylinder(J.NECK,J.BOTTOM,J4.FLAT_Z))  # J22 with its socket filled
    cav,z2=cavity(kind,a,b)
    c=c-cav
    for p in J17.pips(int(name)):c-=p
    return c,z2

def main():
    STL.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    def vol(s):return sum(x.volume for x in s.solids())
    def dv(a,b,r):  # volume of (a-b) inside r, tolerating an empty difference
        d=a-b;return vol(d&r) if d.solids() else 0.
    j22=J22.cap();h=SQUARE/2;roof=J.BOTTOM+DEPTH
    outside=J.M.box(-7,7,-7,7,J.BOTTOM-1,J4.FLAT_Z-1)-J.cylinder(J20.MOUTH_D+.2,J.BOTTOM-2,J4.FLAT_Z)
    checks={};parts={};grip={}
    for name in OPEN:
        c,z2=cap(name);grip[name]=round(roof-z2,3)
        checks[name+'_valid_single_solid']=c.is_valid and len(c.solids())==1
        checks[name+'_roof_at_1.9']=vol(c & J.M.box(-h,h,-h,h,roof-.02,roof-.01))<1e-6 and vol(c & J.M.box(-.05,.05,-.05,.05,roof+h+.05,roof+h+.15))>0
        checks[name+'_stem_fits']=J.overlap(J.M.box(-J.P.J4/2,J.P.J4/2,-J.P.J4/2,J.P.J4/2,z2,roof),c)<1e-6
        checks[name+'_square_solid_around']=vol(c & (J.M.box(-h-.05,h+.05,-h-.05,h+.05,z2+.01,roof-.01)-J.M.box(-h,h,-h,h,z2,roof)))>0.9*4*(SQUARE+.05)*.05*(roof-z2-.02)
        checks[name+'_no_flat_overhang_in_socket']=not J7.overhangs(c)
        checks[name+'_same_as_J22_outside_socket']=dv(c,j22,outside)<1e-4 and dv(j22,c,outside)<.5  # only the dots differ
        if name=='1':core=J.cylinder(J20.MOUTH_D+.2,J.BOTTOM-1,J4.FLAT_Z-1);checks['1_socket_is_J22']=dv(c,j22,core)<1e-6 and dv(j22,c,core)<1e-6
        if name=='2':checks['2_opening_clears_collar']=vol(c & J.cylinder(2.94+.02,J.BOTTOM,J.BOTTOM+.35))<1e-6
        parts[name]=Pos(0,0,-J.BOTTOM)*c
        J.export(parts[name],STL/('joystick-j24-fit-'+name+'.stl'))
    checks['grip_longer_each_step']=grip['1']<grip['2']<grip['3']
    step=2*J17.tab(J20.TAB_SCALE)[1]+J14.GAP
    placed=[Pos(i*step,0,0)*p for i,p in enumerate(parts.values())]
    checks['plate_separate']=all(J.overlap(a,x)<1e-6 for a,x in itertools.combinations(placed,2))
    J.export(Compound(children=placed),STL/'joystick-j24-fit-plate.stl')
    report=dict(status='TEST, not current',checks=checks,passed=all(checks.values()),straight_grip=grip,
        sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(STL.glob('*.stl'))})
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
