"""L2: translate L1 roof 1mm, preserve thickness; exact J2 reprint.
User explicitly authorizes a physical trial despite predicted button overlap.
"""
import base64
import hashlib
import json
import tempfile
from pathlib import Path
from build123d import Pos, Rot, Compound, export_step
import j3_low_lid as L1
import joystick_j2 as J2
M,P,V,J=L1.M,L1.P,L1.V,L1.J
ROOT=J.ROOT
OUT=ROOT/'renders/l2-j2'
STL=ROOT/'stl/l2-j2'
DROP=1.0  # L2-DROP
TOP=L1.TOP-DROP  # L2-RESULT
JOIN=P.S3+P.GLASS_CLEAR  # L2-JOIN

def region(z0,z1):
    return M.box(M.X0-P.TOOL_EXT,M.X1+P.TOOL_EXT,M.Y0-P.TOOL_EXT,M.Y1+P.TOOL_EXT,z0,z1)

def lid():
    old,_=L1.lid()
    upper=old & region(JOIN,L1.TOP+P.TOOL_EXT)
    lower=old & region(-P.TONGUE_H-P.TOOL_EXT,JOIN)
    return lower + Pos(0,0,-DROP)*upper,old

def difference(a,b):
    return sum(s.volume for s in (a-b).solids())

def main():
    OUT.mkdir(parents=True,exist_ok=True);STL.mkdir(parents=True,exist_ok=True)
    l,old=lid();c,_=J2.cap()
    below=region(-P.TONGUE_H-P.TOOL_EXT,0)
    # Roof comparison isolates above the preserved lower wall join.
    upper=region(JOIN+P.EPS,TOP+P.TOOL_EXT)
    translated=Pos(0,0,-DROP)*old
    checks={
        'lid_valid_single_solid':l.is_valid and len(l.solids())==1,
        'face_exactly_1mm_lower':abs(l.bounding_box().max.Z-TOP)<1e-6,
        'full_skirt_unchanged':difference(l & below,old & below)<1e-6 and difference(old & below,l & below)<1e-6,
        'upper_roof_translated_not_thinned':difference(l & upper,translated & upper)<1e-6 and difference(translated & upper,l & upper)<1e-6,
        'joystick_valid_single_solid':c.is_valid and len(c.solids())==1,
    }
    printed_cap=Pos(0,0,-J.BOTTOM)*c
    cap_path=STL/'joystick-j2.stl';J.export(printed_cap,cap_path)
    original=ROOT/'stl/joystick-j2/joystick-j2-stepped-socket.stl'
    checks['j2_byte_identical']=cap_path.read_bytes()==original.read_bytes()
    faces=[f for f in l.faces() if abs(f.bounding_box().size.Z)<1e-6 and f.normal_at().Z>.99 and f.center().Z>JOIN]
    checks['flat_outer_face']=bool(faces) and all(abs(f.center().Z-TOP)<1e-5 for f in faces)
    assert all(checks.values()),checks
    flipped=Rot(180,0,0)*l;bb=flipped.bounding_box()
    printed_lid=Pos(-bb.min.X,-bb.min.Y,-bb.min.Z)*flipped
    plate=Compound(children=[printed_lid,Pos(M.X1-M.X0+5+J.FLANGE/2,J.FLANGE/2,0)*printed_cap])  # L1-PLATE
    J.export(printed_lid,STL/'lid-face-down.stl')
    J.export(plate,STL/'l2-lid-and-j2.stl')
    parts={n:fn() for n,(fn,color) in V.PARTS.items()}
    parts['lid']=l
    parts['joystick_cap']=Pos(*M.JOY_C,L1.LIP_TOP-J.BOTTOM-J.FLANGE_T)*c
    report=dict(structural_checks=checks,physical_fit_confirmed=False,user_authorized_interference_trial=True,
        face_z=TOP,screen_recess=TOP-P.S3,button_underside=V.BUTTON_POCKET-DROP,button_roof=L1.TOP-V.BUTTON_POCKET,
        joystick_underside=L1.UNDER-DROP,joystick_roof=L1.TOP-L1.UNDER,
        diagnostic_overlap_mm3={name:J.overlap(l,shape) for name,shape in parts.items() if name!='lid'},
        limitations=['Predicted button overlap accepted by user for physical test. Do not force assembly.','Joystick seated height in viewer remains earlier estimate, not new measurement.','Actual full motion and slicing require physical/operator checks.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    export_step(l,str(OUT/'lid.step'))
    packed=[]
    with tempfile.TemporaryDirectory() as tmp:
        for name,shape in parts.items():
            path=Path(tmp)/(name+'.stl');J.export(shape,path);bb=shape.bounding_box()
            packed.append(dict(name=name,color=V.PARTS[name][1],stl=base64.b64encode(path.read_bytes()).decode(),bbox=[*tuple(bb.min),*tuple(bb.max)]))
    info=dict(commit='L2 / unchanged J2 fit trial',case_mm=[round(M.X1-M.X0,2),round(M.Y1-M.Y0,2),round(TOP-M.Z_BOTTOM,2)],split_z=0,assumptions=['Whole roof lowered 1.00 mm from L1, thickness retained.','Screen recess 1.15 mm. Same base and buttons.','Exact J2 reprint; NOT J3.','CAD predicts button overlap; Austin explicitly requests physical trial. Do not force.','Lid FACE DOWN, joystick flange DOWN; supports/raft OFF.'])
    html=(ROOT/'cad/viewer_template.html').read_text().replace('/*__PARTS__*/','const PARTS = '+json.dumps(packed)+';').replace('/*__INFO__*/','const INFO = '+json.dumps(info)+';').replace('V3 review · NOT APPROVED FOR PRINT','L2 / J2 · USER-AUTHORIZED FIT TRIAL').replace('V3 Case Review — Not Approved for Print','L2 / J2 physical fit trial')
    (OUT/'viewer.html').write_text(html);(ROOT/'renders/viewer.html').write_text(html)
    sources=[Path(__file__),ROOT/'cad/j3_low_lid.py',ROOT/'cad/joystick_j2.py',ROOT/'cad/v3_flat.py',ROOT/'cad/v3_fit.py',ROOT/'cad/joystick_test.py',ROOT/'cad/model.py',ROOT/'cad/params.py']
    outputs=[*STL.glob('*.stl'),OUT/'validation.json',OUT/'lid.step',OUT/'viewer.html']
    (OUT/'manifest.json').write_text(json.dumps(dict(revision='L2-J2',slice_verified=False,supports=False,raft=False,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}),indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
