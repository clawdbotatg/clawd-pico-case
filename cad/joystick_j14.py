"""J14: J13-O (Austin's best, 2026-09-30) in three stick fits, marked with dots.
O = 8.6 round flange, lift 0.6, flange thinned under the lid. Austin: "one
step tighter on the joystick and one step looser ... call them one, two and
three". A step is 0.05 on the square grip, as J6/J7 (1.95 -> 1.90):
  1  1.85 (tighter: 0.01 smaller than the 1.86 stem)
  2  1.90 (= O)
  3  1.95 (looser)
1-3 bold dots engraved on top instead of letters (J13's letters printed messy).
Rows J14-* in MEASUREMENTS. Run: .venv/bin/python cad/joystick_j14.py
"""
import hashlib
import itertools
import json
from pathlib import Path
from build123d import Pos, Compound
import joystick_test as J
import joystick_j2 as J2
import joystick_j4 as J4
import joystick_j7 as J7
import joystick_j8 as J8
import joystick_j13 as J13

ROOT=J.ROOT
STL=ROOT/'stl/v1.4/joystick-j14'
OUT=ROOT/'renders/v1.4/joystick-j14'
LIFT,THIN,DISC=J13.VARIANTS['O']  # J14-KEEP: J13-O
VARIANTS={'1':1.85,'2':J8.SQUARE,'3':1.95}  # J14-FIT: square grip across the flats
DOT_D,DOT_PITCH,DOT_DEPTH=1.0,1.5,.5  # J14-MARK
GAP=4.0

def dots(n):
    xs=[(i-(n-1)/2)*DOT_PITCH for i in range(n)]
    return [Pos(x,0,0)*J.cylinder(DOT_D,J4.FLAT_Z-DOT_DEPTH,J4.FLAT_Z+J.P.TOOL_EXT) for x in xs]

def cap(square,n):
    c=J8.cap(flange=DISC,lift=LIFT,rim=1.2,notches=0)  # O without its letter
    if square!=J8.SQUARE:  # refill O's socket inside the neck, cut this one
        c=c+(J8.cavity(J8.SQUARE,LIFT) & J.cylinder(J.NECK,J.BOTTOM,J4.FLAT_Z))-J8.cavity(square,LIFT)
    if THIN:c-=J13.thin_cut()
    for d in dots(n):c-=d
    return c

def main():
    STL.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    def vol(s):return sum(x.volume for x in s.solids())
    def diff(a,b):return vol(a-b) if a.solids() else 0.  # a-b, tolerating an empty a
    checks={};parts={}
    o=J13.cap(LIFT,THIN,DISC,'O')
    band=J.M.box(-6,6,-6,6,J.BOTTOM-1,J4.FLAT_Z-1)  # below the marks
    z0=J.BOTTOM+J2.ROUND_DEPTH-LIFT
    for name,square in VARIANTS.items():
        n=int(name);c=cap(square,n)
        checks[name+'_valid_single_solid']=c.is_valid and len(c.solids())==1
        checks[name+'_no_flat_overhang_in_socket']=not J7.overhangs(c)
        checks[name+'_base_lip_clears']=J.overlap(J.cylinder(2.94,J.BOTTOM-J.P.TOOL_EXT,z0),c)<1e-6  # J4b
        grip=vol(c & J.M.box(-J.P.J4/2,J.P.J4/2,-J.P.J4/2,J.P.J4/2,z0,z0+J2.SQUARE_DEPTH))
        checks[name+('_stem_interferes' if square<J.P.J4 else '_stem_fits')]=(grip>0) if square<J.P.J4 else grip<1e-6
        cavity_ok=diff(J8.cavity(square,LIFT)&band,band-c)<1e-4
        checks[name+'_socket_is_this_fit']=cavity_ok
        if square==J8.SQUARE:checks[name+'_same_as_O_below_marks']=diff(c&band,o&band)<1e-4 and diff(o&band,c&band)<1e-4
        else:
            core=J.cylinder(3.2,J.BOTTOM-2,J4.FLAT_Z)  # the socket, which differs on purpose
            checks[name+'_outside_same_as_O']=diff((c&band)-core,o&band)<1e-4 and diff((o&band)-core,c&band)<1e-4
        checks[name+'_dots_inside_flat_top']=(n-1)/2*DOT_PITCH+DOT_D/2<2.5
        parts[name]=Pos(0,0,-J.BOTTOM)*c
        J.export(parts[name],STL/('joystick-j14-'+name+'.stl'))
    placed=[Pos(i*(DISC+GAP),0,0)*p for i,p in enumerate(parts.values())]
    checks['plate_separate']=all(J.overlap(a,x)<1e-6 for a,x in itertools.combinations(placed,2))
    J.export(Compound(children=placed),STL/'joystick-j14-plate.stl')
    report=dict(checks=checks,passed=all(checks.values()),base='J13-O',lift=LIFT,disc=DISC,fits=VARIANTS,
        notes=['1 = 1.85 (tighter), 2 = 1.90 (= O), 3 = 1.95 (looser); dots on top.','Lid clearance identical to O (outside unchanged).'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    files=sorted(STL.glob('*.stl'))
    src=[Path(__file__),*(ROOT/'cad'/n for n in ('joystick_j13.py','joystick_j11.py','joystick_j8.py','joystick_j7.py','joystick_test.py'))]
    (OUT/'manifest.json').write_text(json.dumps(dict(revision='J14',source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in src},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}),indent=2)+'\n')
    print(json.dumps(dict(checks=checks,passed=report['passed']),indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
