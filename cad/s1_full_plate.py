"""Package approved S1 shells + J2 + V2 buttons, without geometry changes."""
import hashlib
import itertools
import json
from pathlib import Path
from build123d import Pos, Rot, Compound
import s1_strong_shell as S
J,V=S.J,S.V
ROOT=S.ROOT
OUT=ROOT/'renders/s1-full-print'
STL=ROOT/'stl/s1-full-print'
GAP=5.0  # S1-PLATE

def origin(shape):
    bb=shape.bounding_box()
    return Pos(-bb.min.X,-bb.min.Y,-bb.min.Z)*shape

def main():
    OUT.mkdir(parents=True,exist_ok=True);STL.mkdir(parents=True,exist_ok=True)
    lid=origin(Rot(180,0,0)*S.lid());base=origin(S.base())
    cap,_=S.L4.L3.J2.cap();cap=Pos(0,0,-J.BOTTOM)*cap
    parts={'lid-face-down':lid,'base-floor-down':base,'joystick-j2':cap}
    for i,b in enumerate(V.buttons().solids(),1):parts['button-'+str(i)]=origin(b)
    for name,shape in parts.items():J.export(shape,STL/(name+'.stl'))
    checks={name+'_one_solid':shape.is_valid and len(shape.solids())==1 for name,shape in parts.items()}
    for name,source in [('lid-face-down',ROOT/'stl/s1-strong-shell/lid-face-down.stl'),('base-floor-down',ROOT/'stl/s1-strong-shell/base-floor-down.stl'),('joystick-j2',ROOT/'stl/joystick-j2/joystick-j2-stepped-socket.stl')]:
        checks[name+'_byte_identical']=(STL/(name+'.stl')).read_bytes()==source.read_bytes()
    width=lid.bounding_box().size.X;length=lid.bounding_box().size.Y
    placed=[lid,Pos(width+GAP,0,0)*base,Pos(J.FLANGE/2,length+GAP+J.FLANGE/2,0)*cap]
    cursor=J.FLANGE+GAP
    for i in range(1,5):
        button=parts['button-'+str(i)]
        placed.append(Pos(cursor,length+GAP,0)*button)
        cursor+=button.bounding_box().size.X+GAP
    plate=Compound(children=placed)
    checks['seven_parts']=len(plate.solids())==7
    def separated(a,b):
        aa,bb=a.bounding_box(),b.bounding_box()
        return aa.max.X<=bb.min.X or bb.max.X<=aa.min.X or aa.max.Y<=bb.min.Y or bb.max.Y<=aa.min.Y
    checks['no_part_overlap']=all(separated(a,b) for a,b in itertools.combinations(placed,2))
    checks['all_on_bed']=all(abs(p.bounding_box().min.Z)<1e-6 for p in placed)
    checks['fits_256mm_bed']=all(v<256 for v in tuple(plate.bounding_box().size))
    assert all(checks.values()),checks
    J.export(plate,STL/'s1-full-case-seven-parts.stl')
    report=dict(checks=checks,size_mm=list(plate.bounding_box().size),part_count=7,orientation='Lid exterior down; base floor down; joystick and buttons flange down',supports=False,raft=False,slice_verified=False,physical_fit_confirmed=False)
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    sources=[Path(__file__),ROOT/'cad/s1_strong_shell.py',ROOT/'cad/joystick_j2.py',ROOT/'cad/v3_fit.py']
    files=[*STL.glob('*.stl'),OUT/'validation.json']
    (OUT/'manifest.json').write_text(json.dumps(dict(source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}),indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
