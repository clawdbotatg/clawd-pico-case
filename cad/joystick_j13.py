"""J13: J11-III between VI and VII, and VII-plus with a thinner flange edge.
Austin, 2026-09-30: VI (lift 0.5) keeps the directions clean but the centre
press doesn't quite click; VII (0.6) clicks the centre every time but some
directions click it too. Riding height sets the press room (cap underside);
the flange TOP sets when the lid is hit. Thinning the flange where it sits
under the lid (r >= 4, outside the 8 mm hole) lowers its top without moving
the underside, so a cap can ride VII-high with VI's lid room.
A smaller square cannot help: its corners must reach past the hole, and the
7.2 square's corners (5.09 on the diagonal) are already near that limit.
Round caps: through the hole you can see past the square's flat sides into
the case (Austin). A disc just past the hole covers it all round. In the
model a 9.0 disc at VII height has less lid room than VII (14.6 vs 15.8 deg),
8.8 about the same, 8.6 much more; 8.6 overlaps the hole by only 0.3.
Letters engraved bold on top, one per cap (Austin: the numerals printed as
"weird holes"):
  H  square, lift 0.55, J11-III flange as is
  T  square, lift 0.60, flange edge thinned to 0.24
  L  square, lift 0.65, thinned
  X  square, lift 0.70, thinned
  O  round 8.6, lift 0.60, thinned
  E  round 8.8, lift 0.60, thinned
Rows J13-* in MEASUREMENTS. Run: .venv/bin/python cad/joystick_j13.py
"""
import hashlib
import itertools
import json
from pathlib import Path
from build123d import Pos, Compound, Cone, Polygon, Plane, extrude
import joystick_test as J
import joystick_j2 as J2
import joystick_j4 as J4
import joystick_j7 as J7
import joystick_j8 as J8
import joystick_j11 as J11
import j10_tilt as TILT

ROOT=J.ROOT
STL=ROOT/'stl/v1.4/joystick-j13'
OUT=ROOT/'renders/v1.4/joystick-j13'
FLATS,TURN=J11.VARIANTS['III']  # J13-KEEP: J11-III flange
EDGE_T=.24          # J13-THIN: flange thickness under the lid
TAPER=(3.4,J.HOLE/2)  # J13-THIN: full 0.4 inside r 3.4, EDGE_T from the hole edge (r 4) out
VARIANTS={'H':(.55,False,None),'T':(.60,True,None),'L':(.65,True,None),'X':(.70,True,None),
          'O':(.60,True,8.6),'E':(.60,True,8.8)}  # J13-LIFT / J13-ROUND: lift, thinned edge, disc (None = J11-III square)
SW,LH,LW,MARK_D=.9,3.2,2.6,.5  # J13-MARK: stroke width, letter height and width, groove depth

def bar(p0,p1,w=SW):
    (x0,y0),(x1,y1)=p0,p1;dx,dy=x1-x0,y1-y0;n=(dx*dx+dy*dy)**.5;ox,oy=-dy/n*w/2,dx/n*w/2
    return [(x0+ox,y0+oy),(x1+ox,y1+oy),(x1-ox,y1-oy),(x0-ox,y0-oy)]

def letter(ch):
    """Bold straight-stroke letters as 2D polygons, centred, readable from above."""
    h,w,s=LH/2,LW/2,SW
    box=lambda x0,x1,y0,y1:[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
    return {'H':[box(-w,-w+s,-h,h),box(w-s,w,-h,h),box(-w,w,-s/2,s/2)],
            'T':[box(-w,w,h-s,h),box(-s/2,s/2,-h,h)],
            'L':[box(-w,-w+s,-h,h),box(-w,w,-h,-h+s)],
            'X':[bar((-w+s/2,-h+s/2),(w-s/2,h-s/2)),bar((-w+s/2,h-s/2),(w-s/2,-h+s/2))],
            'O':[box(-w,-w+s,-h,h),box(w-s,w,-h,h),box(-w,w,h-s,h),box(-w,w,-h,-h+s)],
            'E':[box(-w,-w+s,-h,h),box(-w,w,h-s,h),box(-w,w*.6,-s/2,s/2),box(-w,w,-h,-h+s)]}[ch]

def mark(ch):
    top=J4.FLAT_Z
    return [extrude(Plane.XY.offset(top-MARK_D)*Polygon(*p,align=None),MARK_D+J.P.TOOL_EXT,dir=(0,0,1)) for p in letter(ch)]

def thin_cut():
    """Material above the thinned flange top: the full 0.4 layer outside a cone
    that falls from 0.4 at r 3.4 to EDGE_T at r 4."""
    z1=J.BOTTOM+J.FLANGE_T;z0=J.BOTTOM+EDGE_T;r0,r1=TAPER
    keep=Pos(0,0,(z0+z1)/2)*Cone(r1,r0,z1-z0)
    return J.cylinder(14,z0,z1+J.P.EPS)-keep-J.cylinder(J.NECK,z0-1,z1+1)

def cap(lift,thin,disc,ch):
    if disc:c=J8.cap(flange=disc,lift=lift,rim=1.2,notches=0)  # J9 with a smaller disc
    else:c=J11.cap(FLATS,TURN,'',lift=lift)  # J11-III at this lift, no numeral
    if thin:c-=thin_cut()
    for s in mark(ch):c-=s
    return c

def main():
    STL.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    def vol(s):return sum(x.volume for x in s.solids())
    checks={};parts={};caps={}
    vi=J11.cap(FLATS,TURN,'VI',lift=.5);vii=J11.cap(FLATS,TURN,'VII',lift=.6)
    under=J.M.box(-6,6,-6,6,J.BOTTOM+EDGE_T+.02,J.BOTTOM+J.FLANGE_T-.02)-J.cylinder(J.HOLE,J.BOTTOM-1,J.BOTTOM+1)
    for name,(lift,thin,disc) in VARIANTS.items():
        c=cap(lift,thin,disc,name)
        z0=J.BOTTOM+J2.ROUND_DEPTH-lift
        checks[name+'_valid_single_solid']=c.is_valid and len(c.solids())==1
        checks[name+'_no_flat_overhang_in_socket']=not J7.overhangs(c)
        checks[name+'_stem_fits']=J.overlap(J.M.box(-J.P.J4/2,J.P.J4/2,-J.P.J4/2,J.P.J4/2,z0,z0+J2.SQUARE_DEPTH),c)<1e-6
        checks[name+'_base_lip_clears']=J.overlap(J.cylinder(2.94,J.BOTTOM-J.P.TOOL_EXT,z0),c)<1e-6  # J4b
        checks[name+'_mark_inside_flat_top']=max((x*x+y*y)**.5 for p in letter(name) for x,y in p)<2.5
        checks[name+'_mark_cut']=vol(Compound(children=mark(name))&cap(lift,False,disc,'H'))>0 if name!='H' else vol(Compound(children=mark(name))&cap(lift,False,disc,'T'))>0
        checks[name+('_flange_thinned_under_lid' if thin else '_flange_full_under_lid')]=(vol(c&under)<1e-4) if thin else (vol(c&under)>.01)
        if disc:checks[name+'_disc_past_hole']=disc/2-J.HOLE/2>=.3-1e-9
        checks[name+'_flange_bottom_flat_on_bed']=abs(c.bounding_box().min.Z-J.BOTTOM)<1e-6
        parts[name]=Pos(0,0,-J.BOTTOM)*c;caps['J13-'+name]=(c,lift)
        J.export(parts[name],STL/('joystick-j13-'+name+'.stl'))
    step=max(J11.CORNER_D,9.0)+J11.GAP
    placed=[Pos(i*step,0,0)*p for i,p in enumerate(parts.values())]
    checks['plate_separate']=all(J.overlap(a,x)<1e-6 for a,x in itertools.combinations(placed,2))
    J.export(Compound(children=placed),STL/'joystick-j13-plate.stl')
    tilt=TILT.tilt({'J12-VI':(vi,.5),'J12-VII':(vii,.6),**caps})
    for n in caps:checks[n+'_clear_of_lid_at_rest']=not tilt['caps'][n]['touches_at_rest']
    report=dict(checks=checks,passed=all(checks.values()),flats=FLATS,edge_t=EDGE_T,taper=TAPER,variants=VARIANTS,tilt=tilt,
        notes=['Press room follows lift; lid room follows the flange top (lift minus 0.16 where thinned).','Thinned corners are 0.24 thick: retention only, check they survive removal from the bed.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    files=sorted(STL.glob('*.stl'))
    src=[Path(__file__),*(ROOT/'cad'/n for n in ('joystick_j11.py','j10_tilt.py','joystick_j10.py','joystick_j8.py','joystick_j7.py','joystick_test.py'))]
    (OUT/'manifest.json').write_text(json.dumps(dict(revision='J13',source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in src},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}),indent=2)+'\n')
    print(json.dumps(dict(checks=checks,passed=report['passed']),indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
