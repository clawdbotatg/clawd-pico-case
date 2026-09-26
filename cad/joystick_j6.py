"""J6 test set (v1.4 joystick): J5 (lift 0.3) with a tighter square socket so
the cap cannot rock on the stem, and optionally a thumb dish that centres the
push. Austin: with the cap on, pressing in gives centre + a direction.
Variants carry 1/2/3 small notches on the flange rim to tell them apart.
Rows J6-* in MEASUREMENTS. Run: .venv/bin/python cad/joystick_j6.py
"""
import hashlib
import itertools
import json
import math
from pathlib import Path
from build123d import Pos, Rot, Sphere, Compound
import joystick_test as J
import joystick_j2 as J2
import joystick_j4 as J4
import joystick_j5 as J5

ROOT=J.ROOT
STL=ROOT/'stl/v1.4/joystick-j6'
OUT=ROOT/'renders/v1.4/joystick-j6'
LIFT=.3  # J6-KEEP: J5 lift that stays clear of the lid to ~9 deg tilt
ROUND_DEPTH=J2.ROUND_DEPTH-LIFT
VARIANTS={'a':dict(square=1.95,dish=0,notches=1),  # J6-A
          'b':dict(square=1.90,dish=0,notches=2),  # J6-B
          'c':dict(square=1.95,dish=.4,notches=3)}  # J6-C
DISH_D=5.0  # J6-DISH: chord of the thumb dish on the flat top
NOTCH_W,NOTCH_D=.6,.5  # J6-NOTCH: rim marks; 10.4 flange keeps >= 9.4 > 8 mm hole
GAP=4.0  # plate spacing

def cavity(square):
    circle=J.cylinder(J2.ROUND_D,J.BOTTOM-J.P.TOOL_EXT,J.BOTTOM+ROUND_DEPTH)
    h=square/2
    return circle+J.M.box(-h,h,-h,h,J.BOTTOM+ROUND_DEPTH-J.P.EPS,J.BOTTOM+ROUND_DEPTH+J2.SQUARE_DEPTH)

def dish(depth):
    r=(DISH_D**2/4+depth**2)/(2*depth)
    return Pos(0,0,J4.FLAT_Z-depth+r)*Sphere(r)

def notch(i,n):
    a=90+360*i/n if n>1 else 90
    return Rot(0,0,a)*J.M.box(J.FLANGE/2-NOTCH_D,J.FLANGE/2+1,-NOTCH_W/2,NOTCH_W/2,J.BOTTOM-J.P.TOOL_EXT,J.BOTTOM+J.FLANGE_T+J.P.TOOL_EXT)

def cap(square,dish_depth=0,notches=0):
    j5,_=J5.cap(LIFT)
    solid=j5+J5.cavity(LIFT)  # fill J5's socket, then cut the tighter one
    c=solid-cavity(square)
    if dish_depth:c-=dish(dish_depth)
    for i in range(notches):c-=notch(i,notches)
    return c,j5

def main():
    STL.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    def vol(s):return sum(x.volume for x in s.solids())
    sock=J.cylinder(J.NECK,J.BOTTOM,J.BOTTOM+J2.ROUND_DEPTH+J2.SQUARE_DEPTH+.5)
    ball=J.M.box(-J.FLANGE,J.FLANGE,-J.FLANGE,J.FLANGE,J.BOTTOM+J.FLANGE_T+J.P.TOOL_EXT,J4.FLAT_Z-.5)-sock
    checks={};parts={}
    for name,v in VARIANTS.items():
        c,j5=cap(v['square'],v['dish'],v['notches'])
        expected=math.pi*(J2.ROUND_D/2)**2*ROUND_DEPTH+v['square']**2*J2.SQUARE_DEPTH
        checks[name+'_valid_single_solid']=c.is_valid and len(c.solids())==1
        checks[name+'_socket_volume_exact']=abs(vol(sock-c)-expected)<1e-4
        checks[name+'_square_grips_stem']=v['square']>J.P.J4  # stem 1.86 across flats (J4 row)
        checks[name+'_ball_and_neck_same_as_J5']=vol((c & ball)-(j5 & ball))<1e-5 and vol((j5 & ball)-(c & ball))<1e-5
        checks[name+'_flange_still_retains']=J.FLANGE-2*NOTCH_D>J.HOLE
        if v['dish']:
            flat,_=cap(v['square'],0,v['notches'])
            probe=J.M.box(-.2,.2,-.2,.2,J4.FLAT_Z-v['dish']+.01,J4.FLAT_Z)
            checks[name+'_dish_centre_open']=vol(flat-c)>.3 and vol(c & probe)<1e-6 and abs(c.bounding_box().max.Z-J4.FLAT_Z)<1e-6
        parts[name]=Pos(0,0,-J.BOTTOM)*c
        J.export(parts[name],STL/('joystick-j6-'+name+'.stl'))
    placed=[Pos(i*(J.FLANGE+GAP),0,0)*p for i,p in enumerate(parts.values())]
    checks['plate_separate']=all(J.overlap(a,b)<1e-6 for a,b in itertools.combinations(placed,2))
    plate=Compound(children=placed);J.export(plate,STL/'joystick-j6-abc-plate.stl')
    report=dict(checks=checks,passed=all(checks.values()),lift=LIFT,variants=VARIANTS,stem_across_flats=J.P.J4,
        notes=['A/B/C = 1/2/3 notches on the flange rim.','Square clearance on the 1.86 stem: A/C 0.09, B 0.04 total (J2 was 0.15).','PETG small holes print undersize; B may be a press fit.','Physical press/tilt test pending.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    files=sorted(STL.glob('*.stl'))
    (OUT/'manifest.json').write_text(json.dumps(dict(revision='J6',source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),*(ROOT/'cad'/n for n in ('joystick_j5.py','joystick_j4.py','joystick_j2.py','joystick_test.py'))]},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}),indent=2)+'\n')
    print(json.dumps(report,indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
