"""J11: J9 with a square flange whose corners point to the diagonals.
Austin, 2026-09-30, after J10's tabs slipped through the lid hole: keep the
cap that sat on the stick, and make the flange "a square ... where the thin
part is up, down, left and right and the corners go to NE, NW, SE, SW".
Across the flats it is narrower than J9's 10.4 disc, so the edge behind a
push rises less toward the lid; across the corners it is far wider than the
8 mm hole, so it cannot fall through.
The cap can only sit on the stem in the stem square's orientation, which is
not measured, so the plate carries both turns, in two sizes:
  I   8.0 across the flats, in line with the socket square
  II  8.0 across the flats, turned 45 deg
  III 7.2 across the flats, in line
  IV  7.2 across the flats, turned 45 deg
Keep the pair whose flat sides face up/down/left/right on the device; the
smaller square leaves more room, the corners still hold it in the hole.
Rows J11-* in MEASUREMENTS. Run: .venv/bin/python cad/joystick_j11.py
"""
import hashlib
import itertools
import json
from pathlib import Path
from build123d import Pos, Rot, Compound
import joystick_test as J
import joystick_j7 as J7
import joystick_j8 as J8
import joystick_j9 as J9
import joystick_j10 as J10
import j10_tilt as TILT

ROOT=J.ROOT
STL=ROOT/'stl/v1.4/joystick-j11'
OUT=ROOT/'renders/v1.4/joystick-j11'
CORNER_D=11.0 # J11-SQUARE: corners clipped to this circle; 1.5 past the hole edge
VARIANTS={'I':(8.0,0),'II':(8.0,45),'III':(7.2,0),'IV':(7.2,45)}  # J11-SQUARE / J11-ORIENT: flats, turn vs the socket square (deg)
LIFT=.3       # J9's ride height (J5-LIFT)
GAP=4.0       # plate spacing

def cap(flats,turn,numeral):
    c=J8.cap(flange=J.NECK,lift=LIFT,rim=1.2,notches=0)  # J9 without its disc
    h=flats/2
    square=Rot(0,0,turn)*J.M.box(-h,h,-h,h,J.BOTTOM,J.BOTTOM+J.FLANGE_T) & J.cylinder(CORNER_D,J.BOTTOM-1,J.BOTTOM+1)
    c=c+square-J8.cavity(J8.SQUARE,LIFT)  # re-open the socket mouth under the square
    for s in J10.mark(numeral).solids():c-=s
    return c

def main():
    STL.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    def vol(s):return sum(x.volume for x in s.solids())
    checks={};parts={};caps={}
    j9=J9.cap();sock=J.cylinder(J.NECK,J.BOTTOM-1,J.BOTTOM+4.2)
    above=J.M.box(-6,6,-6,6,J.BOTTOM+J.FLANGE_T+J.P.EPS,20)
    for name,(flats,turn) in VARIANTS.items():
        c=cap(flats,turn,name)
        checks[name+'_valid_single_solid']=c.is_valid and len(c.solids())==1
        checks[name+'_socket_identical_to_J9']=vol((sock-c)-(sock-j9))<1e-4 and vol((sock-j9)-(sock-c))<1e-4
        checks[name+'_same_as_J9_above_flange_except_mark']=vol(((c&above)-(j9&above)))<1e-4 and 0<vol((j9&above)-(c&above))<2
        checks[name+'_no_flat_overhang_in_socket']=not J7.overhangs(c)
        checks[name+'_flats_narrower_than_J9_disc']=flats<J.FLANGE
        checks[name+'_corners_past_hole']=min(CORNER_D/2,flats/2**.5)-J.HOLE/2>=1.0
        parts[name]=Pos(0,0,-J.BOTTOM)*c;caps['J11-'+name]=(c,LIFT)
        J.export(parts[name],STL/('joystick-j11-'+name+'.stl'))
    step=CORNER_D+GAP
    placed=[Pos(i*step,0,0)*p for i,p in enumerate(parts.values())]
    checks['plate_separate']=all(J.overlap(a,x)<1e-6 for a,x in itertools.combinations(placed,2))
    J.export(Compound(children=placed),STL/'joystick-j11-plate.stl')
    tilt=TILT.tilt({'J9':(j9,LIFT),**caps})
    for n in caps:checks[n+'_clear_of_lid_at_rest']=not tilt['caps'][n]['touches_at_rest']
    report=dict(checks=checks,passed=all(checks.values()),corner_d=CORNER_D,variants=VARIANTS,tilt=tilt,
        notes=['I/III: flange square in line with the socket; II/IV: turned 45 deg. Keep the pair whose flats face up/down/left/right.','Numerals engraved on top as J10.','Tilt angles compare caps only; true tilt and seating are unmeasured.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    files=sorted(STL.glob('*.stl'))
    src=[Path(__file__),*(ROOT/'cad'/n for n in ('j10_tilt.py','joystick_j10.py','joystick_j9.py','joystick_j8.py','joystick_j7.py','joystick_test.py'))]
    (OUT/'manifest.json').write_text(json.dumps(dict(revision='J11',source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in src},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}),indent=2)+'\n')
    print(json.dumps(dict(checks=checks,passed=report['passed']),indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
