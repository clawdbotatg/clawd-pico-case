"""J9 (v1.4 joystick candidate): J8-3 without notches = J7-B's 1.90 printable
socket plus the 1.2 mm round top edge. Austin: B has the best hole, 3 the
best surface. Rows J9-* in MEASUREMENTS. Run: .venv/bin/python cad/joystick_j9.py
"""
import hashlib
import json
from build123d import Pos
import joystick_test as J
import joystick_j7 as J7
import joystick_j8 as J8

ROOT=J.ROOT
STL=ROOT/'stl/v1.4'
PARAMS=dict(J8.VARIANTS['3'],notches=0)  # J9: J8-3 geometry, no ID notches

def cap():
    return J8.cap(**PARAMS)

def main():
    c=cap();b,_=J7.cap(J8.SQUARE,0,2);c3=J8.cap(**J8.VARIANTS['3'])
    def vol(s):return sum(x.volume for x in s.solids())
    sock=J.cylinder(J.NECK,J.BOTTOM-1,J.BOTTOM+4.2)
    checks=dict(valid_single_solid=c.is_valid and len(c.solids())==1,
        socket_identical_to_J7B=vol((sock-c)-(sock-b))<1e-6 and vol((sock-b)-(sock-c))<1e-6,
        no_flat_overhang_in_socket=not J7.overhangs(c),
        same_as_J8_3_except_notches=vol(c3-c)<1e-6 and 0<vol(c-c3)<1)
    assert all(checks.values()),checks
    path=STL/'joystick-j9.stl';J.export(Pos(0,0,-J.BOTTOM)*c,path)
    print(json.dumps(dict(checks=checks,params=PARAMS,sha256=hashlib.sha256(path.read_bytes()).hexdigest()),indent=2))

if __name__=='__main__':main()
