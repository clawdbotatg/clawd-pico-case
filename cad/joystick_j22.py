"""J22: the production joystick = J21-1 with a plain flat top (no dot).
Austin, 2026-09-30: "Number one was the one ... smooth out the top".
J21-1 = J20's wide mouth (3.2 x 0.5 + 45 deg funnel), 1.90 square to a flat
roof 1.9 deep, J17-B tabs on the 8.6 thinned disc.
Row J22 in MEASUREMENTS. Run: .venv/bin/python cad/joystick_j22.py
"""
import hashlib
import json
from build123d import Pos
import joystick_test as J
import joystick_j4 as J4
import joystick_j17 as J17
import joystick_j20 as J20
import joystick_j21 as J21

ROOT=J.ROOT
STL=ROOT/'stl/v1.4/joystick-j22'
DEPTH=J21.DEPTHS['1']  # 1.9

def cap():
    return J20.cap(DEPTH,0)  # no dots

def main():
    STL.mkdir(parents=True,exist_ok=True)
    def vol(s):return sum(x.volume for x in s.solids())
    c=cap();j=J20.cap(DEPTH,1)
    below=J.M.box(-7,7,-7,7,J.BOTTOM-1,J4.FLAT_Z-J17.J14.DOT_DEPTH-.01)  # under the 0.5 deep dot
    checks=dict(valid_single_solid=c.is_valid and len(c.solids())==1,
        same_as_J21_1_below_the_dot=vol((c&below)-(j&below))<1e-6 and vol((j&below)-(c&below))<1e-6,
        only_the_dot_filled=vol(j-c)<1e-6 and 0<vol(c-j)<.5,
        flat_top=abs(c.bounding_box().max.Z-J4.FLAT_Z)<1e-6)
    assert all(checks.values()),checks
    path=STL/'joystick-j22.stl';J.export(Pos(0,0,-J.BOTTOM)*c,path)
    print(json.dumps(dict(checks=checks,sha256=hashlib.sha256(path.read_bytes()).hexdigest()),indent=2))

if __name__=='__main__':main()
