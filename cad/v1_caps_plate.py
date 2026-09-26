"""V1.0 caps-only plate: J2 joystick + two S2 buttons, unchanged v1.0 parts."""
import hashlib
import itertools
from build123d import Pos, Compound
import v1_production as V
J,T=V.J,V.T
STL=V.STL
GAP=5.0  # V1-PLATE

def main():
    cap,_=V.L3.J2.cap();cap=Pos(0,0,-J.BOTTOM)*cap
    buttons=[V.origin(c) for c in T.buttons().solids()][:2]
    placed=[Pos(J.FLANGE/2,J.FLANGE/2,0)*cap];x=J.FLANGE+GAP
    for b in buttons:placed.append(Pos(x,0,0)*b);x+=b.bounding_box().size.X+GAP
    plate=Compound(children=placed)
    assert len(plate.solids())==3
    assert all(abs(p.bounding_box().min.Z)<1e-5 for p in placed)
    assert all(T.volume(a & b)<1e-6 for a,b in itertools.combinations(placed,2))
    path=STL/'v1.0-joystick-and-two-buttons.stl';J.export(plate,path)
    print(path.relative_to(V.ROOT),hashlib.sha256(path.read_bytes()).hexdigest(),[round(v,2) for v in tuple(plate.bounding_box().size)])

if __name__=='__main__':main()
