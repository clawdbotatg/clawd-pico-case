"""V1.1: v1.0 plus a USB-end spacer so the boards cannot slide toward USB-C.
Austin: stack slides along the case, lines up best pushed toward the buttons,
~1.2 mm of play. Lid carries a chamfered lip between the rails; base carries
end stops on the rails. Rows V1.1-* in MEASUREMENTS.
"""
import base64
import hashlib
import itertools
import json
import tempfile
from pathlib import Path
from build123d import Pos, Rot, Plane, Polygon, Compound, extrude, export_step
import v1_production as V
T,S=V.T,V.S
M,P,J,L1=V.M,V.P,V.J,V.L1
ROOT=V.ROOT
OUT=ROOT/'renders/v1.1'
STL=ROOT/'stl/v1.1'
SPACER=1.0  # V1.1-SPACER: 1.2 felt, 0.2 left so the rigid PCB cannot bind
FACE=M.IY1-SPACER  # new USB-end stop face
RAIL_TOP=M.Z_LCD_BACK-P.SHELF_GAP
LEFT,RIGHT=M.PICO_CX-P.P2/2-P.CLEAR,M.PICO_CX+P.P2/2+P.CLEAR  # rail inner edges, as S1
STOP_TOP=-.3  # V1.1-STOP: below the LCD PCB front face (z0)
CHAMFER=SPACER  # V1.1-LIP: 45 degree roof so the face-down lid prints unsupported
GAP=5.0  # V1-PLATE

def wedge_y(pts_yz,x0,x1):
    return extrude(Plane.YZ.offset(x0)*Polygon(*pts_yz,align=None),x1-x0)

def lip():
    # Catches the LCD PCB edge (z -1.97..0) between the rails.
    return wedge_y([(FACE,RAIL_TOP),(M.IY1+P.EPS,RAIL_TOP),(M.IY1+P.EPS,CHAMFER),(FACE,0)],LEFT+S.RAIL_GAP,RIGHT-S.RAIL_GAP)

def stops():
    return Compound(children=[M.box(xa,xb,FACE,M.IY1-S.RAIL_GAP,RAIL_TOP-P.EPS,STOP_TOP) for xa,xb in ((M.IX0+S.RAIL_GAP,LEFT),(RIGHT,M.IX1-S.RAIL_GAP))])

def column(shape,z0=None,z1=S.TOP+P.TOOL_EXT):
    # Footprint prism: the lid drops straight down, so lid material under a
    # stop top, or base material over the lip bottom, would collide on the way.
    bb=shape.bounding_box();return M.box(bb.min.X,bb.max.X,bb.min.Y,bb.max.Y,bb.min.Z if z0 is None else z0,z1)

def main():
    OUT.mkdir(parents=True,exist_ok=True);STL.mkdir(parents=True,exist_ok=True)
    oldlid,_=V.lid();oldbase,*_=V.base();k=lip();st=stops()
    l=oldlid+k;b=oldbase+st;caps=T.buttons()
    cap,_=V.L3.J2.cap()
    checks={}
    def check(name,ok):checks[name]=bool(ok)
    check('lid_valid_single_solid',l.is_valid and len(l.solids())==1)
    check('base_valid_single_solid',b.is_valid and len(b.solids())==1)
    check('lid_only_adds_lip',V.volume(l-oldlid-k)<1e-5 and V.volume(oldlid-l)<1e-5 and V.volume(k-oldlid)>1)
    check('base_only_adds_stops',V.volume(b-oldbase-st)<1e-5 and V.volume(oldbase-b)<1e-5 and V.volume(st-oldbase)>1)
    check('spacer_face_at_1mm',abs(k.bounding_box().min.Y-FACE)<1e-6 and all(abs(s.bounding_box().min.Y-FACE)<1e-6 for s in st.solids()))
    check('fully_closed_no_shell_overlap',J.overlap(b,l)<1e-5)
    check('lid_lowers_past_base_stops',J.overlap(l,Compound(children=[column(s,M.Z_BOTTOM-P.TOOL_EXT,STOP_TOP) for s in st.solids()]))<1e-5)
    check('lip_lowers_past_base',J.overlap(b,column(k))<1e-5)
    check('catches_hold_after_0_06mm_lift',J.overlap(b,Pos(0,0,T.FREE_PLAY+.02)*l)>1e-5)
    # Held position: stack pushed away from USB-C until the PCB edge meets FACE.
    # The model's own button-end wall disagrees with Austin's felt play, so only
    # the spacer and USB-end features are checked against the held stack.
    held=FACE-P.L1-.02
    hw=Pos(0,held,0)*(M.hat()+M.pico())
    check('held_stack_clears_spacer',J.overlap(hw,k+st)<1e-5)
    check('spacer_stops_stack',J.overlap(Pos(0,.1,0)*hw,k)>1e-5 and J.overlap(Pos(0,.1,0)*hw,st)>1e-5)
    usb_end=M.box(S.X0,S.X1,40,S.Y1+P.TOOL_EXT,M.Z_BOTTOM,S.TOP)
    check('held_stack_clears_usb_end_of_case',J.overlap(hw & usb_end,l+b)<1e-5)
    held_cap=Pos(M.JOY_C[0],M.JOY_C[1]+held,L1.LIP_TOP-J.BOTTOM-J.FLANGE_T)*cap
    check('held_joystick_cap_clears_lip',J.overlap(held_cap,k)<1e-5)
    check('buttons_clear_lid',J.overlap(caps,l)<1e-5)
    parts={'lid-face-down':V.origin(Rot(180,0,0)*l),'base-floor-down':V.origin(b)}
    for name,shape in parts.items():J.export(shape,STL/(name+'.stl'))
    lb=parts['lid-face-down'].bounding_box().size
    placed=[parts['lid-face-down'],Pos(lb.X+GAP,0,0)*parts['base-floor-down']]
    plate=Compound(children=placed)
    check('plate_two_parts_on_bed',len(plate.solids())==2 and all(abs(p.bounding_box().min.Z)<1e-5 for p in placed))
    check('plate_parts_separate',J.overlap(*placed)<1e-5)
    report=dict(revision='v1.1',checks=checks,passed=all(checks.values()),spacer_mm=SPACER,stop_face_y=FACE,
        lip=dict(x=[LEFT+S.RAIL_GAP,RIGHT-S.RAIL_GAP],z=[RAIL_TOP,0],chamfer_to_z=CHAMFER),
        rail_stops=dict(z=[RAIL_TOP,STOP_TOP]),plate_mm=list(plate.bounding_box().size),physical_fit_confirmed=False,
        notes=['Austin felt ~1.2 mm play; CAD model shows 0.6. His reading is used.','1.0 mm spacer leaves ~0.2 mm so the board cannot jam.','Joystick/button/USB/reset openings unchanged from v1.0.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
    if not report['passed']:raise SystemExit('Validation failed')
    J.export(plate,STL/'v1.1-lid-and-base.stl')
    view={n:fn() for n,(fn,color) in V.V.PARTS.items()};view['base']=b;view['lid']=l;view['button_caps']=caps
    view['joystick_cap']=Pos(*M.JOY_C,L1.LIP_TOP-J.BOTTOM-J.FLANGE_T)*cap
    export_step(Compound(children=list(view.values())),str(OUT/'assembly.step'))
    packed=[]
    with tempfile.TemporaryDirectory() as tmp:
        for name,s in view.items():
            path=Path(tmp)/(name+'.stl');J.export(s,path);bb=s.bounding_box()
            packed.append(dict(name=name,color=V.V.PARTS[name][1],stl=base64.b64encode(path.read_bytes()).decode(),bbox=[*tuple(bb.min),*tuple(bb.max)]))
    info=dict(commit='v1.1 USB-end spacer',case_mm=[round(S.X1-S.X0,2),round(S.Y1-S.Y0,2),round(S.TOP-M.Z_BOTTOM,2)],split_z=S.SEAM,assumptions=['v1.0 plus 1.0mm USB-end spacer.','Lid lip between rails, base stops on rails.','Stops board sliding toward USB-C.','Not printed yet.'])
    html=(ROOT/'cad/viewer_template.html').read_text().replace('/*__PARTS__*/','const PARTS = '+json.dumps(packed)+';').replace('/*__INFO__*/','const INFO = '+json.dumps(info)+';').replace('V3 review · NOT APPROVED FOR PRINT','V1.1 · USB-END SPACER').replace('V3 Case Review — Not Approved for Print','V1.1 spacer case')
    (OUT/'viewer.html').write_text(html);(ROOT/'renders/viewer.html').write_text(html)
    sources=[Path(__file__),*[ROOT/'cad'/n for n in ('v1_production.py','s2_tight_base.py','s1_strong_shell.py','l4_alignment.py','l3_shifted_hole.py','j3_low_lid.py','joystick_j2.py','v3_flat.py','v3_fit.py','joystick_test.py','model.py','params.py')]]
    outputs=[*sorted(STL.glob('*.stl')),OUT/'assembly.step',OUT/'validation.json',OUT/'viewer.html']
    (OUT/'manifest.json').write_text(json.dumps(dict(revision='v1.1',supports=False,raft=False,slice_verified=False,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}),indent=2)+'\n')

if __name__=='__main__':main()
