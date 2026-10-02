"""Promote the best tested version to stl/current/ (stable paths for printing).
CURRENT names the revision; parts are byte-copied from their tested exports
and a full seven-part set plate is built from the same source.
History: v1.3 (2026-09-26 morning), v1.5 (2026-09-26 evening), v1.5 + J14-2
joystick (2026-09-30), v1.7 lid + base + J14-2 (2026-09-30: v1.7 is what Austin
batch-prints, 'lid v1.7 x6'); J15 = J14-2 without the dots (same day); J22 = J21-1 without the dot (same day);
v1.9 lid (+0.3, screen gap filled, no logo) + J24-A joystick (2026-10-02).
"""
import hashlib
import json
import shutil
from build123d import Pos, Rot, Compound
import v1_5_tall as T5
import joystick_j24 as J24
import v1_9 as L9
import v1_7_lock as L7
W,V,J=T5.W,T5.V,T5.J
ROOT=T5.ROOT
CURRENT='v1.9+J24'  # Austin, 2026-09-26: "this is the latest version"; 2026-09-30: J14-2 "is the new joystick"
DIR=ROOT/'stl/current'
GAP=5.0  # V1-PLATE
# v1.9 lid, v1.7 base, J24-A joystick, original S2 buttons. Austin, 2026-10-02: "everything is good".
PARTS={'lid.stl':'stl/v1.9/lid-face-down.stl','base.stl':'stl/v1.7/base-floor-down.stl',
       'joystick.stl':'stl/v1.9/joystick-j24.stl','button.stl':'stl/v1.0/button-1.stl'}

def main():
    DIR.mkdir(parents=True,exist_ok=True)
    for name,src in PARTS.items():shutil.copyfile(ROOT/src,DIR/name)
    W.shorten()
    l=L9.lid();b,_=L7.base()  # W.shorten() above runs once
    lid,base=V.origin(Rot(180,0,0)*l),V.origin(b)
    cap=Pos(0,0,-J.BOTTOM)*J24.cap(True)
    caps=[V.origin(c) for c in V.T.buttons().solids()]
    for shape,name in ((lid,'lid.stl'),(base,'base.stl'),(cap,'joystick.stl'),(caps[0],'button.stl')):
        tmp=DIR/('check-'+name);J.export(shape,tmp)
        assert tmp.read_bytes()==(DIR/name).read_bytes(),name+' differs from tested export'
        tmp.unlink()
    lb=lid.bounding_box().size
    placed=[lid,Pos(lb.X+GAP,0,0)*base,Pos(J.FLANGE/2,lb.Y+GAP+J.FLANGE/2,0)*cap]
    x=J.FLANGE+GAP
    for c in caps:placed.append(Pos(x,lb.Y+GAP,0)*c);x+=c.bounding_box().size.X+GAP
    plate=Compound(children=placed)
    assert len(plate.solids())==7 and all(v<256 for v in tuple(plate.bounding_box().size))
    J.export(plate,DIR/'full-set.stl')
    files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(DIR.glob('*.stl'))}
    (DIR/'current.json').write_text(json.dumps(dict(revision=CURRENT,sources=PARTS,sha256=files,
        print=dict(material='PETG',layer_mm=0.16,walls=4,supports=False,raft=False,
            orientation='lid face down, base floor down, joystick and buttons flange down')),indent=2)+'\n')
    print(json.dumps(files,indent=2),[round(v,2) for v in tuple(plate.bounding_box().size)])

if __name__=='__main__':main()
