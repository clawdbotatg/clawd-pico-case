"""L3: restore L1 height, shift only the round opening toward LCD 1mm."""
import base64
import hashlib
import json
import tempfile
from pathlib import Path
from build123d import Pos, Rot, Cylinder, export_step
import j3_low_lid as L1
import joystick_j2 as J2
M,P,V,J=L1.M,L1.P,L1.V,L1.J
ROOT=J.ROOT
OUT=ROOT/'renders/l3-shifted-hole'
STL=ROOT/'stl/l3-shifted-hole'
SHIFT=1.0  # L3-HOLE

def tube(x,y,z0,z1):
    return Pos(x,y,(z0+z1)/2)*Cylinder(J.HOLE/2,z1-z0)

def lid():
    old,_=L1.lid()
    x,y=M.JOY_C
    # Fill only the old throat through roof thickness, not the lip cavity.
    filled=old+tube(x,y,L1.UNDER,L1.TOP)
    new=filled-tube(x,y-SHIFT,-P.TONGUE_H-P.TOOL_EXT,L1.TOP+P.TOOL_EXT)
    return new,old

def volume(shape):return sum(s.volume for s in shape.solids())

def main():
    OUT.mkdir(parents=True,exist_ok=True);STL.mkdir(parents=True,exist_ok=True)
    l,old=lid();x,y=M.JOY_C
    below=M.box(M.X0-1,M.X1+1,M.Y0-1,M.Y1+1,-P.TONGUE_H-P.TOOL_EXT,L1.UNDER)
    target=tube(x,y-SHIFT,L1.UNDER,L1.TOP)
    repaired=tube(x,y,L1.UNDER,L1.TOP)-target
    checks={
        'valid_single_solid':l.is_valid and len(l.solids())==1,
        'restored_L1_height':abs(l.bounding_box().max.Z-L1.TOP)<1e-6,
        'same_full_skirt_height':abs(l.bounding_box().min.Z-old.bounding_box().min.Z)<1e-6,
        'pocket_and_lower_geometry_unchanged':volume((l & below)-(old & below))<1e-6 and volume((old & below)-(l & below))<1e-6,
        'new_8mm_hole_clear':J.overlap(l,target)<1e-6,
        'old_hole_crescent_filled':volume(repaired-l)<1e-6,
        'hole_closer_to_glass':abs(y-SHIFT-M.GLASS_C[1])<abs(y-M.GLASS_C[1]),
    }
    change_region=tube(x,y,L1.UNDER,L1.TOP)+target
    checks['only_hole_changed']=volume((l-old)-change_region)<1e-6 and volume((old-l)-change_region)<1e-6
    checks['existing_buttons_clear']=J.overlap(l,V.buttons())<1e-6
    assert all(checks.values()),checks
    flipped=Rot(180,0,0)*l;bb=flipped.bounding_box()
    printed=Pos(-bb.min.X,-bb.min.Y,-bb.min.Z)*flipped
    path=STL/'l3-lid-face-down.stl';J.export(printed,path)
    export_step(l,str(OUT/'lid.step'))
    report=dict(checks=checks,old_hole_center=list(M.JOY_C),new_hole_center=[x,y-SHIFT],diameter=J.HOLE,face_z=L1.TOP,joystick_underside=L1.UNDER,
        physical_fit_confirmed=False,limitations=['Hardware joystick datum is NOT changed from photos; only the lid aperture is corrected by user request.','Physical alignment, movement and closure need test.','Lip pocket unchanged; no hardware or button redesign.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    parts={n:fn() for n,(fn,color) in V.PARTS.items()};parts['lid']=l
    cap,_=J2.cap();parts['joystick_cap']=Pos(*M.JOY_C,L1.LIP_TOP-J.BOTTOM-J.FLANGE_T)*cap
    packed=[]
    with tempfile.TemporaryDirectory() as tmp:
        for name,shape in parts.items():
            file=Path(tmp)/(name+'.stl');J.export(shape,file);bb=shape.bounding_box()
            packed.append(dict(name=name,color=V.PARTS[name][1],stl=base64.b64encode(file.read_bytes()).decode(),bbox=[*tuple(bb.min),*tuple(bb.max)]))
    info=dict(commit='L3 shifted opening / L1 height',case_mm=[round(M.X1-M.X0,2),round(M.Y1-M.Y0,2),round(L1.TOP-M.Z_BOTTOM,2)],split_z=0,assumptions=['L1 taller lid restored; L2 failed physical closure.','Round opening shifted exactly 1mm toward LCD; diameter unchanged.','Only lid printed, face DOWN, no supports/raft.','Reuse base/buttons/J2. Hardware datum remains historical; photos correct opening only.','Physical alignment and motion require testing.'])
    html=(ROOT/'cad/viewer_template.html').read_text().replace('/*__PARTS__*/','const PARTS = '+json.dumps(packed)+';').replace('/*__INFO__*/','const INFO = '+json.dumps(info)+';').replace('V3 review · NOT APPROVED FOR PRINT','L3 · OPENING 1mm TOWARD LCD').replace('V3 Case Review — Not Approved for Print','L3 alignment trial')
    (OUT/'viewer.html').write_text(html);(ROOT/'renders/viewer.html').write_text(html)
    sources=[Path(__file__),ROOT/'cad/j3_low_lid.py',ROOT/'cad/joystick_j2.py',ROOT/'cad/v3_flat.py',ROOT/'cad/v3_fit.py',ROOT/'cad/joystick_test.py',ROOT/'cad/model.py',ROOT/'cad/params.py']
    outputs=[path,OUT/'lid.step',OUT/'validation.json',OUT/'viewer.html']
    (OUT/'manifest.json').write_text(json.dumps(dict(revision='L3',print_parts=['lid'],supports=False,raft=False,slice_verified=False,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}),indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
