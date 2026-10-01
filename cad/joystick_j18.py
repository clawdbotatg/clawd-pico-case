"""J18: J17-B's tabs on six hole depths, 2.2 down to 1.7, dice dots 1-6.
Austin, 2026-09-30: pressing a J16/J17 cap clicks all five switches; the bare
stick clicks only the centre. The square-only hole lets the cap's bottom land
on the wider collar at the stick's base (2.94, J4b) and press it flat. Austin
estimates the stick tip to collar top at about 2 mm, so the hole (cap bottom
to the square's flat roof, where the stick tip sits) is set to 2.2 / 2.1 /
2.0 / 1.9 / 1.8 / 1.7. J16/J17-A is 2.4.
Rows J18-* in MEASUREMENTS. Run: .venv/bin/python cad/joystick_j18.py
"""
import hashlib
import itertools
import json
from pathlib import Path
from build123d import Pos, Compound
import joystick_test as J
import joystick_j2 as J2
import joystick_j7 as J7
import joystick_j14 as J14
import joystick_j16 as J16
import joystick_j17 as J17
import j10_tilt as TILT

ROOT=J.ROOT
STL=ROOT/'stl/v1.4/joystick-j18'
OUT=ROOT/'renders/v1.4/joystick-j18'
J16_DEPTH=J2.ROUND_DEPTH-J16.LIFT+J2.SQUARE_DEPTH  # 2.4: cap bottom to the square's roof
TAB_SCALE=J17.VARIANTS['B'][1]  # J18-TAB: 1.55x, J17-B ("the two dot")
DEPTHS=[2.2,2.1,2.0,1.9,1.8,1.7]  # J18-DEPTH, dots 1..6

def cap(depth,n):
    return J17.cap(J16_DEPTH-depth,TAB_SCALE,n)

def main(depths=DEPTHS,stl=STL,out=OUT,rev='J18'):  # J19 reuses this with shallower depths
    stl.mkdir(parents=True,exist_ok=True);out.mkdir(parents=True,exist_ok=True)
    def vol(s):return sum(x.volume for x in s.solids())
    checks={};parts={};caps={};h=J16.SQUARE/2
    for i,depth in enumerate(depths):
        n=i+1;name=str(n);c=cap(depth,n);roof=J.BOTTOM+depth
        checks[name+'_valid_single_solid']=c.is_valid and len(c.solids())==1
        checks[name+'_no_flat_overhang_in_socket']=not J7.overhangs(c)
        checks[name+'_depth_is_'+str(depth)]=vol(c & J.M.box(-h,h,-h,h,J.BOTTOM,roof-.01))<1e-6 and vol(c & J.M.box(-.05,.05,-.05,.05,roof+h+.05,roof+h+.15))>0
        checks[name+'_pips_inside_flat_top']=J17.PIP_STEP*2**.5+J17.PIP_D/2<2.5
        parts[name]=Pos(0,0,-J.BOTTOM)*c;caps[rev+'-'+name]=(c,J16.LIFT+J16_DEPTH-depth)
        J.export(parts[name],stl/('joystick-'+rev.lower()+'-'+name+'.stl'))
    step=2*J17.tab(TAB_SCALE)[1]+J14.GAP
    placed=[Pos((i%3)*step,(i//3)*step,0)*p for i,p in enumerate(parts.values())]  # 3 x 2
    checks['plate_separate']=all(J.overlap(a,x)<1e-6 for a,x in itertools.combinations(placed,2))
    J.export(Compound(children=placed),stl/('joystick-'+rev.lower()+'-plate.stl'))
    tilt=TILT.tilt({'J17-B':(J17.cap(*J17.VARIANTS['B'],2),J16.LIFT+J17.VARIANTS['B'][0]),**caps})
    warnings=[n+' touches the lid at rest in the model (if the stick tip seats on the roof)' for n in caps if tilt['caps'][n]['touches_at_rest']]  # reported, not fatal: Austin picks depths by hand
    report=dict(checks=checks,passed=all(checks.values()),warnings=warnings,depths={str(i+1):d for i,d in enumerate(depths)},tab_scale=TAB_SCALE,tilt=tilt,
        notes=['Depth = cap bottom to the flat roof the stick tip sits on (J16 2.4).','If the roof is what stops the cap, shallower also rides higher: see tilt.'])
    (out/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    files=sorted(stl.glob('*.stl'))
    src=[Path(__file__),*(ROOT/'cad'/n for n in ('joystick_j17.py','joystick_j16.py','joystick_j15.py','joystick_test.py'))]
    (out/'manifest.json').write_text(json.dumps(dict(revision=rev,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in src},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}),indent=2)+'\n')
    print(json.dumps(dict(checks=checks,passed=report['passed'],warnings=warnings),indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
