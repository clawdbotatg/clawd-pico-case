"""AW1: Atomic Wedgie base v1, for the RP2040-Plus with a battery (Austin,
2026-10-08). BAT1 base (battery plug slot) plus: the old BOOTSEL pin hole is
filled; BOOT gets a pin hole at its new spot; RESET gets a hole for a standard
button cap (stl/current/button.stl, unchanged) pushed in from inside, flange
on the floor, pressed from under the case. Switch height is a guess
(AW1-SW-H), so this is a fit test. Rows AW1-*, RP2040PLUS-* in MEASUREMENTS.
Run: .venv/bin/python cad/aw1_base.py
"""
import hashlib
import json
from build123d import Cylinder, Pos
import bat1_base as B
L,M,S,P,J,V=B.L,B.M,B.S,B.P,B.J,B.V

ROOT=B.ROOT
STL=ROOT/'stl/aw1'
BTN_FROM_USB=22.02  # RP2040PLUS-BTN-Y
BTN_FROM_EDGE=6.0   # RP2040PLUS-BTN-EDGE
BTN_DX=P.P2/2-BTN_FROM_EDGE  # board width from the Pico rows (RP2040-Plus width not measured)
# Seen from below, +x is on the left, so BOOT (left, bottom face up) is +x.
BOOT=(M.PICO_CX+BTN_DX,M.PICO_Y1-BTN_FROM_USB)
RESET=(M.PICO_CX-BTN_DX,M.PICO_Y1-BTN_FROM_USB)
SW_H=2.65  # AW1-SW-H: plunger top above the PCB, guessed high (cap rattles if low; never held pressed)
CAP_FLANGE_T=.8  # stl/current/button.stl, measured from the file
CAP_H=4.29       # same file, total height

def cap():
    """The standard cap, flipped: flange up against the plunger, post down through the floor.
    Boxes with the file's sizes (the STL is a mesh, not a solid)."""
    x,y=RESET;z=M.Z_PICO_BOT-SW_H
    f=M.rbox(x-P.CAP_FLANGE_W/2,x+P.CAP_FLANGE_W/2,y-P.CAP_FLANGE_D/2,y+P.CAP_FLANGE_D/2,z-CAP_FLANGE_T,z,P.CAP_R)
    return f+M.rbox(x-P.CAP_W/2,x+P.CAP_W/2,y-P.CAP_D/2,y+P.CAP_D/2,z-CAP_H,z-CAP_FLANGE_T+P.EPS,P.CAP_R)

def main():
    STL.mkdir(parents=True,exist_ok=True)
    L.W.shorten()
    b,_=L.base()
    b-=B.slot()
    zf=(M.Z_BOTTOM+M.Z_FLOOR_TOP)/2
    old_hole=Pos(*M.ACCESS_C,zf)*Cylinder(P.ACCESS_D/2,P.FLOOR)
    b+=old_hole
    b-=Pos(*BOOT,zf)*Cylinder(P.ACCESS_D/2,P.FLOOR+2*P.TOOL_EXT)
    hw,hd=P.CAP_W/2+P.CAP_HOLE_CLEAR,P.CAP_D/2+P.CAP_HOLE_CLEAR
    x,y=RESET
    b-=M.rbox(x-hw,x+hw,y-hd,y+hd,M.Z_BOTTOM-P.TOOL_EXT,M.Z_FLOOR_TOP+P.TOOL_EXT,P.CAP_R+P.CAP_HOLE_CLEAR)
    c=cap();cb=c.bounding_box()
    def vol(s):return sum(x.volume for x in s.solids())
    slack=round(M.Z_PICO_BOT-SW_H-CAP_FLANGE_T-M.Z_FLOOR_TOP,2)
    checks=dict(base_valid_single_solid=b.is_valid and len(b.solids())==1,
        cap_clear_of_base=J.overlap(b,c)<1e-5,
        flange_fits_under_switch=slack>=0,
        old_hole_filled=vol(b & old_hole)>vol(old_hole)-.01,
        holes_apart=abs(M.ACCESS_C[1]-BOOT[1])>P.ACCESS_D)
    out=STL/'base-floor-down.stl'
    J.export(V.origin(b),out)
    report=dict(checks=checks,passed=all(checks.values()),boot_xy=[round(v,2) for v in BOOT],reset_xy=[round(v,2) for v in RESET],
        flange_slack_at_guess=slack,cap_below_floor=round(M.Z_BOTTOM-cb.min.Z,2),
        sha256=hashlib.sha256(out.read_bytes()).hexdigest())
    print(json.dumps(report,indent=2))
    if not report['passed']:raise SystemExit('Validation failed')

if __name__=='__main__':main()
