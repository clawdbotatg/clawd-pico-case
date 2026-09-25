"""L4: halfway back from L3, slightly photo-up; original geometry only."""
import base64
import hashlib
import json
import tempfile
from pathlib import Path
from build123d import Pos, Rot, export_step
import l3_shifted_hole as L3
M,P,V,J,L1=L3.M,L3.P,L3.V,L3.J,L3.L1
ROOT=J.ROOT
OUT=ROOT/'renders/l4-alignment'
STL=ROOT/'stl/l4-alignment'
DX,DY=.30,-.50  # L4-OFFSET relative to original, not L3

def lid():
    old,_=L1.lid();x,y=M.JOY_C
    return (old+L3.tube(x,y,L1.UNDER,L1.TOP))-L3.tube(x+DX,y+DY,-P.TONGUE_H-P.TOOL_EXT,L1.TOP+P.TOOL_EXT),old

def main():
    OUT.mkdir(parents=True,exist_ok=True);STL.mkdir(parents=True,exist_ok=True)
    l,old=lid();x,y=M.JOY_C
    hole=L3.tube(x+DX,y+DY,L1.UNDER,L1.TOP)
    oldhole=L3.tube(x,y,L1.UNDER,L1.TOP)
    below=M.box(M.X0-1,M.X1+1,M.Y0-1,M.Y1+1,-P.TONGUE_H-P.TOOL_EXT,L1.UNDER)
    checks=dict(valid_single_solid=l.is_valid and len(l.solids())==1,
        height_unchanged=abs(l.bounding_box().max.Z-L1.TOP)<1e-6,
        lower_geometry_unchanged=L3.volume((l & below)-(old & below))<1e-6 and L3.volume((old & below)-(l & below))<1e-6,
        hole_clear=J.overlap(l,hole)<1e-6,
        old_crescent_filled=L3.volume((oldhole-hole)-l)<1e-6,
        only_aperture_changed=L3.volume((l-old)-(hole+oldhole))<1e-6 and L3.volume((old-l)-(hole+oldhole))<1e-6,
        buttons_clear=J.overlap(l,V.buttons())<1e-6)
    assert all(checks.values()),checks
    printed=Rot(180,0,0)*l;bb=printed.bounding_box()
    printed=Pos(-bb.min.X,-bb.min.Y,-bb.min.Z)*printed
    path=STL/'l4-lid-face-down.stl';J.export(printed,path)
    export_step(l,str(OUT/'lid.step'))
    report=dict(checks=checks,original_center=[x,y],L3_center=[x,y-1],L4_center=[x+DX,y+DY],delta_from_L3=[DX,DY+1],diameter=J.HOLE,face_z=L1.TOP,physical_fit_confirmed=False,print_sent=False,notes=['Photo-up amount 0.30mm is a trial choice, not measured.','Only aperture changed. Hardware datum, pocket and J2 unchanged.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    parts={n:fn() for n,(fn,color) in V.PARTS.items()};parts['lid']=l
    cap,_=L3.J2.cap();parts['joystick_cap']=Pos(*M.JOY_C,L1.LIP_TOP-J.BOTTOM-J.FLANGE_T)*cap
    packed=[]
    with tempfile.TemporaryDirectory() as tmp:
        for name,shape in parts.items():
            file=Path(tmp)/(name+'.stl');J.export(shape,file);bb=shape.bounding_box()
            packed.append(dict(name=name,color=V.PARTS[name][1],stl=base64.b64encode(file.read_bytes()).decode(),bbox=[*tuple(bb.min),*tuple(bb.max)]))
    info=dict(commit='L4 halfway back + photo-up',case_mm=[round(M.X1-M.X0,2),round(M.Y1-M.Y0,2),round(L1.TOP-M.Z_BOTTOM,2)],split_z=0,assumptions=['From L3: 0.50mm away from LCD and 0.30mm photo-up.','Same L1 height and 8mm aperture. Pocket unchanged.','Photo-up amount is a trial choice, not calibrated.','Lid only, exterior face DOWN, no supports/raft. Not sent.'])
    html=(ROOT/'cad/viewer_template.html').read_text().replace('/*__PARTS__*/','const PARTS = '+json.dumps(packed)+';').replace('/*__INFO__*/','const INFO = '+json.dumps(info)+';').replace('V3 review · NOT APPROVED FOR PRINT','L4 · HALFWAY BACK + PHOTO-UP').replace('V3 Case Review — Not Approved for Print','L4 alignment trial')
    (OUT/'viewer.html').write_text(html);(ROOT/'renders/viewer.html').write_text(html)
    sources=[Path(__file__),ROOT/'cad/l3_shifted_hole.py',ROOT/'cad/j3_low_lid.py',ROOT/'cad/joystick_j2.py',ROOT/'cad/v3_flat.py',ROOT/'cad/v3_fit.py',ROOT/'cad/joystick_test.py',ROOT/'cad/model.py',ROOT/'cad/params.py']
    outputs=[path,OUT/'lid.step',OUT/'validation.json',OUT/'viewer.html']
    (OUT/'manifest.json').write_text(json.dumps(dict(revision='L4',supports=False,raft=False,slice_verified=False,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}),indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
