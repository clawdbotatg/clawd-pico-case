"""S1 original lower-seam shell: continuous walls, hidden detents, one pry.
Design dimensions documented in MEASUREMENTS S1-*; L4 controls retained.
"""
import base64
import hashlib
import json
import tempfile
from pathlib import Path
from build123d import Pos, Rot, Cylinder, Axis, fillet, export_step, Compound
import l4_alignment as L4
M,P,V,J,L1=L4.M,L4.P,L4.V,L4.J,L4.L1
ROOT=J.ROOT
OUT=ROOT/'renders/s1-strong-shell'
STL=ROOT/'stl/s1-strong-shell'
TOP=L1.TOP  # S1-FACE
SEAM=M.Z_BOTTOM+(TOP-M.Z_BOTTOM)/3  # S1-SPLIT
WALL=3.0; EXTRA=WALL-P.WALL  # S1-WALL
X0,X1,Y0,Y1=M.X0-EXTRA,M.X1+EXTRA,M.Y0-EXTRA,M.Y1+EXTRA
R=P.CORNER_R+EXTRA
LAP,SKIN,GAP,AXIAL=3.0,1.4,.2,.2  # S1-JOINT
SNAP_W,SNAP_T,SNAP_D,SNAP_Z=6.,1.2,.35,SEAM+1.5  # S1-SNAP
RECESS,END_CLEAR,Z_CLEAR=.35,.3,.15  # S1-RECESS
RAIL_GAP=.25  # S1-SUPPORT

def outer(z0,z1,inset=0):
    return M.rbox(X0+inset,X1-inset,Y0+inset,Y1-inset,z0,z1,R-inset)

def cavity(z0,z1):
    return M.rbox(M.IX0,M.IX1,M.IY0,M.IY1,z0,z1,P.POCKET_R)

def prism_region(z0,z1):
    return M.box(X0-P.TOOL_EXT,X1+P.TOOL_EXT,Y0-P.TOOL_EXT,Y1+P.TOOL_EXT,z0,z1)

def pry():
    cut=M.box(X0-P.TOOL_EXT,X0+P.PRY_DEPTH,M.CY-P.PRY_W/2,M.CY+P.PRY_W/2,SEAM-P.PRY_H/2,SEAM+P.PRY_H/2)
    return fillet(cut.edges().filter_by(Axis.X),P.PRY_R)

def lid():
    old,_=L4.lid()
    # Discard all old skirt slots and snaps. Solid ring also fills their small
    # remnants above z0; the control geometry inward of the wall is untouched.
    face=old & prism_region(0,TOP+P.TOOL_EXT)
    wall=outer(SEAM,TOP)-cavity(SEAM-P.TOOL_EXT,TOP+P.TOOL_EXT)
    l=face+wall
    l-=outer(SEAM-P.TOOL_EXT,SEAM+LAP+AXIAL,SKIN)
    # Blind pockets cut from inside; never through the external wall.
    for yc in (M.CY-P.L1/4,M.CY+P.L1/4):
        for xa,xb in ((X0+SKIN-RECESS,X0+SKIN+P.EPS),(X1-SKIN-P.EPS,X1-SKIN+RECESS)):
            l-=M.box(xa,xb,yc-SNAP_W/2-END_CLEAR,yc+SNAP_W/2+END_CLEAR,SNAP_Z-SNAP_T/2-Z_CLEAR,SNAP_Z+SNAP_T/2+Z_CLEAR)
    return l-pry()

def base():
    b=outer(M.Z_BOTTOM,SEAM)-cavity(M.Z_FLOOR_TOP,SEAM+P.TOOL_EXT)
    tongue=outer(SEAM-P.EPS,SEAM+LAP,SKIN+GAP)-cavity(SEAM-P.TOOL_EXT,SEAM+LAP+P.TOOL_EXT)
    b+=tongue
    # Symmetric ramps release by modest wall flex; no through-slots.
    xl,xr=X0+SKIN+GAP,X1-SKIN-GAP
    for yc in (M.CY-P.L1/4,M.CY+P.L1/4):
        b+=M.wedge_x([(xl+P.EPS,SNAP_Z-SNAP_T/2),(xl-SNAP_D,SNAP_Z),(xl+P.EPS,SNAP_Z+SNAP_T/2)],yc-SNAP_W/2,yc+SNAP_W/2)
        b+=M.wedge_x([(xr-P.EPS,SNAP_Z-SNAP_T/2),(xr+SNAP_D,SNAP_Z),(xr-P.EPS,SNAP_Z+SNAP_T/2)],yc-SNAP_W/2,yc+SNAP_W/2)
    # Base carries PCB supports above the seam; independent of removable top.
    left=M.PICO_CX-P.P2/2-P.CLEAR;right=M.PICO_CX+P.P2/2+P.CLEAR
    for xa,xb in ((M.IX0+RAIL_GAP,left),(right,M.IX1-RAIL_GAP)):
        b+=M.box(xa,xb,M.IY0+RAIL_GAP,M.IY1-RAIL_GAP,M.Z_FLOOR_TOP-P.EPS,M.Z_LCD_BACK-P.SHELF_GAP)
    # Exact USB aperture location/size; deeper outside counterbore compensates
    # outward wall thickening without moving the plug seating plane.
    b-=M.box(M.PICO_CX-M.USB_HALF_W,M.PICO_CX+M.USB_HALF_W,M.IY1-P.TOOL_EXT,Y1+P.TOOL_EXT,M.USB_Z0,M.USB_Z1)
    zm=(M.USB_Z0+M.USB_Z1)/2
    recess=M.box(M.PICO_CX-P.PLUG_W/2,M.PICO_CX+P.PLUG_W/2,M.Y1-P.PLUG_RECESS,Y1+P.TOOL_EXT,zm-P.PLUG_H/2,zm+P.PLUG_H/2)
    b-=fillet(recess.edges().filter_by(Axis.Y),P.PLUG_R)
    b-=Pos(*M.ACCESS_C,(M.Z_BOTTOM+M.Z_FLOOR_TOP)/2)*Cylinder(P.ACCESS_D/2,P.FLOOR+2*P.TOOL_EXT)
    return b-pry()

def main():
    OUT.mkdir(parents=True,exist_ok=True);STL.mkdir(parents=True,exist_ok=True)
    l,b=lid(),base();old,_=L4.lid()
    checks={}
    def check(name,ok):checks[name]=bool(ok)
    def equal(a,b):return L4.L3.volume(a-b)<1e-5 and L4.L3.volume(b-a)<1e-5
    for name,s in [('lid',l),('base',b)]:check(name+'_valid_single_solid',s.is_valid and len(s.solids())==1)
    check('no_shell_overlap',J.overlap(l,b)<1e-5)
    check('two_thirds_visible_top',abs((TOP-SEAM)/(TOP-M.Z_BOTTOM)-2/3)<1e-6)
    check('one_third_visible_base',abs((SEAM-M.Z_BOTTOM)/(TOP-M.Z_BOTTOM)-1/3)<1e-6)
    inner=cavity(0,TOP+P.TOOL_EXT)
    check('controls_unchanged_from_L4',equal(l & inner,old & inner))
    check('buttons_clear',J.overlap(l,V.buttons())<1e-5)
    check('hat_clear',J.overlap(l+b,M.hat())<1e-5)
    check('pico_clear',J.overlap(l+b,M.pico())<1e-5)
    check('detents_resist_lifting',J.overlap(Pos(0,0,.6)*l,b)>1e-5)
    usb=M.box(M.PICO_CX-M.USB_HALF_W,M.PICO_CX+M.USB_HALF_W,M.IY1,Y1,M.USB_Z0,M.USB_Z1)
    check('USB_aperture_clear',J.overlap(b+l,usb)<1e-5)
    access=Pos(*M.ACCESS_C,(M.Z_BOTTOM+M.Z_FLOOR_TOP)/2)*Cylinder(P.ACCESS_D/2,P.FLOOR)
    check('reset_access_clear',J.overlap(b+l,access)<1e-5)
    check('single_pry_open',J.overlap(l+b,pry())<1e-5)
    skin=outer(SEAM,TOP)-outer(SEAM-P.TOOL_EXT,TOP+P.TOOL_EXT,SKIN-RECESS)
    check('exterior_skin_continuous_except_pry',L4.L3.volume((skin-pry())-l)<1e-5)
    # Board-loaded base approaches top until deliberate snap engagement.
    assembly_motion=[]
    for dz in (0,1,3,6,12,20,30):
        overlap=J.overlap(Pos(0,0,dz)*l,M.hat()+M.pico()+V.buttons())
        assembly_motion.append(dict(lid_lift=dz,hardware_overlap_mm3=overlap))
        check('lid_hardware_approach_'+str(dz),overlap<1e-5)
    report=dict(checks=checks,passed=all(checks.values()),seam_z=SEAM,visible_top_height=TOP-SEAM,visible_base_height=SEAM-M.Z_BOTTOM,outer_size=[X1-X0,Y1-Y0,TOP-M.Z_BOTTOM],wall_mm=WALL,joint_overlap=LAP,socket_skin=SKIN,minimum_skin_at_catches=SKIN-RECESS,nominal_detent_flex=SNAP_D-GAP,assembly_motion=assembly_motion,
        physical_fit_confirmed=False,limitations=['New joint retention, removal force and wall strength need physical tests.','L4 opening adjustment not yet physically verified.','USB-first separate-Pico insertion still needs a physical assembly test.','Tall base support rails and no-support slicing need operator review.','Blue tape proxy remains unverified, not included in clearance passes.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)
    if not report['passed']:raise SystemExit('Structural/clearance checks failed; no print export')
    for name,s in [('lid-face-down',Rot(180,0,0)*l),('base-floor-down',b)]:
        bb=s.bounding_box();s=Pos(-bb.min.X,-bb.min.Y,-bb.min.Z)*s
        J.export(s,STL/(name+'.stl'))
    parts={n:fn() for n,(fn,color) in V.PARTS.items()};parts['lid']=l;parts['base']=b
    cap,_=L4.L3.J2.cap();parts['joystick_cap']=Pos(*M.JOY_C,L1.LIP_TOP-J.BOTTOM-J.FLANGE_T)*cap
    export_step(Compound(children=list(parts.values())),str(OUT/'assembly.step'))
    packed=[]
    with tempfile.TemporaryDirectory() as tmp:
        for name,s in parts.items():
            file=Path(tmp)/(name+'.stl');J.export(s,file);bb=s.bounding_box()
            packed.append(dict(name=name,color=V.PARTS[name][1],stl=base64.b64encode(file.read_bytes()).decode(),bbox=[*tuple(bb.min),*tuple(bb.max)]))
    info=dict(commit='S1 strong shell / low seam',case_mm=[round(X1-X0,2),round(Y1-Y0,2),round(TOP-M.Z_BOTTOM,2)],split_z=SEAM,assumptions=['Visible top 2/3, base 1/3. Matching NEW pair required.','3mm continuous walls; hidden catches, no exterior clip slots; one pry notch.','L4 joystick opening retained; roof and control heights unchanged.','New base carries tall PCB support rails; original USB/reset location.','Top face DOWN, base floor DOWN, no supports planned. Not sent.','Joint force, stiffness, slicing and physical assembly unverified.'])
    html=(ROOT/'cad/viewer_template.html').read_text().replace('/*__PARTS__*/','const PARTS = '+json.dumps(packed)+';').replace('/*__INFO__*/','const INFO = '+json.dumps(info)+';').replace('V3 review · NOT APPROVED FOR PRINT','S1 · LOWER SEAM / STRONGER WALLS').replace('V3 Case Review — Not Approved for Print','S1 strong shell review')
    (OUT/'viewer.html').write_text(html);(ROOT/'renders/viewer.html').write_text(html)
    sources=[Path(__file__),*[ROOT/'cad'/n for n in ('l4_alignment.py','l3_shifted_hole.py','j3_low_lid.py','joystick_j2.py','v3_flat.py','v3_fit.py','joystick_test.py','model.py','params.py')]]
    outputs=[*STL.glob('*.stl'),OUT/'assembly.step',OUT/'validation.json',OUT/'viewer.html']
    (OUT/'manifest.json').write_text(json.dumps(dict(revision='S1',print_sent=False,slice_verified=False,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}),indent=2)+'\n')

if __name__=='__main__':main()
