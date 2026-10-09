"""RESET button v2 for the Atomic Wedgie base (Austin, 2026-10-08): the
1-notch AW-R cap is right (height, square). It went into the hole only after
some wiggling: its sharp post corners sit 0.35 in from the hole corners, which
are rounded 1.05, so the corners rub (~0.08). Fix: round the post's vertical
edges 0.5 and take 0.05 off each side. No notches.
Run: .venv/bin/python cad/aw_reset_v2.py
"""
import hashlib
from build123d import Axis, fillet
import aw_reset_caps as R
M,P,J=R.M,R.P,R.J

SHAVE=.05   # AW-RESET-V2: per side, Austin's ask
POST_R=.5   # AW-RESET-V2: clears the hole's 1.05 corners
OUT=R.ROOT/'stl/aw2/reset-button.stl'

def cap():
    fw,fd,t=P.CAP_FLANGE_W/2,P.CAP_FLANGE_D/2,R.A.CAP_FLANGE_T
    w,d=P.CAP_W/2-SHAVE,P.CAP_D/2-SHAVE
    post=M.box(-w,w,-d,d,t-P.EPS,R.INSIDE+R.PROUD[0])
    post=fillet(post.edges().filter_by(Axis.Z),POST_R)
    return M.box(-fw,fw,-fd,fd,0,t)+post

if __name__=='__main__':
    c=cap();assert c.is_valid and len(c.solids())==1
    J.export(c,OUT);print(c.bounding_box().size,hashlib.sha256(OUT.read_bytes()).hexdigest())
