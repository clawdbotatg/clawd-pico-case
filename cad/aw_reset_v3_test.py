"""RESET v3 test (Austin, 2026-10-08): v2 sticks out too far when the Pico
doesn't seat fully in the LCD board; wants ~0.75 shorter. Three heights:
0.60 / 0.75 / 0.90 shorter than v2 (1 / 2 / 3 flange notches). Otherwise v2.
Run: .venv/bin/python cad/aw_reset_v3_test.py
"""
import hashlib
import aw_reset_v2 as V2
R,M,P,J=V2.R,V2.M,V2.P,V2.J

CUTS=(.60,.75,.90)  # AW-RESET-V3-TEST
STL=R.ROOT/'stl/test/aw-reset-v3'

def cap(cut,notches):
    c=V2.cap()-M.box(-5,5,-5,5,R.INSIDE+R.PROUD[0]-cut,10)
    fd,t=P.CAP_FLANGE_D/2,R.A.CAP_FLANGE_T
    span=notches*R.NOTCH_W+(notches-1)*R.NOTCH_GAP
    for i in range(notches):
        x0=-span/2+i*(R.NOTCH_W+R.NOTCH_GAP)
        c-=M.box(x0,x0+R.NOTCH_W,fd-R.NOTCH_D,fd+P.TOOL_EXT,-P.TOOL_EXT,t+P.EPS)
    return c

if __name__=='__main__':
    STL.mkdir(parents=True,exist_ok=True)
    for i,cut in enumerate(CUTS,1):
        c=cap(cut,i);assert c.is_valid and len(c.solids())==1
        f=STL/f'reset-v3-{i}-notch.stl';J.export(c,f)
        print(f.name,round(c.bounding_box().size.Z,2),hashlib.sha256(f.read_bytes()).hexdigest()[:12])
