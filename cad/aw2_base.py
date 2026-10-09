"""AW2: Atomic Wedgie base v2 (Austin, 2026-10-08, after printing AW1).
(1) The battery slot runs all the way up, through the tongue, so the plug can
slide in from the top. The catch on that end is removed (it sat on the slot);
5 catches left, current lid still fits. (2) The old BOOTSEL hole is filled for
real: AW1 filled the S1 spot, but v1.0 had moved it 0.25 (RESET_DY).
RESET and BOOT holes unchanged from AW1. Run: .venv/bin/python cad/aw2_base.py
"""
import hashlib
import json
from build123d import Cylinder, Pos
import aw1_base as A
B,L,M,S,P,J,V=A.B,A.L,A.M,A.S,A.P,A.J,A.V

ROOT=A.ROOT
STL=ROOT/'stl/aw2'

def slot():
    # AW2-SLOT: BAT1 slot taken to the top of the tongue
    y=M.IY0
    return M.box(M.PICO_CX-B.SLOT_W/2,M.PICO_CX+B.SLOT_W/2,y-B.SLOT_D,y+P.EPS,M.Z_FLOOR_TOP-P.EPS,S.SEAM+S.LAP+P.TOOL_EXT)

def end_catch():
    # AW2-CATCH: the v1.7 catch on the non-USB end, outside the tongue face only
    yl=S.Y0+S.SKIN+S.GAP
    return M.box(M.CX-L.W2-P.EPS,M.CX+L.W2+P.EPS,S.Y0-P.TOOL_EXT,yl,S.SEAM+P.EPS,S.SEAM+S.LAP+P.TOOL_EXT)

def main():
    STL.mkdir(parents=True,exist_ok=True)
    L.W.shorten()
    b,_=L.base()
    had_catch=J.overlap(b,end_catch())
    b-=end_catch()
    b-=slot()
    zf=(M.Z_BOTTOM+M.Z_FLOOR_TOP)/2
    x,y=M.ACCESS_C
    fill=Pos(x,y+V.RESET_DY/2,zf)*Cylinder(P.ACCESS_D/2+abs(V.RESET_DY)/2+.2,P.FLOOR)  # covers both old spots
    b+=fill
    b-=Pos(*A.BOOT,zf)*Cylinder(P.ACCESS_D/2,P.FLOOR+2*P.TOOL_EXT)
    hw,hd=P.CAP_W/2+P.CAP_HOLE_CLEAR,P.CAP_D/2+P.CAP_HOLE_CLEAR
    rx,ry=A.RESET
    b-=M.rbox(rx-hw,rx+hw,ry-hd,ry+hd,M.Z_BOTTOM-P.TOOL_EXT,M.Z_FLOOR_TOP+P.TOOL_EXT,P.CAP_R+P.CAP_HOLE_CLEAR)
    def vol(s):return sum(v.volume for v in s.solids())
    old_hole=V.reset_cut(V.RESET_DY,0)
    checks=dict(base_valid_single_solid=b.is_valid and len(b.solids())==1,
        end_catch_was_there=had_catch>.1,
        end_catch_gone=J.overlap(b,end_catch())<1e-5,
        slot_open_to_top=J.overlap(b,slot())<1e-5,
        tongue_left_behind_slot=round(M.IY0-B.SLOT_D-(S.Y0+S.SKIN+S.GAP),2)>=.4,
        old_hole_filled=vol(b & old_hole)>vol(old_hole & M.box(-50,50,-50,90,M.Z_BOTTOM,M.Z_FLOOR_TOP))-.01,
        cap_clear_of_base=J.overlap(b,A.cap())<1e-5)
    out=STL/'base-floor-down.stl'
    J.export(V.origin(b),out)
    report=dict(checks=checks,passed=all(checks.values()),tongue_behind_slot=round(M.IY0-B.SLOT_D-(S.Y0+S.SKIN+S.GAP),2),
        sha256=hashlib.sha256(out.read_bytes()).hexdigest())
    print(json.dumps(report,indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
