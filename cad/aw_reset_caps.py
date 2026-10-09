"""AW-R: shorter, square RESET caps for the Atomic Wedgie base (Austin,
2026-10-08: the standard cap sticks out 1.79 and gets hit when the case is
laid down; try ~85% height and shorter). Same flange and post plan size as
stl/current/button.stl, sharp corners and flat top so they read differently.
Sticks out 1.2 / 0.8 / 0.4 below the AW2 floor (at the AW1-SW-H guess);
1 / 2 / 3 notches on the flange edge. Run: .venv/bin/python cad/aw_reset_caps.py
"""
import hashlib
import json
import aw1_base as A
M,P,J=A.M,A.P,A.J

ROOT=A.ROOT
STL=ROOT/'stl/test/aw-reset'
PROUD=(1.2,0.8,0.4)  # AW-R-PROUD: below the base floor; 1.2 ~ 85% of the 4.29 cap
INSIDE=A.CAP_H-1.79  # flange top to the floor bottom, from AW1 (cap stuck out 1.79)
NOTCH_W,NOTCH_D,NOTCH_GAP=.5,.3,.5  # mark-caps-with-edge-notches; flange overhangs the post by 0.45 in y

def cap(proud,notches):
    fw,fd,t=P.CAP_FLANGE_W/2,P.CAP_FLANGE_D/2,A.CAP_FLANGE_T
    c=M.box(-fw,fw,-fd,fd,0,t)+M.box(-P.CAP_W/2,P.CAP_W/2,-P.CAP_D/2,P.CAP_D/2,t-P.EPS,INSIDE+proud)
    span=notches*NOTCH_W+(notches-1)*NOTCH_GAP
    for i in range(notches):
        x0=-span/2+i*(NOTCH_W+NOTCH_GAP)
        c-=M.box(x0,x0+NOTCH_W,fd-NOTCH_D,fd+P.TOOL_EXT,-P.TOOL_EXT,t+P.EPS)
    return c

def main():
    STL.mkdir(parents=True,exist_ok=True)
    out={}
    for i,p in enumerate(PROUD,1):
        c=cap(p,i);f=STL/f'reset-{i}-notch.stl'
        assert c.is_valid and len(c.solids())==1
        J.export(c,f);out[f.name]=dict(height=round(INSIDE+p,2),proud=p,sha256=hashlib.sha256(f.read_bytes()).hexdigest())
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
