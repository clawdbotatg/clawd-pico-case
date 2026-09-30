"""J15: J14-2 with a plain flat top (no dots). Austin, 2026-09-30: "we kinda
just want it to be flat on top". Everything else is J14-2 (checked).
Row J15 in MEASUREMENTS. Run: .venv/bin/python cad/joystick_j15.py
"""
import hashlib
import json
from build123d import Pos
import joystick_test as J
import joystick_j4 as J4
import joystick_j14 as J14

ROOT=J.ROOT
STL=ROOT/'stl/v1.4/joystick-j15'
SQUARE=J14.VARIANTS['2']  # J15: J14-2's 1.90 grip

def cap():
    return J14.cap(SQUARE,0)  # zero dots

def main():
    STL.mkdir(parents=True,exist_ok=True)
    def vol(s):return sum(x.volume for x in s.solids())
    c=cap();j=J14.cap(SQUARE,2)
    below=J.M.box(-6,6,-6,6,J.BOTTOM-1,J4.FLAT_Z-J14.DOT_DEPTH-.01)
    checks=dict(valid_single_solid=c.is_valid and len(c.solids())==1,
        same_as_J14_2_below_dots=vol((c&below)-(j&below))<1e-6 and vol((j&below)-(c&below))<1e-6,
        only_dots_filled=abs(vol(c-j)-2*3.14159265*(J14.DOT_D/2)**2*J14.DOT_DEPTH)<.01 and vol(j-c)<1e-6,
        flat_top_whole=abs(c.bounding_box().max.Z-J4.FLAT_Z)<1e-6)
    assert all(checks.values()),checks
    path=STL/'joystick-j15.stl';J.export(Pos(0,0,-J.BOTTOM)*c,path)
    print(json.dumps(dict(checks=checks,sha256=hashlib.sha256(path.read_bytes()).hexdigest()),indent=2))

if __name__=='__main__':main()
