"""J17: five J16 variants, A-E: shallower hole and bigger diagonal tabs, together.
Austin, 2026-09-30, after printing J16: "the hole needs to be shallower" and
"the tabs need to be about two to three times bigger". In the model 2-3x
tabs with a shallower hole all fall below VII's lid room (double click), so
Austin set the range: A = J16 (no double click) with bigger tabs, E = where
the model is sure it double-clicks, B-D a gradient between.
  shallower: the square's roof comes down 0.05 per step, so the cap rides higher
  tabs: J16's tab (1.2 wide, 0.5 past the 8.6 disc) scaled 1.3 -> 2.3 in width
  and in reach past the disc; 0.24 thick past the hole edge, as J16
  model lid room (pivot 3, push): J16 17.6, A 16.6, B 15.1, C 13.7, D 12.5,
  E 11.4 (VI 17.6 tested clean, VII 15.8 double-clicked)
Marked with dice dots on top (A 1 ... E 5).
Rows J17-* in MEASUREMENTS. Run: .venv/bin/python cad/joystick_j17.py
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
import joystick_j14 as J14
import joystick_j15 as J15
import joystick_j16 as J16
import j10_tilt as TILT

ROOT=J.ROOT
STL=ROOT/'stl/v1.4/joystick-j17'
OUT=ROOT/'renders/v1.4/joystick-j17'
DISC_R=4.3  # J13-O / J15 disc
BASE_W,BASE_PAST=J16.FLARE_W,J16.FLARE_TIP-DISC_R  # J16 tab: 1.2 wide, 0.5 past the disc
VARIANTS={'A':(0.,1.3),'B':(.05,1.55),'C':(.1,1.8),'D':(.15,2.05),'E':(.2,2.3)}  # J17-STEP: hole shallower by, tab scale
PIP_D,PIP_STEP=.9,1.2  # J17-MARK: dice dots, 0.5 deep (J14 dot depth)

def pips(n):
    s=PIP_STEP
    pos={1:[(0,0)],2:[(-s,-s),(s,s)],3:[(-s,-s),(0,0),(s,s)],4:[(-s,-s),(s,s),(-s,s),(s,-s)],5:[(-s,-s),(s,s),(-s,s),(s,-s),(0,0)]}[n]
    return [Pos(x,y,0)*J.cylinder(PIP_D,J4.FLAT_Z-J14.DOT_DEPTH,J4.FLAT_Z+J.P.TOOL_EXT) for x,y in pos]

def cavity(up):
    """J16's square-only socket with its roof `up` lower (a shallower hole)."""
    z0=J.BOTTOM+J2.ROUND_DEPTH-J16.LIFT;roof=z0+J2.SQUARE_DEPTH-up;h=J16.SQUARE/2;ch=J16.MOUTH_CH
    return (J.M.box(-h,h,-h,h,J.BOTTOM-J.P.TOOL_EXT,roof)+J7.frustum(J16.SQUARE,0,roof,roof+J16.SQUARE/2)
            +J7.frustum(J16.SQUARE+2*ch,J16.SQUARE,J.BOTTOM,J.BOTTOM+ch)
            +J.M.box(-h-ch,h+ch,-h-ch,h+ch,J.BOTTOM-J.P.TOOL_EXT,J.BOTTOM+J.P.EPS))

def tab(scale):
    return BASE_W*scale,DISC_R+BASE_PAST*scale  # width, tip radius

def cap(up,scale,n):
    w,tip=tab(scale)
    c=J15.cap()+(J8.cavity(J16.SQUARE,J16.LIFT) & J.cylinder(J.NECK,J.BOTTOM,J4.FLAT_Z))  # J15 with its socket filled
    fl=None
    for f in J16.flares(w,tip):fl=f if fl is None else fl+f
    c=c+(fl-J16.thin(J16.FLARE_T))-cavity(up)
    for p in pips(n):c-=p
    return c

def main():
    STL.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    def vol(s):return sum(x.volume for x in s.solids())
    checks={};parts={};caps={}
    j16=J16.cap()
    for i,(name,(up,scale)) in enumerate(VARIANTS.items()):
        c=cap(up,scale,i+1);w,tip=tab(scale)
        z0=J.BOTTOM+J2.ROUND_DEPTH-J16.LIFT;roof=z0+J2.SQUARE_DEPTH-up;h=J16.SQUARE/2
        checks[name+'_valid_single_solid']=c.is_valid and len(c.solids())==1
        checks[name+'_no_flat_overhang_in_socket']=not J7.overhangs(c)
        checks[name+'_socket_square_to_roof']=vol(c & J.M.box(-h,h,-h,h,J.BOTTOM,roof))<1e-6
        checks[name+'_roof_lower_by_step']=vol(c & J.M.box(-.05,.05,-.05,.05,roof+h+.05,roof+h+.15))>0 and vol(c & J.M.box(-h,h,-h,h,roof-.02,roof-.01))<1e-6  # solid just above the pyramid apex, void under the roof
        checks[name+'_lip_stop_kept']=J16.SQUARE+2*J16.MOUTH_CH<2.94
        checks[name+'_pips_inside_flat_top']=PIP_STEP*2**.5+PIP_D/2<2.5
        checks[name+'_hole_not_deeper_than_J16']=up>=0
        checks[name+'_tabs_bigger_than_J16']=w>J16.FLARE_W and tip>J16.FLARE_TIP
        parts[name]=Pos(0,0,-J.BOTTOM)*c;caps['J17-'+name]=(c,J16.LIFT+up)
        J.export(parts[name],STL/('joystick-j17-'+name+'.stl'))
    step=2*tab(max(s for _,s in VARIANTS.values()))[1]+J14.GAP
    placed=[Pos(i*step,0,0)*p for i,p in enumerate(parts.values())]
    checks['plate_separate']=all(J.overlap(a,x)<1e-6 for a,x in itertools.combinations(placed,2))
    J.export(Compound(children=placed),STL/'joystick-j17-plate.stl')
    tilt=TILT.tilt({'J16':(j16,J16.LIFT),**caps})
    for n in caps:checks[n+'_clear_of_lid_at_rest']=not tilt['caps'][n]['touches_at_rest']
    report=dict(checks=checks,passed=all(checks.values()),variants={k:dict(shallower=u,tab_scale=s,tab_width=round(tab(s)[0],2),tab_tip_r=round(tab(s)[1],2)) for k,(u,s) in VARIANTS.items()},tilt=tilt,
        notes=['Dice dots: A 1 ... E 5.','Shallower and bigger both bring the flange/tabs toward the lid: see tilt.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    files=sorted(STL.glob('*.stl'))
    src=[Path(__file__),*(ROOT/'cad'/n for n in ('joystick_j16.py','joystick_j15.py','joystick_j14.py','joystick_j13.py','joystick_j8.py','joystick_j7.py','joystick_test.py'))]
    (OUT/'manifest.json').write_text(json.dumps(dict(revision='J17',source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in src},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}),indent=2)+'\n')
    print(json.dumps(dict(checks=checks,passed=report['passed']),indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
