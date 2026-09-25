"""V3 fitted shells: reuse physically printed V2 buttons and J1 cap.

Isolated revision builder. Does not overwrite historical print artifacts.
Dimensions: MEASUREMENTS V3-FIT, J1, D4/D5; hardware in params.py.
"""
import base64
import hashlib
import itertools
import json
import math
from pathlib import Path
import tempfile
from build123d import Pos, Rot, Axis, Cylinder, Compound, export_step
import model as M
import params as P
import joystick_test as J

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'renders/v3-fit'
STL=ROOT/'stl/v3-fit'
SCREEN_TOP=P.S3+1.0  # V3-FIT-LID
BUTTON_TOP=4.6  # V3-FIT-LID, printed V2 lid
BUTTON_FLANGE_T=.8  # V3-FIT-BUTTON, printed V2 caps
BUTTON_POCKET=P.B5+BUTTON_FLANGE_T+P.CAP_POCKET_CLEAR
JOY_UNDER, JOY_TOP=J.UNDER,J.UNDER+J.THICK  # V3-FIT-LID/J1
JOY_POCKET, JOY_OUTER=13.,15.8  # V3-FIT-LID

def button_bounds():
    return (min(x for x,y in M.BUTTONS)-P.CAP_FLANGE_W/2-P.POCKET_MARGIN,
            max(x for x,y in M.BUTTONS)+P.CAP_FLANGE_W/2+P.POCKET_MARGIN,
            min(y for x,y in M.BUTTONS)-P.CAP_FLANGE_D/2-P.POCKET_MARGIN,
            max(y for x,y in M.BUTTONS)+P.CAP_FLANGE_D/2+P.POCKET_MARGIN)

def buttons():
    parts=[]
    for x,y in M.BUTTONS:
        c=M.rbox(x-P.CAP_FLANGE_W/2,x+P.CAP_FLANGE_W/2,
                 y-P.CAP_FLANGE_D/2,y+P.CAP_FLANGE_D/2,
                 P.B5,P.B5+BUTTON_FLANGE_T,P.CAP_R)
        c+=M.rbox(x-P.CAP_W/2,x+P.CAP_W/2,y-P.CAP_D/2,y+P.CAP_D/2,
                  P.B5+BUTTON_FLANGE_T-P.EPS,BUTTON_TOP+P.CAP_PROUD,P.CAP_R)
        parts.append(c)
    return Compound(children=parts)

def joystick():
    return Pos(*M.JOY_C,0)*J.cap()

def base():
    # Closed V2-aligned port, original pry/reset; discard rejected D8 arm pocket.
    return M.base(rear_pocket=False)

def lid():
    x0,x1,y0,y1=M.X0,M.X1,M.Y0,M.Y1
    outer=M.rbox(x0,x1,y0,y1,-P.TONGUE_H,SCREEN_TOP,P.CORNER_R)
    cavity=M.rbox(x0+P.SKIRT,x1-P.SKIRT,y0+P.SKIRT,y1-P.SKIRT,
                  -P.TONGUE_H-P.TOOL_EXT,0,P.CORNER_R-P.SKIRT)
    ceiling=M.rbox(M.IX0,M.IX1,M.IY0,M.IY1,-P.TOOL_EXT,
                   P.S3+P.GLASS_CLEAR,P.CAVITY_R)
    l=outer-cavity-ceiling
    bx0,bx1,by0,by1=button_bounds()
    # Only the button-end deck keeps V2 height; screen side rails remain low.
    outline=M.rbox(x0,x1,y0,y1,SCREEN_TOP-P.EPS,BUTTON_TOP,P.CORNER_R)
    l+=outline & M.box(x0-P.TOOL_EXT,x1+P.TOOL_EXT,y0-P.TOOL_EXT,
                       by1+P.CAP_R,SCREEN_TOP-P.EPS,BUTTON_TOP)
    gx,gy=M.GLASS_C
    screen_end=gy+P.S1/2+P.WINDOW_CLEAR
    jx,jy=M.JOY_C
    front=screen_end
    keep=M.box(x0-P.TOOL_EXT,x1+P.TOOL_EXT,front,y1+P.TOOL_EXT,
               -P.TOOL_EXT,JOY_TOP+P.TOOL_EXT)
    l+=(Pos(jx,jy,(SCREEN_TOP-P.EPS+JOY_TOP)/2)*Cylinder(JOY_OUTER/2,JOY_TOP-SCREEN_TOP+P.EPS)) & keep
    # Corner contacts grow directly from surrounding walls, not isolated islands.
    for xa,xb in ((M.IX0-P.EPS,P.LID_PAD_INSET+P.LID_PAD),
                  (P.L2-P.LID_PAD_INSET-P.LID_PAD,M.IX1+P.EPS)):
        for ya,yb in ((M.IY0-P.EPS,P.LID_PAD_INSET+P.LID_PAD),
                      (P.L1-P.LID_PAD_INSET-P.LID_PAD,M.IY1+P.EPS)):
            l+=M.box(xa,xb,ya,yb,P.LID_PAD_GAP,P.S3+P.GLASS_CLEAR+P.EPS)
    zlo=P.SNAP_Z-P.SNAP_BUMP_T/2-P.SNAP_WIN_CLEAR
    zhi=P.SNAP_Z+P.SNAP_BUMP_T/2+P.SNAP_WIN_CLEAR
    for yc in (M.CY-P.L1/4,M.CY+P.L1/4):
        for xa,xb in ((x0-P.TOOL_EXT,x0+P.SKIRT+P.EPS),
                      (x1-P.SKIRT-P.EPS,x1+P.TOOL_EXT)):
            l-=M.box(xa,xb,yc-P.SNAP_LEN/2-P.SNAP_END_CLEAR,
                     yc+P.SNAP_LEN/2+P.SNAP_END_CLEAR,zlo,zhi)
            l-=M.box(xa,xb,yc-P.ARM_LEN/2,yc+P.ARM_LEN/2,
                     P.ARM_ROOF,P.ARM_ROOF+P.ARM_SLOT)
    w=P.WINDOW_CLEAR
    l-=M.rbox(gx-P.S2/2-w,gx+P.S2/2+w,gy-P.S1/2-w,screen_end,
              -P.TOOL_EXT,JOY_TOP+P.TOOL_EXT,P.WINDOW_R)
    l-=M.rbox(bx0,bx1,by0,by1,-P.TOOL_EXT,BUTTON_POCKET,P.WINDOW_R)
    for x,y in M.BUTTONS:
        hx=P.CAP_W/2+P.CAP_HOLE_CLEAR; hy=P.CAP_D/2+P.CAP_HOLE_CLEAR
        l-=M.rbox(x-hx,x+hx,y-hy,y+hy,BUTTON_POCKET-P.TOOL_EXT,
                  BUTTON_TOP+P.TOOL_EXT,P.CAP_R+P.CAP_HOLE_CLEAR)
    pocket=Pos(jx,jy,(JOY_UNDER-P.TOOL_EXT)/2)*Cylinder(JOY_POCKET/2,JOY_UNDER+P.TOOL_EXT)
    # Distinct clipping planes retain a continuous front wall, not an open slot
    # or a zero-thickness edge joining a hanging wall to the low deck.
    pocket_keep=M.box(x0-P.TOOL_EXT,x1+P.TOOL_EXT,front+P.JOY_SCREEN_WEB,y1+P.TOOL_EXT,
                      -P.TOOL_EXT,JOY_UNDER+P.EPS)
    l-=pocket & pocket_keep
    l-=Pos(jx,jy,JOY_TOP/2)*Cylinder(J.HOLE/2,JOY_TOP+2*P.TOOL_EXT)
    return l-M.pry_notches()

PARTS={'hat':(M.hat,'#1f5f7a'),'pico':(M.pico,'#d4667a'),
       'base':(base,'#c9c4b8'),'lid':(lid,'#e8e3d6'),
       'button_caps':(buttons,'#f0a030'),'joystick_cap':(joystick,'#f0a030')}

def validate(parts, flat_face=False):
    checks=[]
    def check(name,passed,value=None):
        checks.append(dict(name=name,passed=bool(passed),value=value))
        if not passed: print('FAIL',name,value,flush=True)
    def clear(name,a,b):
        v=J.overlap(a,b);check(name,v<1e-5,round(v,7))
    b,l,c=parts['base'],parts['lid'],parts['joystick_cap']
    for name in ('base','lid'):
        shape=parts[name];check(name+' valid single solid',shape.is_valid and len(shape.solids())==1)
        oriented=Rot(180,0,0)*shape if flat_face and name=='lid' else shape
        z=oriented.bounding_box().min.Z
        area=sum(f.area for f in oriented.faces() if abs(f.bounding_box().min.Z-z)<1e-5 and abs(f.bounding_box().max.Z-z)<1e-5)
        check(name+' face-down bed contact' if flat_face and name=='lid' else name+' upright bed contact',area>(300 if flat_face and name=='lid' else 50),area)
    for a,z in itertools.combinations(parts,2):clear(a+'/'+z,parts[a],parts[z])
    if flat_face:
        check('uniform raised face maximum',abs(l.bounding_box().max.Z-JOY_TOP)<1e-5)
        check('existing buttons protrude after full press',BUTTON_TOP+P.CAP_PROUD-P.B6>JOY_TOP,BUTTON_TOP+P.CAP_PROUD-P.B6-JOY_TOP)
    else:
        check('screen rim 1mm',abs(SCREEN_TOP-P.S3-1)<1e-5)
    check('lid no USB fin',abs(l.bounding_box().min.Z+P.TONGUE_H)<1e-5)
    check('snap catches on lift',J.overlap(b,Pos(0,0,P.SNAP_WIN_CLEAR+.1)*l)>1e-5)
    # Lid first passes ball; lip remains below roof and stops upward removal.
    for i in range(25):
        raised=Pos(0,0,i/2)*l
        clear('lid installation lift '+str(i/2),raised,c)
        clear('lid approach hardware '+str(i/2),raised,parts['hat']+parts['pico']+parts['button_caps'])
    check('joystick lip retained',J.overlap(Pos(0,0,.7)*c,l)>1e-5)
    fixed=parts['hat']
    for x,y in M.BUTTONS:
        fixed-=M.box(x-P.B4X/2,x+P.B4X/2,y-P.B4Y/2,y+P.B4Y/2,P.B3,P.B5+P.EPS)
    for i in range(9):
        pressed=Pos(0,0,-P.B6*i/8)*parts['button_caps']
        clear('V2 buttons press/lid '+str(i),pressed,l)
        clear('V2 buttons press/hardware '+str(i),pressed,fixed)
    check('V2 buttons retained',J.overlap(Pos(0,0,.25)*parts['button_caps'],l)>1e-5)
    for i,button in enumerate(parts['button_caps'].solids()):
        check('individual button retained '+str(i),J.overlap(Pos(0,0,.25)*button,l)>1e-5)
    jx,jy=M.JOY_C
    gauge=Pos(jx,jy,0)*J.gauge()
    pcb=M.box(0,P.L2,0,P.L1,-P.L3,0)
    fixedjoy=parts['hat']-M.box(jx-P.J4/2,jx+P.J4/2,jy-P.J4/2,jy+P.J4/2,P.J3,P.J6+P.EPS)
    motion=[]
    for seating,pivot,angle,az,press in itertools.product((0.,-.3),(0.,3.),(0,5,10),range(0,360,45),(0.,.3)):
        axis=Axis((jx,jy,pivot),(math.cos(math.radians(az)),math.sin(math.radians(az)),0))
        moved=Pos(0,0,-press)*(Pos(0,0,seating)*c).rotate(axis,angle)
        v=J.overlap(moved,l); old=J.overlap(moved,gauge)
        record=dict(seating=seating,pivot=pivot,angle=angle,azimuth=az,press=press,lid_mm3=round(v,6),J1_gauge_mm3=round(old,6),guessed_fixed_hardware_mm3=round(J.overlap(moved,fixedjoy),6))
        motion.append(record)
        check('no new motion interference '+str((seating,pivot,angle,az,press)),v<=old+1e-5,round(v-old,7))
        clear('joystick/base '+str((seating,pivot,angle,az,press)),moved,b)
        clear('joystick/PCB '+str((seating,pivot,angle,az,press)),moved,pcb)
    # USB uses precisely the recorded working V2 bounds; channel above is closed.
    usb=M.box(M.PICO_CX-M.USB_HALF_W,M.PICO_CX+M.USB_HALF_W,M.IY1,M.Y1,M.USB_Z0,M.USB_Z1)
    clear('USB opening remains clear',usb,b)
    wall=M.box(M.PICO_CX-1,M.PICO_CX+1,M.IY1+.1,M.Y1-P.PLUG_RECESS-.1,M.USB_Z1+.2,-P.TONGUE_H-.2)
    check('USB channel closed',abs((wall-b).volume)<1e-5)
    access=Pos(*M.ACCESS_C,(M.Z_BOTTOM+M.Z_FLOOR_TOP)/2)*Cylinder(P.ACCESS_D/2,P.FLOOR)
    clear('bottom access open',access,b)
    for side,xa,xb in [('left',M.X0-.2,M.X0+.7),('right',M.X1-.7,M.X1+.2)]:
        clear(side+' pry access',M.box(xa,xb,M.CY-2,M.CY+2,-P.TONGUE_H-.3,-P.TONGUE_H+.3),b+l)
    # Existing USB-first separate-Pico path, repeated with this base.
    py=M.USB_EDGE_Y+P.P11; pz=M.Z_USB_SHELL_BOT+P.P13/2
    pivot=Pos(M.PICO_CX,py,pz);unpivot=Pos(-M.PICO_CX,-py,-pz)
    for angle in range(0,-13,-2):clear('USB-first angle '+str(angle),pivot*Rot(angle,0,0)*unpivot*parts['pico'],b)
    tilted=pivot*Rot(-12,0,0)*unpivot*parts['pico']
    for n in range(7):clear('USB-first retreat '+str(n),Pos(0,-n*.3,0)*tilted,b)
    for z in (1,3,6,12,20,30):clear('USB-first lift '+str(z),Pos(0,-1.8,z)*tilted,b)
    return dict(passed=all(x['passed'] for x in checks),checks=checks,motion=motion,
                unresolved={'blue_flag_lid_mm3':J.overlap(M.fpc_tape(),l),
                            'limitations':['Actual seated height and travel unknown; J1 hand-held free motion is encouraging but not a rigid-lid test.','Inherited J1 10-degree lip contacts and guessed-body contacts remain diagnostics, not passes.','Slice review mandatory: face-down lid snap bridges.' if flat_face else 'Slice review mandatory: upright lid bridges/overhangs and narrow bed footprint.','USB-first assembly and snaps require bench test.']})

def main():
    OUT.mkdir(parents=True,exist_ok=True);STL.mkdir(parents=True,exist_ok=True)
    parts={n:fn() for n,(fn,color) in PARTS.items()}
    audit=validate(parts)
    (OUT/'validation.json').write_text(json.dumps(audit,indent=2)+'\n')
    if not audit['passed']:raise SystemExit('Failed fit checks; no new print files exported')
    placed=[]
    for n in ('base','lid'):
        shape=parts[n]; bb=shape.bounding_box()
        shape=Pos(-bb.min.X,-bb.min.Y,-bb.min.Z)*shape
        J.export(shape,STL/(n+'.stl'))
        placed.append(shape if n=='base' else Pos(M.X1-M.X0+5,0,0)*shape)
    J.export(Compound(children=placed),STL/'v3-shells-only.stl')
    export_step(Compound(children=list(parts.values())),str(OUT/'assembly.step'))
    packed=[]
    with tempfile.TemporaryDirectory() as tmp:
        for n,shape in parts.items():
            path=Path(tmp)/(n+'.stl');J.export(shape,path);bb=shape.bounding_box()
            packed.append(dict(name=n,color=PARTS[n][1],stl=base64.b64encode(path.read_bytes()).decode(),bbox=[bb.min.X,bb.min.Y,bb.min.Z,bb.max.X,bb.max.Y,bb.max.Z]))
    info=dict(commit='v3-fit-shells',case_mm=[round(v,2) for v in (M.X1-M.X0,M.Y1-M.Y0,JOY_TOP-M.Z_BOTTOM)],split_z=0,assumptions=[
        'PRINT ONLY BASE AND LID. Reuse printed V2 buttons and unchanged J1 joystick.',
        'Screen rim1mm above glass. Local joystick roof matches J1, not full-case raise.',
        'Closed V2-aligned USB aperture. No lid fin. Pry/reset retained.',
        'User reports full J1 hand-held motion. Inherited10-degree model contacts remain unresolved.',
        'Both shells upright. No supports/raft. Operator must check bridges before starting.',
        'USB-first insertion: Pico separately, then connect LCD. Test gently.',
        'Blue tape proxy and actual joystick seated travel remain uncertain.' ])
    html=(ROOT/'cad/viewer_template.html').read_text().replace('/*__PARTS__*/','const PARTS = '+json.dumps(packed)+';').replace('/*__INFO__*/','const INFO = '+json.dumps(info)+';').replace('V3 review · NOT APPROVED FOR PRINT','V3 fitted shells · SLICE CHECK REQUIRED').replace('V3 Case Review — Not Approved for Print','V3 fitted shells')
    (OUT/'viewer.html').write_text(html)
    (ROOT/'renders/viewer.html').write_text(html)
    manifest=dict(revision='v3-fit-shells',print_parts=['base','lid'],reuse=['prototype-v2 button caps','joystick-j1 cap'],slice_verified=False,
        source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),ROOT/'cad/model.py',ROOT/'cad/params.py',ROOT/'cad/joystick_test.py',ROOT/'cad/viewer_template.html']},
        files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [*STL.glob('*.stl'),OUT/'viewer.html',OUT/'validation.json',OUT/'assembly.step']})
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('PASS',len(audit['checks']),'required checks. Inherited lid contacts',sum(x['lid_mm3']>1e-5 for x in audit['motion']),flush=True)

if __name__=='__main__':main()
