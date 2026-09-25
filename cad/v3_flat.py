"""V3-FLAT: raised uniform face, exported FACE DOWN. Existing caps/base reused."""
import base64
import hashlib
import json
from pathlib import Path
import tempfile
from build123d import Pos, Rot, Cylinder, Compound, export_step
import v3_fit as V
import joystick_test as J
M,P=V.M,V.P
ROOT=V.ROOT
OUT=ROOT/'renders/v3-flat'
STL=ROOT/'stl/v3-flat'

def lid():
    # V3-FLAT: fill all low outer regions to the established J1 roof height.
    shape=V.lid()+M.rbox(M.X0,M.X1,M.Y0,M.Y1,V.SCREEN_TOP-P.EPS,V.JOY_TOP,P.CORNER_R)
    gx,gy=M.GLASS_C;w=P.WINDOW_CLEAR
    shape-=M.rbox(gx-P.S2/2-w,gx+P.S2/2+w,gy-P.S1/2-w,gy+P.S1/2+w,
                  -P.TOOL_EXT,V.JOY_TOP+P.TOOL_EXT,P.WINDOW_R)
    bx0,bx1,by0,by1=V.button_bounds()
    shape-=M.rbox(bx0,bx1,by0,by1,-P.TOOL_EXT,V.BUTTON_POCKET,P.WINDOW_R)
    for x,y in M.BUTTONS:
        hx=P.CAP_W/2+P.CAP_HOLE_CLEAR;hy=P.CAP_D/2+P.CAP_HOLE_CLEAR
        shape-=M.rbox(x-hx,x+hx,y-hy,y+hy,V.BUTTON_POCKET-P.TOOL_EXT,
                      V.JOY_TOP+P.TOOL_EXT,P.CAP_R+P.CAP_HOLE_CLEAR)
    x,y=M.JOY_C
    pocket=Pos(x,y,(V.JOY_UNDER-P.TOOL_EXT)/2)*Cylinder(V.JOY_POCKET/2,V.JOY_UNDER+P.TOOL_EXT)
    clip=M.box(M.X0-P.TOOL_EXT,M.X1+P.TOOL_EXT,gy+P.S1/2+w+P.JOY_SCREEN_WEB,
                M.Y1+P.TOOL_EXT,-P.TOOL_EXT,V.JOY_UNDER+P.EPS)
    shape-=pocket & clip
    shape-=Pos(x,y,V.JOY_TOP/2)*Cylinder(J.HOLE/2,V.JOY_TOP+2*P.TOOL_EXT)
    return shape

def main():
    OUT.mkdir(parents=True,exist_ok=True);STL.mkdir(parents=True,exist_ok=True)
    parts={n:fn() for n,(fn,color) in V.PARTS.items()};parts['lid']=lid()
    audit=V.validate(parts,flat_face=True)
    shape=parts['lid']
    # All outward-facing horizontal surfaces must be on the same print plane.
    upfaces=[f for f in shape.faces() if abs(f.bounding_box().max.Z-f.bounding_box().min.Z)<1e-6 and f.normal_at().Z>.99]
    flat=all(abs(f.center().Z-V.JOY_TOP)<1e-5 for f in upfaces if f.center().Z>0)
    audit['checks'].append(dict(name='all outer positive-Z horizontal faces coplanar',passed=flat))
    audit['passed']=audit['passed'] and flat
    (OUT/'validation.json').write_text(json.dumps(audit,indent=2)+'\n')
    if not audit['passed']:raise SystemExit('Fit/flatness checks failed; no export')
    oriented=Rot(180,0,0)*shape;bb=oriented.bounding_box()
    oriented=Pos(-bb.min.X,-bb.min.Y,-bb.min.Z)*oriented
    J.export(oriented,STL/'v3-flat-lid-face-down.stl')
    export_step(shape,str(OUT/'lid.step'))
    packed=[]
    with tempfile.TemporaryDirectory() as tmp:
        for n,s in parts.items():
            p=Path(tmp)/(n+'.stl');J.export(s,p);bb=s.bounding_box()
            packed.append(dict(name=n,color=V.PARTS[n][1],stl=base64.b64encode(p.read_bytes()).decode(),bbox=[bb.min.X,bb.min.Y,bb.min.Z,bb.max.X,bb.max.Y,bb.max.Z]))
    info=dict(commit='v3-flat-face-down',case_mm=[round(M.X1-M.X0,2),round(M.Y1-M.Y0,2),round(V.JOY_TOP-M.Z_BOTTOM,2)],split_z=0,assumptions=[
        'CORRECTED LID ONLY. Whole face flat at z5.1; print FACE DOWN, NO supports/raft.',
        'Screen recess3.05mm explicitly accepted for this test; lower later after fitting.',
        'Reuse V3 base, V2 buttons and unchanged J1 joystick.',
        'Buttons remain1.3mm proud, .92mm at full press. Joystick roof unchanged.',
        'Inherited motion hypotheses still show16 contacts; hand-held J1 test moved freely.',
        'Slicer checks and rigid-lid fit still required.' ])
    html=(ROOT/'cad/viewer_template.html').read_text().replace('/*__PARTS__*/','const PARTS = '+json.dumps(packed)+';').replace('/*__INFO__*/','const INFO = '+json.dumps(info)+';').replace('V3 review · NOT APPROVED FOR PRINT','V3 flat face · FACE-DOWN PRINT').replace('V3 Case Review — Not Approved for Print','V3 flat-face correction')
    (OUT/'viewer.html').write_text(html);(ROOT/'renders/viewer.html').write_text(html)
    sources=[Path(__file__),ROOT/'cad/v3_fit.py',ROOT/'cad/model.py',ROOT/'cad/params.py',ROOT/'cad/joystick_test.py',ROOT/'cad/viewer_template.html']
    outputs=[STL/'v3-flat-lid-face-down.stl',OUT/'viewer.html',OUT/'validation.json',OUT/'lid.step']
    manifest=dict(revision='v3-flat',print_parts=['lid'],orientation='face down',supports=False,raft=False,slice_verified=False,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs})
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('PASS',len(audit['checks']),'checks; face-down lid exported',flush=True)

if __name__=='__main__':main()
