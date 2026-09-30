"""J12: J11-III (7.2 square flange, in line) riding higher on the stick.
Austin, 2026-09-30: with J11-III, up/down/left/right no longer click the
centre, but the centre press is hard to get without a direction: the cap sits
too low, so make the hole for the stick less deep. Same knob as J5-LIFT: a
shorter round mouth puts the socket lower in the cap, so the cap rides higher.
Numbered V-VIII on top, continuing from J11's I-IV:
  V lift 0.4 (+0.1 over III), VI 0.5 (+0.2), VII 0.6 (+0.3), VIII 0.7 (+0.4)
Rows J12-* in MEASUREMENTS. Run: .venv/bin/python cad/joystick_j12.py
"""
import hashlib
import itertools
import json
from pathlib import Path
from build123d import Pos, Compound
import joystick_test as J
import joystick_j2 as J2
import joystick_j7 as J7
import joystick_j8 as J8
import joystick_j10 as J10
import joystick_j11 as J11
import j10_tilt as TILT

ROOT=J.ROOT
STL=ROOT/'stl/v1.4/joystick-j12'
OUT=ROOT/'renders/v1.4/joystick-j12'
FLATS,TURN=J11.VARIANTS['III']  # J12-KEEP: J11-III flange
VARIANTS={'V':.4,'VI':.5,'VII':.6,'VIII':.7}  # J12-LIFT: round mouth 1.0 - lift deep
MARK=dict(sw=.5,height=2.2,gap=.4,vw=1.4,apex=.8)  # J12-MARK: smaller, so VIII fits the 5 mm flat

def cap(lift,numeral):
    return J11.cap(FLATS,TURN,numeral,lift=lift,mark=MARK)

def main():
    STL.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    def vol(s):return sum(x.volume for x in s.solids())
    checks={};parts={};caps={}
    iii=J11.cap(FLATS,TURN,'III')
    for name,lift in VARIANTS.items():
        c=cap(lift,name)
        z0=J.BOTTOM+J2.ROUND_DEPTH-lift
        checks[name+'_valid_single_solid']=c.is_valid and len(c.solids())==1
        checks[name+'_no_flat_overhang_in_socket']=not J7.overhangs(c)
        checks[name+'_stem_fits']=J.overlap(J.M.box(-J.P.J4/2,J.P.J4/2,-J.P.J4/2,J.P.J4/2,z0,z0+J2.SQUARE_DEPTH),c)<1e-6
        checks[name+'_base_lip_clears']=J.overlap(J.cylinder(2.94,J.BOTTOM-J.P.TOOL_EXT,z0),c)<1e-6  # J4b
        checks[name+'_socket_is_III_moved_down']=abs(vol(J8.cavity(J8.SQUARE,lift))-vol(J8.cavity(J8.SQUARE,.3))+(lift-.3)*3.14159*1.5**2)<.02
        pts=[p for poly in J10.strokes(name,**MARK) for p in poly]
        checks[name+'_mark_inside_flat_top']=max((x*x+y*y)**.5 for x,y in pts)<2.5  # J4 7.4 ball - 1.2 top edge
        outside=J.M.box(-6,6,-6,6,J.BOTTOM-1,J.BOTTOM+J.FLANGE_T)-J.cylinder(J.NECK,J.BOTTOM-2,J.BOTTOM+1)  # flange only, not the socket mouth
        checks[name+'_flange_same_as_III']=vol((c&outside)-(iii&outside))<1e-4 and vol((iii&outside)-(c&outside))<1e-4
        parts[name]=Pos(0,0,-J.BOTTOM)*c;caps['J12-'+name]=(c,lift)
        J.export(parts[name],STL/('joystick-j12-'+name+'.stl'))
    step=FLATS+J11.GAP
    placed=[Pos(i*step,0,0)*p for i,p in enumerate(parts.values())]
    checks['plate_separate']=all(J.overlap(a,x)<1e-6 for a,x in itertools.combinations(placed,2))
    J.export(Compound(children=placed),STL/'joystick-j12-plate.stl')
    tilt=TILT.tilt({'J11-III':(iii,.3),**caps})
    for n in caps:checks[n+'_clear_of_lid_at_rest']=not tilt['caps'][n]['touches_at_rest']
    report=dict(checks=checks,passed=all(checks.values()),flats=FLATS,turn=TURN,lifts=VARIANTS,tilt=tilt,
        notes=['V-VIII ride 0.1/0.2/0.3/0.4 higher than J11-III.','Riding higher also brings the flange closer to the lid; the tilt table compares that.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    files=sorted(STL.glob('*.stl'))
    src=[Path(__file__),*(ROOT/'cad'/n for n in ('joystick_j11.py','j10_tilt.py','joystick_j10.py','joystick_j8.py','joystick_j7.py','joystick_test.py'))]
    (OUT/'manifest.json').write_text(json.dumps(dict(revision='J12',source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in src},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}),indent=2)+'\n')
    print(json.dumps(dict(checks=checks,passed=report['passed']),indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
