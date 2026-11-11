"""Wedgie v2 base (AW3): Atomic Wedgie base, holds better (Austin, 2026-11-10). The AW2 base
(RESET plunger hole, BOOT pin hole, battery slot), printed black, for the
RP2040-Plus without a battery. Same lid as now: printed lids must fit, so
every change is on the base side of the joint:
(1) catches 6.5 wide instead of 6.0 (lid pockets are 6.6: 0.05 a side left);
(2) hook 0.54 instead of 0.5 (lid pocket depth 0.55: 0.01 left);
(4) the battery slot 1.8 deep instead of 1.0;
(3) the tongue's lower part on the long sides is 0.8 thicker on the inside, so
    the tongue flexes less and the catches push harder. It stops 0.3 below the
    LCD board and stays clear of the Pico.
Rows AW3-* in MEASUREMENTS. Run: .venv/bin/python cad/wedgie_v2_base.py
"""
import hashlib
import json
from build123d import Cylinder, Pos, Compound
import aw2_base as A2
A=A2.A
B,L,M,S,P,J,V=A.B,A.L,A.M,A.S,A.P,A.J,A.V
import v1_1_spacer as SP

ROOT=A.ROOT
STL=ROOT/'stl/wedgie-v2'
CATCH_W=6.5   # AW3-CATCH-W: lid pocket width 2*(SNAP_W/2+END_CLEAR)=6.6, 0.05 a side spare
HOOK=.54      # AW3-HOOK: lid pocket depth L.RECESS 0.55, 0.01 spare
PROJ=S.GAP+HOOK
STIFF_IN=.8   # AW3-STIFF: inward thickening of the long-side tongue
STIFF_TOP_GAP=.3  # AW3-STIFF: clearance under the LCD board
SLOT_D=1.8    # AW3-SLOT: was 1.0 (BAT1-SLOT); leaves 1.2 of end wall below the seam

def slot():
    y=M.IY0  # AW2 slot, deeper: floor to tongue top; cuts through the tongue there (lid covers it)
    return M.box(M.PICO_CX-B.SLOT_W/2,M.PICO_CX+B.SLOT_W/2,y-SLOT_D,y+P.EPS,M.Z_FLOOR_TOP-P.EPS,S.SEAM+S.LAP+P.TOOL_EXT)

def profile(face,sgn):
    o=-sgn  # same shape as v1.7 L.hook_profile, deeper tip
    return [(face-o*P.EPS,L.Z_HOLD),(face+o*PROJ,L.Z_HOLD),(face+o*PROJ,L.Z_HOLD+L.NOSE),(face,L.Z_RAMP_TOP),(face-o*P.EPS,L.Z_RAMP_TOP)]

def catches():
    """Five catches: both long sides x2, USB end. The slot end has none (AW2)."""
    xl,xr=S.X0+S.SKIN+S.GAP,S.X1-S.SKIN-S.GAP
    yr=S.Y1-S.SKIN-S.GAP;w=CATCH_W/2
    out=[]
    for yc in L.LONG_Y:
        out+=[M.wedge_x(profile(xl,1),yc-w,yc+w),M.wedge_x(profile(xr,-1),yc-w,yc+w)]
    for xc in L.END_X:
        c=SP.wedge_y(profile(yr,-1),xc-w,xc+w)
        out.append(Pos(xc-w-c.bounding_box().min.X,0,0)*c)
    return Compound(children=out)

def stiffeners(z_top):
    """Inside the long-side tongue walls, from the seam up to z_top."""
    y0,y1=M.IY0+1.0,M.IY1-1.0  # stop short of the ends and corners
    return Compound(children=[M.box(M.IX0-P.EPS,M.IX0+STIFF_IN,y0,y1,S.SEAM-P.EPS,z_top),
                              M.box(M.IX1-STIFF_IN,M.IX1+P.EPS,y0,y1,S.SEAM-P.EPS,z_top)])

def base():
    L.W.shorten()
    b,_=L.base()  # v1.7 base, 6 catches
    old=b
    xl,xr=S.X0+S.SKIN+S.GAP,S.X1-S.SKIN-S.GAP
    w=CATCH_W/2+P.EPS
    for yc in L.LONG_Y:  # strip v1.7 long catches (outside tongue face only)
        for xa,xb in ((S.X0-P.TOOL_EXT,xl),(xr,S.X1+P.TOOL_EXT)):
            b-=M.box(xa,xb,yc-w,yc+w,S.SEAM+P.EPS,S.SEAM+S.LAP+P.TOOL_EXT)
    yl,yr=S.Y0+S.SKIN+S.GAP,S.Y1-S.SKIN-S.GAP
    for xc in L.END_X:  # both end catches out; USB end comes back bigger, slot end stays gone
        b-=M.box(xc-w,xc+w,S.Y0-P.TOOL_EXT,yl,S.SEAM+P.EPS,S.SEAM+S.LAP+P.TOOL_EXT)
        b-=M.box(xc-w,xc+w,yr,S.Y1+P.TOOL_EXT,S.SEAM+P.EPS,S.SEAM+S.LAP+P.TOOL_EXT)
    for c in catches().solids():b+=c
    hat_bottom=M.hat().bounding_box().min.Z
    z_top=hat_bottom-STIFF_TOP_GAP
    for s in stiffeners(z_top).solids():b+=s
    # AW2 changes, unchanged
    b-=slot()
    zf=(M.Z_BOTTOM+M.Z_FLOOR_TOP)/2
    x,y=M.ACCESS_C
    b+=Pos(x,y+V.RESET_DY/2,zf)*Cylinder(P.ACCESS_D/2+abs(V.RESET_DY)/2+.2,P.FLOOR)
    b-=Pos(*A.BOOT,zf)*Cylinder(P.ACCESS_D/2,P.FLOOR+2*P.TOOL_EXT)
    hw,hd=P.CAP_W/2+P.CAP_HOLE_CLEAR,P.CAP_D/2+P.CAP_HOLE_CLEAR
    rx,ry=A.RESET
    b-=M.rbox(rx-hw,rx+hw,ry-hd,ry+hd,M.Z_BOTTOM-P.TOOL_EXT,M.Z_FLOOR_TOP+P.TOOL_EXT,P.CAP_R+P.CAP_HOLE_CLEAR)
    return b,z_top

def main():
    STL.mkdir(parents=True,exist_ok=True)
    b,z_top=base()
    l,_=L.lid()  # v1.7 lid: same joint and pockets as v1.9 (v1.9 stretches above z=1.0)
    ribs=A.L.R.ribs()
    from build123d import Pos as Ps
    cat=catches()
    def vol(s):return sum(v.volume for v in s.solids())
    checks=dict(base_valid_single_solid=b.is_valid and len(b.solids())==1,
        five_catches=len(cat.solids())==5,
        catches_clear_lid_closed=J.overlap(cat,l)<1e-5,
        closed_contact_only_at_ribs=J.overlap(b,l-ribs)<1e-5,
        catches_hook_into_lid=all(J.overlap(Ps(0,0,L.T.FREE_PLAY+.02)*l,c)>1e-4 for c in cat.solids()),
        stiffeners_clear_board=J.overlap(b,M.hat()+M.pico())<1e-5,
        stiffeners_below_board=z_top>S.SEAM+.5,
        slot_open=J.overlap(b,slot())<1e-5,
        end_wall_left=round(M.IY0-SLOT_D-S.Y0,2)>=1.2,
        cap_clear_of_base=J.overlap(b,A.cap())<1e-5)
    out=STL/'base-floor-down.stl'
    J.export(V.origin(b),out)
    report=dict(checks=checks,passed=all(checks.values()),catch_w=CATCH_W,hook=HOOK,
        stiffener=dict(inward=STIFF_IN,z=[round(S.SEAM,2),round(z_top,2)],height=round(z_top-S.SEAM,2)),
        sha256=hashlib.sha256(out.read_bytes()).hexdigest())
    print(json.dumps(report,indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
