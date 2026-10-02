"""V1.9 TEST (not current): the v1.8 +0.3 lid (Austin, 2026-10-01: "works pretty
darn well" with J22) plus two changes:
 1. Screen gap: the bezel ring was built to sit GLASS_GAP (0.3) above the
    glass (V1.4-GLASS-GAP), but the v1.5 (+0.5) and v1.8 (+0.3) stretches
    lifted it too, to 1.1 above the glass. Fill the ring back down to 0.3.
 2. Logo inlay: an original line drawing of briefs (drawn here, not traced
    from any image), set flush into the top face beside the joystick, 2
    layers deep. Printed face down, the slicer gives the logo part a second
    filament for its first layers; the rest of the lid prints over it.
Placement: held landscape with the joystick on the left, "under the
joystick" is the -x side of the hole; the logo stands upright that way
(its up = +x, its right = -y).
Rows V1.9-* in MEASUREMENTS. Run: .venv/bin/python cad/v1_9_test.py
Outputs go to stl/test/v1.9/, never stl/current.
"""
import hashlib
import json
from build123d import Pos, Rot, Compound, Polygon, Plane, extrude
import v1_8_test as T8
import v1_4_rounded as R
import v1_7_lock as L7
J,M,S,V=T8.J,T8.M,T8.S,T8.V
P=M.P

ROOT=T8.ROOT
STL=ROOT/'stl/test/v1.9'
OUT=ROOT/'renders/test/v1.9'
RAISE=.3                 # V1.9: the +0.3 lid that worked
INLAY_D=.32              # V1.9-LOGO: two 0.16 layers
LOGO_C=(4.6,None)        # V1.9-LOGO: centre x; y = the joystick hole's
LOGO_SCALE=1.0           # 9.0 wide x 6.8 tall

def bezier(p0,p1,p2,n=8):
    return [((1-t)**2*p0[0]+2*(1-t)*t*p1[0]+t*t*p2[0],(1-t)**2*p0[1]+2*(1-t)*t*p1[1]+t*t*p2[1]) for t in (i/n for i in range(n+1))]

def logo_2d():
    """Briefs: waistband over a body with curved leg openings, in (u right, v up)."""
    s=LOGO_SCALE
    band=[(-4.5,2.0),(4.5,2.0),(4.5,3.3),(-4.5,3.3)]  # waistband; 0.5 gap below it stays lid colour
    right=bezier((4.5,.6),(2.0,-.2),(1.3,-3.5))
    left=[(-x,y) for x,y in reversed(right)]
    body=[(-4.5,1.5),(4.5,1.5),*right,*left]
    return [[(x*s,y*s) for x,y in p] for p in (band,body)]

def logo(top):
    hx,hy=M.JOY_C[0]+V.L4.DX,M.JOY_C[1]+V.L4.DY+V.JOY_DY
    cx,cy=LOGO_C[0],hy
    out=[]
    for poly in logo_2d():
        pts=[(cx+v,cy-u) for u,v in poly]  # logo up = +x, logo right = -y
        out.append(extrude(Plane.XY.offset(top-INLAY_D)*Polygon(*pts,align=None),INLAY_D,dir=(0,0,1)))
    return Compound(children=out)

def bezel_fill(top_under):
    """The bezel ring from GLASS_GAP above the glass up to its raised underside."""
    gx,gy=M.GLASS_C;c=P.WINDOW_CLEAR
    x0,x1,y0,y1=gx-P.S2/2-c,gx+P.S2/2+c,gy-P.S1/2-c,gy+P.S1/2+c  # the pre-V1.4 window (R.narrow_window's bb)
    z0=P.S3+R.GLASS_GAP
    return M.rbox(x0,x1,y0,y1,z0,top_under+P.EPS,P.WINDOW_R)-M.rbox(x0+R.WINDOW_IN,x1-R.WINDOW_IN,y0+R.WINDOW_IN,y1-R.WINDOW_IN,z0-1,top_under+1,P.WINDOW_R)

def build():
    L7.W.shorten()
    l,_=T8.lid(RAISE)
    gx,gy=M.GLASS_C
    probe=lambda shape:(shape & M.box(gx-P.S2/2+.1,gx-P.S2/2+.5,gy-5,gy+5,P.S3,10)).bounding_box().min.Z
    under=probe(l)
    l=l+bezel_fill(under)
    top=l.bounding_box().max.Z
    lg=logo(top)
    for s in lg.solids():l-=s
    return l,lg,under,probe(l),top

def main():
    STL.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    def vol(s):return sum(x.volume for x in s.solids())
    l,lg,under,new_under,top=build()
    l8,_=T8.lid(RAISE)
    gx,gy=M.GLASS_C
    sight=M.rbox(gx-P.S2/2+R.WINDOW_IN-P.WINDOW_CLEAR+.01,gx+P.S2/2-R.WINDOW_IN+P.WINDOW_CLEAR-.01,gy-P.S1/2+R.WINDOW_IN-P.WINDOW_CLEAR+.01,gy+P.S1/2-R.WINDOW_IN+P.WINDOW_CLEAR-.01,P.S3,top+1,P.WINDOW_R)
    flat=M.box(S.X0-5,S.X1+5,S.Y0-5,S.Y1+5,top-INLAY_D-.05,top)
    area=sum(f.area for s in lg.solids() for f in s.faces() if f.normal_at().Z>.99)
    checks=dict(lid_valid_single_solid=l.is_valid and len(l.solids())==1,
        bezel_was_raised=abs(under-(P.S3+R.GLASS_GAP+T5_RAISE_TOTAL))<.02,
        bezel_now_0_3_over_glass=abs(new_under-(P.S3+R.GLASS_GAP))<1e-3,
        window_still_clear=vol(l & sight)<1e-6,
        logo_parts_valid=all(s.is_valid for s in lg.solids()) and len(lg.solids())==2,
        logo_on_flat_top=abs(vol(l8 & flat & Compound(children=[Pos(0,0,0)*s for s in lg.solids()]))-area*INLAY_D)<.02,
        logo_fills_its_pocket=vol(Compound(children=list(lg.solids())) & l)<1e-6,
        only_bezel_and_logo_changed=abs(vol(l)-(vol(l8)+vol(bezel_fill(under)-l8)-area*INLAY_D))<.05)
    face_down=lambda s:Rot(180,0,0)*s
    shift=l.bounding_box();lf=face_down(l);bb=lf.bounding_box();d=Pos(-bb.min.X,-bb.min.Y,-bb.min.Z)
    J.export(d*lf,STL/'lid-v1.9-test-face-down.stl')
    J.export(d*face_down(Compound(children=list(lg.solids()))),STL/'logo-inlay-face-down.stl')
    report=dict(status='TEST, not current',checks=checks,passed=all(checks.values()),bezel_underside_before=round(under,3),bezel_underside_after=round(new_under,3),
        glass_top=P.S3,logo_area_mm2=round(area,2),inlay_depth=INLAY_D,
        sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(STL.glob('*.stl'))})
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

T5_RAISE_TOTAL=T8.T5.RAISE+RAISE  # 0.5 (v1.5) + 0.3

if __name__=='__main__':main()
