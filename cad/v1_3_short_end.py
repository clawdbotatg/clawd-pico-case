"""V1.3: v1.0 with the USB-C end wall moved 0.5 mm inward on lid and base.
No lip, no spacer: the case is 0.5 mm shorter. Replaces the v1.1/v1.2 spacer
trials (Austin, 2026-09-25). Rows V1.3-* in MEASUREMENTS.
Every openings/controls position is absolute and stays put; only the USB end
(outer face, inner face, corners, tongue/socket ends, rail ends, USB slot and
plug recess) moves, because they are all built from Y1/IY1.
"""
import base64
import hashlib
import json
import tempfile
from pathlib import Path
from build123d import Pos, Rot, Compound, export_step
import v1_production as V
T,S=V.T,V.S
M,P,J,L1=V.M,V.P,V.J,V.L1
ROOT=V.ROOT
REV='v1.3'
OUT=ROOT/'renders'/REV
STL=ROOT/'stl'/REV
SHORTEN=.5  # V1.3-SHORTEN: +y end wall inward
CHANGED_FROM_Y=51.0  # everything at y < this must be identical to v1.0
GAP=5.0  # V1-PLATE

def shorten():
    # All shell geometry reads these at call time; move the USB end only.
    M.Y1-=SHORTEN;M.IY1-=SHORTEN;S.Y1-=SHORTEN

def main():
    OUT.mkdir(parents=True,exist_ok=True);STL.mkdir(parents=True,exist_ok=True)
    oldlid,_=V.lid();oldbase,*_=V.base()
    shorten()
    l,_=V.lid();b,*_=V.base();caps=T.buttons()
    cap,_=V.L3.J2.cap();placed_cap=Pos(*M.JOY_C,L1.LIP_TOP-J.BOTTOM-J.FLANGE_T)*cap
    checks={}
    def check(name,ok):checks[name]=bool(ok)
    check('lid_valid_single_solid',l.is_valid and len(l.solids())==1)
    check('base_valid_single_solid',b.is_valid and len(b.solids())==1)
    for name,new,old in (('lid',l,oldlid),('base',b,oldbase)):
        bn,bo=new.bounding_box(),old.bounding_box()
        check(name+'_0_5mm_shorter',abs((bo.max.Y-bn.max.Y)-SHORTEN)<1e-6 and abs(bn.min.Y-bo.min.Y)<1e-6)
        keep=M.box(S.X0-P.TOOL_EXT,S.X1+P.TOOL_EXT,S.Y0-P.TOOL_EXT,CHANGED_FROM_Y,M.Z_BOTTOM-P.TOOL_EXT,S.TOP+P.TOOL_EXT)
        check(name+'_unchanged_below_y51',V.same(new & keep,old & keep))
    check('fully_closed_no_shell_overlap',J.overlap(b,l)<1e-5)
    check('catches_hold_after_0_06mm_lift',J.overlap(b,Pos(0,0,T.FREE_PLAY+.02)*l)>1e-5)
    def vol(a,c):
        try:return V.volume(a & c)
        except ValueError:return 0  # empty intersection
    check('rails_keep_gap_to_lid',vol(b,M.box(M.IX0,M.IX1,M.IY1-S.RAIL_GAP+P.EPS,M.IY1-P.EPS,S.SEAM+S.LAP+P.EPS,M.Z_LCD_BACK))<1e-5)
    usb=M.box(M.PICO_CX-M.USB_HALF_W,M.PICO_CX+M.USB_HALF_W,M.IY1,S.Y1,M.USB_Z0+V.USB_DZ,M.USB_Z1+V.USB_DZ)
    check('usb_aperture_open_through_new_wall',J.overlap(b+l,usb)<1e-5)
    check('reset_access_open',J.overlap(b,V.reset_cut(V.RESET_DY,0))<1e-5)
    check('joystick_throat_open',J.overlap(l,V.joy_hole(V.JOY_DY,L1.UNDER,L1.TOP))<1e-5)
    check('joystick_cap_clear_at_rest',J.overlap(l,placed_cap)<1e-5)
    check('joystick_cap_retained_on_pull',J.overlap(Pos(0,0,L1.UNDER-L1.LIP_TOP+.1)*placed_cap,l)>1e-5)
    check('buttons_clear_lid',J.overlap(caps,l)<1e-5)
    # Held position: stack pushed away from USB-C until the LCD PCB meets the
    # new wall. Model play (0.6) disagrees with Austin's felt play (~1.2), so
    # the USB end is checked against the held stack, not the model datum.
    held=M.IY1-P.L1-.02
    hw=Pos(0,held,0)*(M.hat()+M.pico())
    usb_end=M.box(S.X0,S.X1,40,S.Y1+P.TOOL_EXT,M.Z_BOTTOM,S.TOP)
    check('held_stack_clears_usb_end',J.overlap(hw & usb_end,l+b)<1e-5)
    check('usb_shell_reaches_new_slot',(hw & usb).bounding_box().max.Y>M.IY1)
    parts={'lid-face-down':V.origin(Rot(180,0,0)*l),'base-floor-down':V.origin(b)}
    for name,shape in parts.items():J.export(shape,STL/(name+'.stl'))
    lb=parts['lid-face-down'].bounding_box().size
    placed=[parts['lid-face-down'],Pos(lb.X+GAP,0,0)*parts['base-floor-down']]
    plate=Compound(children=placed)
    check('plate_two_parts_on_bed',len(plate.solids())==2 and all(abs(p.bounding_box().min.Z)<1e-5 for p in placed))
    check('plate_parts_separate',J.overlap(*placed)<1e-5)
    report=dict(revision=REV,checks=checks,passed=all(checks.values()),shorten_mm=SHORTEN,
        case_mm=[S.X1-S.X0,S.Y1-S.Y0,S.TOP-M.Z_BOTTOM],inner_usb_face_y=M.IY1,plate_mm=list(plate.bounding_box().size),physical_fit_confirmed=False,
        notes=['v1.0 with the USB end moved in 0.5 mm; v1.1/v1.2 spacers dropped.','Austin felt ~1.2 mm play; the v1.1 1.0 mm spacer was too much.','Caps unchanged: reuse v1.0 caps.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
    if not report['passed']:raise SystemExit('Validation failed')
    J.export(plate,STL/(REV+'-lid-and-base.stl'))
    view={n:fn() for n,(fn,color) in V.V.PARTS.items()};view['base']=b;view['lid']=l;view['button_caps']=caps;view['joystick_cap']=placed_cap
    export_step(Compound(children=list(view.values())),str(OUT/'assembly.step'))
    packed=[]
    with tempfile.TemporaryDirectory() as tmp:
        for name,s in view.items():
            path=Path(tmp)/(name+'.stl');J.export(s,path);bb=s.bounding_box()
            packed.append(dict(name=name,color=V.V.PARTS[name][1],stl=base64.b64encode(path.read_bytes()).decode(),bbox=[*tuple(bb.min),*tuple(bb.max)]))
    info=dict(commit=REV+' short USB end',case_mm=[round(v,2) for v in report['case_mm']],split_z=S.SEAM,assumptions=['v1.0 with USB-C end wall 0.5mm inward.','No lip, no spacer.','Lid and base both change.','Not printed yet.'])
    html=(ROOT/'cad/viewer_template.html').read_text().replace('/*__PARTS__*/','const PARTS = '+json.dumps(packed)+';').replace('/*__INFO__*/','const INFO = '+json.dumps(info)+';').replace('V3 review · NOT APPROVED FOR PRINT','V1.3 · USB END 0.5 MM IN').replace('V3 Case Review — Not Approved for Print','V1.3 short-end case')
    (OUT/'viewer.html').write_text(html);(ROOT/'renders/viewer.html').write_text(html)
    sources=[Path(__file__),*[ROOT/'cad'/n for n in ('v1_production.py','s2_tight_base.py','s1_strong_shell.py','l4_alignment.py','l3_shifted_hole.py','j3_low_lid.py','joystick_j2.py','v3_flat.py','v3_fit.py','joystick_test.py','model.py','params.py')]]
    outputs=[*sorted(STL.glob('*.stl')),OUT/'assembly.step',OUT/'validation.json',OUT/'viewer.html']
    (OUT/'manifest.json').write_text(json.dumps(dict(revision=REV,supports=False,raft=False,slice_verified=False,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}),indent=2)+'\n')

if __name__=='__main__':main()
