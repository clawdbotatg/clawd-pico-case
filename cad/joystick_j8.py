"""J8 test set: three variations on J7-B (Austin's best fit, 1.90 socket).
With B, a direction push sometimes also clicks the centre. Each variant
tests one fix: 1 = smaller flange (less dip when tilted), 2 = smaller flange
and riding 0.5 higher (more room under), 3 = rounder top edge (thumb rolls
sideways instead of pressing down). 1/2/3 flange notches mark them.
Rows J8-* in MEASUREMENTS. Run: .venv/bin/python cad/joystick_j8.py
"""
import hashlib
import itertools
import json
import math
from pathlib import Path
from build123d import Pos, Sphere, Compound, Plane, Rectangle, Circle, loft, fillet
import joystick_test as J
import joystick_j2 as J2
import joystick_j4 as J4
import joystick_j6 as J6
import joystick_j7 as J7

ROOT=J.ROOT
STL=ROOT/'stl/v1.4/joystick-j8'
OUT=ROOT/'renders/v1.4/joystick-j8'
SQUARE=1.90  # J8-KEEP: J7-B socket
VARIANTS={'1':dict(flange=9.2,lift=.3,rim=J4.RIM_R,notches=1),  # J8-1
          '2':dict(flange=9.2,lift=.5,rim=J4.RIM_R,notches=2),  # J8-2
          '3':dict(flange=J.FLANGE,lift=.3,rim=1.2,notches=3)}  # J8-3
BASELINE=dict(flange=J.FLANGE,lift=.3,rim=J4.RIM_R,notches=0)  # = J7-B, for comparison

def cavity(square,lift):
    # J7's self-supporting socket, with the round mouth set by lift.
    z0=J.BOTTOM+J2.ROUND_DEPTH-lift;roof=z0+J2.SQUARE_DEPTH
    mouth=J.cylinder(J2.ROUND_D,J.BOTTOM-J.P.TOOL_EXT,z0)
    funnel=loft([Plane.XY.offset(z0)*Circle(J2.ROUND_D/2),Plane.XY.offset(z0+(J2.ROUND_D-square)/2)*Rectangle(square,square)])
    h=square/2
    return mouth+funnel+J.M.box(-h,h,-h,h,z0,roof)+J7.frustum(square,0,roof,roof+square/2)

def cap(flange,lift,rim,notches):
    _,blank=J2.cap()  # J2 outside with no socket
    c=(blank+Pos(0,0,J.BALL_Z)*Sphere(J4.BALL_D/2))-J.M.box(-J4.BALL_D,J4.BALL_D,-J4.BALL_D,J4.BALL_D,J4.FLAT_Z,J.BALL_Z+J4.BALL_D)
    edge=[e for e in c.edges() if abs(e.bounding_box().min.Z-J4.FLAT_Z)<1e-6 and abs(e.bounding_box().max.Z-J4.FLAT_Z)<1e-6]
    c=fillet(edge,rim)
    if flange<J.FLANGE:
        c-=J.cylinder(J.FLANGE+2,J.BOTTOM-J.P.TOOL_EXT,J.BOTTOM+J.FLANGE_T+J.P.EPS)-J.cylinder(flange,J.BOTTOM-2*J.P.TOOL_EXT,J.BOTTOM+J.FLANGE_T+2*J.P.EPS)
    for i in range(notches):
        a=90+360*i/notches if notches>1 else 90
        from build123d import Rot
        c-=Rot(0,0,a)*J.M.box(flange/2-J6.NOTCH_D,flange/2+1,-J6.NOTCH_W/2,J6.NOTCH_W/2,J.BOTTOM-J.P.TOOL_EXT,J.BOTTOM+J.FLANGE_T+J.P.TOOL_EXT)
    return c-cavity(SQUARE,lift)

def main():
    STL.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    def vol(s):return sum(x.volume for x in s.solids())
    checks={};parts={}
    b=cap(**BASELINE);b7,_=J7.cap(SQUARE)
    band=J.M.box(-5,5,-5,5,J.BOTTOM+J.FLANGE_T+.05,J4.FLAT_Z-1)  # neck, ball: J7-B's own
    checks['baseline_matches_J7B_above_flange']=vol((b & band)-(b7 & band))<1e-4 and vol((b7 & band)-(b & band))<1e-4
    for name,v in VARIANTS.items():
        c=cap(**v)
        checks[name+'_valid_single_solid']=c.is_valid and len(c.solids())==1
        checks[name+'_no_flat_overhang_in_socket']=not J7.overhangs(c)
        checks[name+'_stem_fits']=J.overlap(J.M.box(-J.P.J4/2,J.P.J4/2,-J.P.J4/2,J.P.J4/2,J.BOTTOM+J2.ROUND_DEPTH-v['lift'],J.BOTTOM+J2.ROUND_DEPTH-v['lift']+J2.SQUARE_DEPTH),c)<1e-6
        checks[name+'_base_lip_clears']=J.overlap(J.cylinder(2.94,J.BOTTOM-J.P.TOOL_EXT,J.BOTTOM+J2.ROUND_DEPTH-v['lift']),c)<1e-6  # J4b
        checks[name+'_flange_retains_at_notch']=v['flange']-2*J6.NOTCH_D>J.HOLE
        parts[name]=Pos(0,0,-J.BOTTOM)*c
        J.export(parts[name],STL/('joystick-j8-'+name+'.stl'))
    placed=[Pos(i*(J.FLANGE+J6.GAP),0,0)*p for i,p in enumerate(parts.values())]
    checks['plate_separate']=all(J.overlap(a,x)<1e-6 for a,x in itertools.combinations(placed,2))
    J.export(Compound(children=placed),STL/'joystick-j8-123-plate.stl')
    # Tilt dip: how far the flange rim drops below the cap's resting underside
    # at 10 deg, minus the lift gap (positive = rim can reach the body).
    dip={name:round(v['flange']/2*math.sin(math.radians(10))-v['lift'],2) for name,v in {**VARIANTS,'J7-B':BASELINE}.items()}
    report=dict(checks=checks,passed=all(checks.values()),square=SQUARE,variants=VARIANTS,rim_dip_past_lift_at_10deg=dip,
        notes=['1/2/3 flange notches = J8-1/2/3.','Dip is geometry only; the body top height (J3) is not measured.','Press/tilt test pending.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    files=sorted(STL.glob('*.stl'))
    (OUT/'manifest.json').write_text(json.dumps(dict(revision='J8',source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),*(ROOT/'cad'/n for n in ('joystick_j7.py','joystick_j6.py','joystick_j4.py','joystick_j2.py','joystick_test.py'))]},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}),indent=2)+'\n')
    print(json.dumps(report,indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
