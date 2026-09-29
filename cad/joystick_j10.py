"""J10 test set: stop the flange lifting into the lid when the stick tips.
Austin, 2026-09-29: pushing a direction clicks once (the direction), then a
little farther clicks the centre too. The flange edge behind the push rises
into the lid underside, pivots there, and drives the stem down. Every variant
keeps J9's socket, 7.4 half ball and 1.2 round top edge; only the retention
under the lid changes. A Roman numeral engraved on top tells them apart.
  I   four tabs on the diagonals (45 deg to the socket flats)
  II  four tabs in line with the socket flats (= diagonals if the stem is
      turned 45 deg on the board; its orientation is not measured)
  III J9's full disc, riding 0.2 lower on the stem
  IV  I's tabs, riding 0.2 lower
Rows J10-* in MEASUREMENTS. Run: .venv/bin/python cad/joystick_j10.py
"""
import hashlib
import itertools
import json
import math
from pathlib import Path
from build123d import Pos, Rot, Axis, Compound, Polygon, extrude, Plane
import joystick_test as J
import joystick_j2 as J2
import joystick_j4 as J4
import joystick_j6 as J6
import joystick_j7 as J7
import joystick_j8 as J8
import joystick_j9 as J9

ROOT=J.ROOT
STL=ROOT/'stl/v1.4/joystick-j10'
OUT=ROOT/'renders/v1.4/joystick-j10'
TAB_W=1.6    # J10-TAB: tab width
TAB_TIP=4.6  # J10-TAB: tip 0.6 past the 8 mm lid hole edge, as J8-1's 9.2 flange
LOWER=.2     # J10-LOWER: lift 0.3 -> 0.1
VARIANTS={'I':dict(tabs=45,lift=.3),
          'II':dict(tabs=0,lift=.3),
          'III':dict(tabs=None,lift=.3-LOWER),
          'IV':dict(tabs=45,lift=.3-LOWER)}
MARK_W,MARK_D,MARK_H,MARK_GAP=.6,.4,2.6,.6  # J10-MARK: groove width/depth, numeral height, stroke gap

def strokes(numeral):
    """2D stroke polygons for I/V numerals, centred on the origin."""
    out=[];x=0;h=MARK_H/2;w=MARK_W/2;vw=1.8
    for ch in numeral:
        if ch=='I':
            out.append([(x,-h),(x+MARK_W,-h),(x+MARK_W,h),(x,h)]);x+=MARK_W+MARK_GAP
        else:  # V: one outline, so the two strokes leave no sliver where they meet
            m=x+vw/2
            out.append([(x,h),(x+MARK_W,h),(m,-h+1.),(x+vw-MARK_W,h),(x+vw,h),(m+w,-h),(m-w,-h)]);x+=vw+MARK_GAP
    x-=MARK_GAP
    return [[(px-x/2,py) for px,py in p] for p in out]

def mark(numeral):
    top=J4.FLAT_Z
    return Compound(children=[extrude(Plane.XY.offset(top-MARK_D)*Polygon(*p,align=None),MARK_D+J.P.TOOL_EXT,dir=(0,0,1)) for p in strokes(numeral)])

def tabs(angle):
    out=[]
    for i in range(4):
        out.append(Rot(0,0,angle+90*i)*J.M.box(J.NECK/2-.3,TAB_TIP,-TAB_W/2,TAB_W/2,J.BOTTOM,J.BOTTOM+J.FLANGE_T))
    return out

def cap(tabs_at,lift,numeral):
    c=J8.cap(flange=J.FLANGE if tabs_at is None else J.NECK,lift=lift,rim=1.2,notches=0)
    if tabs_at is not None:
        for t in tabs(tabs_at):c+=t
    for s in mark(numeral).solids():c-=s
    return c

def main():
    STL.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    def vol(s):return sum(x.volume for x in s.solids())
    checks={};parts={}
    j9=J9.cap();sock=J.cylinder(J.NECK,J.BOTTOM-1,J.BOTTOM+4.2)
    for name,v in VARIANTS.items():
        c=cap(v['tabs'],v['lift'],name)
        checks[name+'_valid_single_solid']=c.is_valid and len(c.solids())==1
        checks[name+'_no_flat_overhang_in_socket']=not J7.overhangs(c)
        z0=J.BOTTOM+J2.ROUND_DEPTH-v['lift']
        checks[name+'_stem_fits']=J.overlap(J.M.box(-J.P.J4/2,J.P.J4/2,-J.P.J4/2,J.P.J4/2,z0,z0+J2.SQUARE_DEPTH),c)<1e-6
        checks[name+'_base_lip_clears']=J.overlap(J.cylinder(2.94,J.BOTTOM-J.P.TOOL_EXT,z0),c)<1e-6  # J4b
        checks[name+'_retains_past_hole']=(TAB_TIP if v['tabs'] is not None else J.FLANGE/2)>J.HOLE/2+.5
        mark_vol=vol(mark(name)&j9)
        checks[name+'_mark_cut']=mark_vol>0
        if v['lift']==.3:  # same socket as J9: the void inside the neck must match (the mark sits above it)
            checks[name+'_socket_identical_to_J9']=vol((sock-c)-(sock-j9))<1e-4 and vol((sock-j9)-(sock-c))<1e-4
        parts[name]=Pos(0,0,-J.BOTTOM)*c
        J.export(parts[name],STL/('joystick-j10-'+name+'.stl'))
    step=J.FLANGE+J6.GAP
    placed=[Pos(i*step,0,0)*p for i,p in enumerate(parts.values())]
    checks['plate_separate']=all(J.overlap(a,x)<1e-6 for a,x in itertools.combinations(placed,2))
    J.export(Compound(children=placed),STL/'joystick-j10-plate.stl')
    report=dict(checks=checks,passed=all(checks.values()),variants=VARIANTS,tab=dict(width=TAB_W,tip_radius=TAB_TIP),
        notes=['Numerals I-IV engraved on the flat top.','Tilt contact vs the v1.7 lid: tools/j10_tilt.py.','Press/tilt test pending.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    files=sorted(STL.glob('*.stl'))
    src=[Path(__file__),*(ROOT/'cad'/n for n in ('joystick_j9.py','joystick_j8.py','joystick_j7.py','joystick_j6.py','joystick_j4.py','joystick_j2.py','joystick_test.py'))]
    (OUT/'manifest.json').write_text(json.dumps(dict(revision='J10',source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in src},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}),indent=2)+'\n')
    print(json.dumps(report,indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
