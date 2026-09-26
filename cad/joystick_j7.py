"""J7 test set: J6 A/B/C with a self-supporting stick socket. Printed flange
down, J6's socket had a flat ledge (round mouth -> square) and a flat roof in
mid-air; PETG strung across both (IMG_0887). J7 replaces the ledge with a 45
degree funnel and the roof with a 45 degree pyramid. The round mouth still
clears the 2.94 base lip (J4b) and the square grips the 1.86 stem (J4).
Stops barely move: the pyramid only lets a 1.86 tip rise ~0.05 further.
Rows J7-* in MEASUREMENTS. Run: .venv/bin/python cad/joystick_j7.py
"""
import hashlib
import itertools
import json
import math
from pathlib import Path
from build123d import Pos, Compound, Plane, Rectangle, Circle, loft
import joystick_test as J
import joystick_j2 as J2
import joystick_j4 as J4
import joystick_j6 as J6

ROOT=J.ROOT
STL=ROOT/'stl/v1.4/joystick-j7'
OUT=ROOT/'renders/v1.4/joystick-j7'
Z0=J.BOTTOM+J6.ROUND_DEPTH  # top of the round mouth (unchanged from J6)
ROOF=Z0+J2.SQUARE_DEPTH  # top of the square grip (unchanged from J6)

def frustum(w0,w1,z0,z1):
    # Square frustum; w1=0 gives a pyramid (tiny tip keeps the loft valid).
    return loft([Plane.XY.offset(z0)*Rectangle(w0,w0),Plane.XY.offset(z1)*Rectangle(max(w1,.001),max(w1,.001))])

def cavity(square):
    mouth=J.cylinder(J2.ROUND_D,J.BOTTOM-J.P.TOOL_EXT,Z0)
    # Round-to-square funnel: the flats drop 45 deg, the corners steeper.
    funnel=loft([Plane.XY.offset(Z0)*Circle(J2.ROUND_D/2),Plane.XY.offset(Z0+(J2.ROUND_D-square)/2)*Rectangle(square,square)])
    h=square/2
    grip=J.M.box(-h,h,-h,h,Z0,ROOF)
    roof=frustum(square,0,ROOF,ROOF+square/2)
    return mouth+funnel+grip+roof

def cap(square,dish_depth=0,notches=0):
    j6,j5=J6.cap(square,dish_depth,notches)
    solid=j6+J6.cavity(square)  # fill J6's socket, cut the printable one
    return solid-cavity(square),j6

def overhangs(c):
    # Downward faces steeper than 45 deg inside the socket (excluding the bed face).
    box=J.M.box(-J2.ROUND_D,J2.ROUND_D,-J2.ROUND_D,J2.ROUND_D,J.BOTTOM+.01,ROOF+J2.ROUND_D)
    bad=[]
    for f in (c & box).faces():
        n=f.normal_at()
        if n.Z<-math.cos(math.radians(45))-1e-3 and abs(f.center().Z-(J.BOTTOM+.01))>1e-3 and f.area>1e-4:
            bad.append(round(f.center().Z,3))
    return bad

def main():
    STL.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    def vol(s):return sum(x.volume for x in s.solids())
    sock=J.cylinder(J.NECK,J.BOTTOM,J.BOTTOM+J2.ROUND_DEPTH+J2.SQUARE_DEPTH+3)
    outside=J.M.box(-J.FLANGE,J.FLANGE,-J.FLANGE,J.FLANGE,J.BOTTOM-J.P.TOOL_EXT,J4.FLAT_Z+1)-sock
    checks={};parts={};report_overhangs={}
    for name,v in J6.VARIANTS.items():
        c,j6=cap(v['square'],v['dish'],v['notches'])
        bad=overhangs(c);report_overhangs[name]=bad
        stem=J.M.box(-J.P.J4/2,J.P.J4/2,-J.P.J4/2,J.P.J4/2,Z0,ROOF)
        lip=J.cylinder(2.94,  # J4b base lip width, cal 2026-09-24
            J.BOTTOM-J.P.TOOL_EXT,Z0)
        checks[name+'_valid_single_solid']=c.is_valid and len(c.solids())==1
        checks[name+'_no_flat_overhang_in_socket']=not bad
        checks[name+'_stem_square_fits']=J.overlap(stem,c)<1e-6 and v['square']>J.P.J4
        checks[name+'_grip_walls_kept']=vol(J.M.box(-v['square']/2-.05,v['square']/2+.05,-v['square']/2-.05,v['square']/2+.05,Z0+(J2.ROUND_D-v['square'])/2,ROOF) & c)>0
        checks[name+'_base_lip_clears']=J.overlap(lip,c)<1e-6
        checks[name+'_outside_same_as_J6']=vol((c & outside)-(j6 & outside))<1e-5 and vol((j6 & outside)-(c & outside))<1e-5
        checks[name+'_roof_left_under_top']=J4.FLAT_Z-v['dish']-(ROOF+v['square']/2)>.8
        parts[name]=Pos(0,0,-J.BOTTOM)*c
        J.export(parts[name],STL/('joystick-j7-'+name+'.stl'))
    placed=[Pos(i*(J.FLANGE+J6.GAP),0,0)*p for i,p in enumerate(parts.values())]
    checks['plate_separate']=all(J.overlap(a,b)<1e-6 for a,b in itertools.combinations(placed,2))
    J.export(Compound(children=placed),STL/'joystick-j7-abc-plate.stl')
    report=dict(checks=checks,passed=all(checks.values()),socket=dict(round_d=J2.ROUND_D,round_depth=J6.ROUND_DEPTH,funnel='45 deg',grip_depth=J2.SQUARE_DEPTH,roof='45 deg pyramid'),
        variants=J6.VARIANTS,overhangs=report_overhangs,notes=['A/B/C = 1/2/3 flange notches, as J6.','Socket prints flange-down with no flat overhang.','Press/tilt test pending.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    files=sorted(STL.glob('*.stl'))
    (OUT/'manifest.json').write_text(json.dumps(dict(revision='J7',source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),*(ROOT/'cad'/n for n in ('joystick_j6.py','joystick_j5.py','joystick_j4.py','joystick_j2.py','joystick_test.py'))]},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}),indent=2)+'\n')
    print(json.dumps(report,indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
