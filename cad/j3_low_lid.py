"""Original J3/L1 trial. Historical builders/artifacts remain unchanged."""
import base64
import hashlib
import json
import math
import tempfile
from pathlib import Path
from build123d import Pos, Rot, Sphere, Cylinder, Compound, export_step
import v3_flat as F
import joystick_test as J
M,P,V=F.M,F.P,F.V
ROOT=J.ROOT
OUT=ROOT/'renders/j3-low-lid'
STL=ROOT/'stl/j3-low-lid'
DIAM,DEPTH,SQUARE_DEPTH=3.5,1.1,2.0  # J3-SOCKET
TOP,UNDER=4.2,3.5  # L1-FACE
LIP_TOP=P.S3+.4  # J3-LIP: estimate only, not measured seating

def cap():
    blank=J.cylinder(J.NECK,J.BOTTOM,J.BALL_Z)+J.cylinder(J.FLANGE,J.BOTTOM,J.BOTTOM+J.FLANGE_T)
    blank+=Pos(0,0,J.BALL_Z)*Sphere(J.BALL/2)
    half=J.SOCKET/2
    cavity=J.cylinder(DIAM,J.BOTTOM-P.TOOL_EXT,J.BOTTOM+DEPTH)
    cavity+=M.box(-half,half,-half,half,J.BOTTOM+DEPTH-P.EPS,J.BOTTOM+DEPTH+SQUARE_DEPTH)
    return blank-cavity,blank

def lid():
    old=F.lid()
    shape=old & M.box(M.X0-1,M.X1+1,M.Y0-1,M.Y1+1,-P.TOOL_EXT,TOP)
    # Lower the pocket roof without changing the opening, skirt or snap datum.
    x,y=M.JOY_C;gx,gy=M.GLASS_C
    fill=Pos(x,y,(UNDER+TOP)/2)*Cylinder(V.JOY_POCKET/2,TOP-UNDER)
    clip=M.box(M.X0,M.X1,gy+P.S1/2+P.WINDOW_CLEAR+P.JOY_SCREEN_WEB,M.Y1,UNDER,TOP)
    shape+=fill & clip
    shape-=Pos(x,y,TOP/2)*Cylinder(J.HOLE/2,TOP+2*P.TOOL_EXT)
    return shape,old

def main():
    OUT.mkdir(parents=True,exist_ok=True);STL.mkdir(parents=True,exist_ok=True)
    c,blank=cap();l,old=lid()
    placed=Pos(*M.JOY_C,LIP_TOP-J.BOTTOM-J.FLANGE_T)*c
    checks={
        'lid_valid_single_solid':l.is_valid and len(l.solids())==1,
        'cap_valid_single_solid':c.is_valid and len(c.solids())==1,
        'socket_volume':abs(blank.volume-c.volume-(math.pi*(DIAM/2)**2*DEPTH+J.SOCKET**2*SQUARE_DEPTH))<1e-5,
        'button_roof_at_least_0_6':TOP-V.BUTTON_POCKET>=.6,
        'ball_passes_hole_lip_does_not':J.BALL<J.HOLE<J.FLANGE,
        'estimated_resting_cap_clear':J.overlap(placed,l)<1e-5,
        'lip_retained_on_pull':J.overlap(Pos(0,0,UNDER-LIP_TOP+.1)*placed,l)>1e-5,
        'same_skirt_and_snaps':True,
    }
    region=M.box(M.X0-1,M.X1+1,M.Y0-1,M.Y1+1,-P.TOOL_EXT,0)
    checks['same_skirt_and_snaps']=abs((l & region).volume-(old & region).volume)<1e-5 and J.overlap(l & region,old & region)>0
    faces=[f for f in l.faces() if abs(f.bounding_box().size.Z)<1e-6 and f.normal_at().Z>.99 and f.center().Z>0]
    checks['flat_exterior']=all(abs(f.center().Z-TOP)<1e-5 for f in faces)
    for i in range(9):
        checks['buttons_press_'+str(i)]=J.overlap(l,Pos(0,0,-P.B6*i/8)*V.buttons())<1e-5
    assert all(checks.values()),checks
    report=dict(checks=checks,face_z=TOP,screen_recess=TOP-P.S3,joystick_roof_z=UNDER,estimated_lip_z=LIP_TOP,estimated_rest_gap=UNDER-LIP_TOP,button_roof=TOP-V.BUTTON_POCKET,
        socket=dict(diameter=DIAM,round_depth=DEPTH,square_width=J.SOCKET,square_depth=SQUARE_DEPTH),
        limitations=['Lip height is user visual estimate; new seating and full motion need physical testing.','Hardware body height/pivot guesses are not evidence against observed seating.','Hole centre unchanged: prior photo direction lacks measured offset.','Existing blue tape proxy clearance remains unresolved.','Operator must preview support-free slicing before start.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    flipped=Rot(180,0,0)*l;bb=flipped.bounding_box()
    printed_lid=Pos(-bb.min.X,-bb.min.Y,-bb.min.Z)*flipped
    printed_cap=Pos(J.FLANGE/2,J.FLANGE/2,-J.BOTTOM)*c
    plate=Compound(children=[printed_lid,Pos(M.X1-M.X0+5,0,0)*printed_cap])  # L1-PLATE
    for name,shape in [('lid-face-down',printed_lid),('joystick-j3',printed_cap),('lid-and-joystick',plate)]:
        J.export(shape,STL/(name+'.stl'))
    parts={n:fn() for n,(fn,color) in V.PARTS.items()}
    parts['lid']=l;parts['joystick_cap']=placed
    export_step(Compound(children=list(parts.values())),str(OUT/'assembly.step'))
    packed=[]
    with tempfile.TemporaryDirectory() as tmp:
        for name,shape in parts.items():
            path=Path(tmp)/(name+'.stl');J.export(shape,path);bb=shape.bounding_box()
            packed.append(dict(name=name,color=V.PARTS[name][1],stl=base64.b64encode(path.read_bytes()).decode(),bbox=[*tuple(bb.min),*tuple(bb.max)]))
    info=dict(commit='J3 / L1 height trial',case_mm=[M.X1-M.X0,M.Y1-M.Y0,TOP-M.Z_BOTTOM],split_z=0,assumptions=['Face lowered 0.90 mm; screen recess 2.15 mm.','Joysticks shown at estimated lip height, not confirmed seated position.','Socket 3.50 diameter by 1.10 deep, then 2.01 square by 2.00 deep.','Print lid FACE DOWN, joystick flange DOWN; no supports or raft.','Reuse base and buttons. Physical motion test required.'])
    html=(ROOT/'cad/viewer_template.html').read_text().replace('/*__PARTS__*/','const PARTS = '+json.dumps(packed)+';').replace('/*__INFO__*/','const INFO = '+json.dumps(info)+';').replace('V3 review · NOT APPROVED FOR PRINT','J3 / L1 · PHYSICAL FIT TRIAL')
    (OUT/'viewer.html').write_text(html);(ROOT/'renders/viewer.html').write_text(html)
    outputs=[*STL.glob('*.stl'),OUT/'validation.json',OUT/'assembly.step',OUT/'viewer.html']
    sources=[Path(__file__),ROOT/'cad/v3_flat.py',ROOT/'cad/v3_fit.py',ROOT/'cad/joystick_test.py',ROOT/'cad/model.py',ROOT/'cad/params.py']
    (OUT/'manifest.json').write_text(json.dumps(dict(revision='J3-L1',supports=False,raft=False,slice_verified=False,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}),indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
