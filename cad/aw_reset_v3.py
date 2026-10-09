"""RESET button v3, final (Austin, 2026-10-09): the 3-notch v3 test cap,
0.90 shorter than v2 (2.80 total), without the test notches.
Replaces stl/aw2/reset-button.stl. Run: .venv/bin/python cad/aw_reset_v3.py
"""
import hashlib
import aw_reset_v2 as V2
import aw_reset_v3_test as T
M,R=V2.M,V2.R

CUT=T.CUTS[2]  # AW-RESET-V3: Austin picked the 0.90 cap
OUT=V2.OUT

if __name__=='__main__':
    c=V2.cap()-M.box(-5,5,-5,5,R.INSIDE+R.PROUD[0]-CUT,10)
    assert c.is_valid and len(c.solids())==1
    V2.J.export(c,OUT);print(round(c.bounding_box().size.Z,2),hashlib.sha256(OUT.read_bytes()).hexdigest())
