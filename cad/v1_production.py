"""V1.0 production: S2 fit (S1 lid, S2 base, S2 buttons, J2) plus three
0.25 mm nudges from Austin's final physical test. Rows V1-* in MEASUREMENTS.
"""
import base64
import hashlib
import itertools
import json
import tempfile
from pathlib import Path
from build123d import Pos, Rot, Axis, Cylinder, Compound, fillet, export_step
import s2_tight_base as T
S=T.S
M,P,V,J,L1,L4=S.M,S.P,S.V,S.J,S.L1,S.L4
L3=L4.L3
ROOT=S.ROOT
OUT=ROOT/'renders/v1.0'
STL=ROOT/'stl/v1.0'
NUDGE=.25  # V1-NUDGE
JOY_DY=NUDGE  # V1-JOY: +y = toward USB-C end, away from the LCD
USB_DZ=NUDGE  # V1-USB: +z = toward the lid
RESET_DY=-NUDGE  # V1-RESET: -y = away from USB-C end, toward centre
GAP=5.0  # V1-PLATE

def joy_hole(dy,z0,z1):
    x,y=M.JOY_C
    return L3.tube(x+L4.DX,y+L4.DY+dy,z0,z1)

def usb_cut(dz):
    cut=M.box(M.PICO_CX-M.USB_HALF_W,M.PICO_CX+M.USB_HALF_W,M.IY1-P.TOOL_EXT,S.Y1+P.TOOL_EXT,M.USB_Z0+dz,M.USB_Z1+dz)
    zm=(M.USB_Z0+M.USB_Z1)/2+dz
    recess=M.box(M.PICO_CX-P.PLUG_W/2,M.PICO_CX+P.PLUG_W/2,M.Y1-P.PLUG_RECESS,S.Y1+P.TOOL_EXT,zm-P.PLUG_H/2,zm+P.PLUG_H/2)
    return cut+fillet(recess.edges().filter_by(Axis.Y),P.PLUG_R)

def reset_cut(dy,extra=P.TOOL_EXT):
    x,y=M.ACCESS_C
    return Pos(x,y+dy,(M.Z_BOTTOM+M.Z_FLOOR_TOP)/2)*Cylinder(P.ACCESS_D/2,P.FLOOR+2*extra)

def lid():
    old=S.lid()
    # Same method as L4: fill the old throat through the roof, cut the new one.
    return (old+joy_hole(0,L1.UNDER,L1.TOP))-joy_hole(JOY_DY,-P.TONGUE_H-P.TOOL_EXT,L1.TOP+P.TOOL_EXT),old

def base():
    old,_,_=T.base()
    wall=S.outer(M.Z_BOTTOM,S.SEAM)-S.cavity(M.Z_FLOOR_TOP,S.SEAM+P.TOOL_EXT)
    before=usb_cut(0)+reset_cut(0);after=usb_cut(USB_DZ)+reset_cut(RESET_DY)
    # Refill the S2 openings only inside the original wall/floor, then recut.
    return (old+(wall & before))-after,old,wall,before,after

def volume(shape):return T.volume(shape)
def same(a,b):return volume(a-b)<1e-5 and volume(b-a)<1e-5
def origin(shape):
    bb=shape.bounding_box();return Pos(-bb.min.X,-bb.min.Y,-bb.min.Z)*shape

def main():
    OUT.mkdir(parents=True,exist_ok=True);STL.mkdir(parents=True,exist_ok=True)
    l,oldlid=lid();b,oldbase,wall,before,after=base();caps=T.buttons()
    cap,_=L3.J2.cap();placed_cap=Pos(*M.JOY_C,L1.LIP_TOP-J.BOTTOM-J.FLANGE_T)*cap
    checks={}
    def check(name,ok):checks[name]=bool(ok)
    check('lid_valid_single_solid',l.is_valid and len(l.solids())==1)
    check('base_valid_single_solid',b.is_valid and len(b.solids())==1)
    throats=joy_hole(0,L1.UNDER,L1.TOP)+joy_hole(JOY_DY,L1.UNDER,L1.TOP)
    check('lid_changes_only_at_joystick_throat',volume((l-oldlid)-throats)<1e-5 and volume((oldlid-l)-throats)<1e-5)
    check('lid_really_changed',volume(l-oldlid)>1e-3 and volume(oldlid-l)>1e-3)
    check('joystick_throat_open_at_new_centre',J.overlap(l,joy_hole(JOY_DY,L1.UNDER,L1.TOP))<1e-5)
    check('joystick_cap_clear_at_rest',J.overlap(l,placed_cap)<1e-5)
    check('joystick_cap_retained_on_pull',J.overlap(Pos(0,0,L1.UNDER-L1.LIP_TOP+.1)*placed_cap,l)>1e-5)
    check('base_changes_only_at_usb_and_reset',volume((b-oldbase)-(before+after))<1e-5 and volume((oldbase-b)-(before+after))<1e-5)
    check('base_really_changed',volume(b-oldbase)>1e-3 and volume(oldbase-b)>1e-3)
    check('old_openings_refilled_in_wall_only',same((b & before)-after,(wall & before)-after))
    usb=M.box(M.PICO_CX-M.USB_HALF_W,M.PICO_CX+M.USB_HALF_W,M.IY1,S.Y1,M.USB_Z0+USB_DZ,M.USB_Z1+USB_DZ)
    check('usb_aperture_open_at_new_height',J.overlap(b+l,usb)<1e-5)
    check('usb_aperture_below_seam',M.USB_Z1+USB_DZ<S.SEAM and (M.USB_Z0+M.USB_Z1)/2+USB_DZ+P.PLUG_H/2<S.SEAM)
    check('reset_access_open_at_new_position',J.overlap(b,reset_cut(RESET_DY,0))<1e-5)
    check('hardware_clear',J.overlap(b+l,M.hat()+M.pico())<1e-5)
    check('fully_closed_no_shell_overlap',J.overlap(b,l)<1e-5)
    check('catches_hold_after_0_06mm_lift',J.overlap(b,Pos(0,0,T.FREE_PLAY+.02)*l)>1e-5)
    check('buttons_clear_lid',J.overlap(caps,l)<1e-5)
    for i,c in enumerate(caps.solids()):check('button_retained_'+str(i),J.overlap(Pos(0,0,.25)*c,l)>1e-5)
    for i in range(0,9,2):check('button_travel_'+str(i),J.overlap(Pos(0,0,-P.B6*i/8)*caps,l)<1e-5)
    # Print set: lid face down, base floor down, J2 and S2 caps unchanged.
    parts={'lid-face-down':origin(Rot(180,0,0)*l),'base-floor-down':origin(b),'joystick-j2':Pos(0,0,-J.BOTTOM)*cap}
    for i,c in enumerate(caps.solids(),1):parts['button-'+str(i)]=origin(c)
    for name,shape in parts.items():J.export(shape,STL/(name+'.stl'))
    check('joystick_identical_to_tested_J2',(STL/'joystick-j2.stl').read_bytes()==(ROOT/'stl/joystick-j2/joystick-j2-stepped-socket.stl').read_bytes())
    for i in range(1,5):check('button_'+str(i)+'_identical_to_tested_S2',(STL/('button-'+str(i)+'.stl')).read_bytes()==(ROOT/'stl/s2-tight-base'/('button-'+str(i)+'.stl')).read_bytes())
    lb=parts['lid-face-down'].bounding_box().size;bb=parts['base-floor-down'].bounding_box().size
    placed=[parts['lid-face-down'],Pos(lb.X+GAP,0,0)*parts['base-floor-down'],Pos(J.FLANGE/2,max(lb.Y,bb.Y)+GAP+J.FLANGE/2,0)*parts['joystick-j2']]
    x=J.FLANGE+GAP
    for i in range(1,5):
        c=parts['button-'+str(i)];placed.append(Pos(x,max(lb.Y,bb.Y)+GAP,0)*c);x+=c.bounding_box().size.X+GAP
    def apart(a,c):
        p,q=a.bounding_box(),c.bounding_box()
        return p.max.X<=q.min.X or q.max.X<=p.min.X or p.max.Y<=q.min.Y or q.max.Y<=p.min.Y
    plate=Compound(children=placed)
    check('plate_seven_parts',len(plate.solids())==7)
    check('plate_parts_separate',all(apart(a,c) for a,c in itertools.combinations(placed,2)))
    check('plate_all_on_bed',all(abs(p.bounding_box().min.Z)<1e-5 for p in placed))
    check('plate_fits_256_bed',all(v<256 for v in tuple(plate.bounding_box().size)))
    x,y=M.JOY_C
    report=dict(revision='v1.0',checks=checks,passed=all(checks.values()),
        joystick_hole_centre=[x+L4.DX,y+L4.DY+JOY_DY],joystick_hole_from_S1=[0,JOY_DY],
        usb_aperture_z=[M.USB_Z0+USB_DZ,M.USB_Z1+USB_DZ],usb_from_S1=USB_DZ,
        reset_centre=[M.ACCESS_C[0],M.ACCESS_C[1]+RESET_DY],reset_from_S1=[0,RESET_DY],
        case_mm=[S.X1-S.X0,S.Y1-S.Y0,S.TOP-M.Z_BOTTOM],plate_mm=list(plate.bounding_box().size),
        physical_fit_confirmed=False,
        notes=['S2 fit confirmed by Austin; v1.0 = S2 plus three 0.25 mm nudges, not printed.','Nudges are from hand feel and photos, not caliper readings.','PETG fit untested; first PETG set is the check.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
    if not report['passed']:raise SystemExit('Validation failed')
    J.export(plate,STL/'v1.0-full-set-seven-parts.stl')
    view={n:fn() for n,(fn,color) in V.PARTS.items()};view['base']=b;view['lid']=l;view['button_caps']=caps;view['joystick_cap']=placed_cap
    export_step(Compound(children=list(view.values())),str(OUT/'assembly.step'))
    packed=[]
    with tempfile.TemporaryDirectory() as tmp:
        for name,s in view.items():
            path=Path(tmp)/(name+'.stl');J.export(s,path);bb=s.bounding_box()
            packed.append(dict(name=name,color=V.PARTS[name][1],stl=base64.b64encode(path.read_bytes()).decode(),bbox=[*tuple(bb.min),*tuple(bb.max)]))
    info=dict(commit='v1.0 production',case_mm=[round(v,2) for v in report['case_mm']],split_z=S.SEAM,assumptions=['S2 fit plus three 0.25mm nudges.','Joystick hole toward USB-C, away from LCD.','USB-C opening up toward lid.','Reset hole away from USB-C.','Not printed. PETG fit untested.'])
    html=(ROOT/'cad/viewer_template.html').read_text().replace('/*__PARTS__*/','const PARTS = '+json.dumps(packed)+';').replace('/*__INFO__*/','const INFO = '+json.dumps(info)+';').replace('V3 review · NOT APPROVED FOR PRINT','V1.0 · PRODUCTION').replace('V3 Case Review — Not Approved for Print','V1.0 production case')
    (OUT/'viewer.html').write_text(html);(ROOT/'renders/viewer.html').write_text(html)
    sources=[Path(__file__),*[ROOT/'cad'/n for n in ('s2_tight_base.py','s1_strong_shell.py','l4_alignment.py','l3_shifted_hole.py','j3_low_lid.py','joystick_j2.py','v3_flat.py','v3_fit.py','joystick_test.py','model.py','params.py')]]
    outputs=[*sorted(STL.glob('*.stl')),OUT/'assembly.step',OUT/'validation.json',OUT/'viewer.html']
    (OUT/'manifest.json').write_text(json.dumps(dict(revision='v1.0',supports=False,raft=False,slice_verified=False,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}),indent=2)+'\n')

if __name__=='__main__':main()
