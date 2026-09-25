"""S2: replacement base for existing S1 lid, four rounded V2-interface caps."""
import base64
import hashlib
import itertools
import json
import tempfile
from pathlib import Path
from build123d import Pos, Compound, fillet, export_step
import s1_strong_shell as S
M,P,V,J=S.M,S.P,S.V,S.J
ROOT=S.ROOT
OUT=ROOT/'renders/s2-tight-base'
STL=ROOT/'stl/s2-tight-base'
PROJECTION,FREE_PLAY,NOSE=.50,.04,.30  # S2-CATCH
BUTTON_TOP,TOP_R=6.90,1.20  # S2-BUTTON
GAP=5.0  # S2-PLATE
POCKET_BOTTOM=S.SNAP_Z-S.SNAP_T/2-S.Z_CLEAR
CATCH_BOTTOM=POCKET_BOTTOM+FREE_PLAY

def base():
    old=S.base();new=old
    xl,xr=S.X0+S.SKIN+S.GAP,S.X1-S.SKIN-S.GAP
    zones=[]
    for yc in (M.CY-P.L1/4,M.CY+P.L1/4):
        # Remove ONLY exterior protrusions, keep tongue wall/root untouched.
        for xa,xb in ((S.X0-P.TOOL_EXT,xl),(xr,S.X1+P.TOOL_EXT)):
            zone=M.box(xa,xb,yc-S.SNAP_W/2,yc+S.SNAP_W/2,S.SEAM,S.SEAM+S.LAP)
            new-=zone;zones.append(zone)
        z0,z1,z2=CATCH_BOTTOM,CATCH_BOTTOM+NOSE,S.SNAP_Z+S.SNAP_T/2
        new+=M.wedge_x([(xl+P.EPS,z0),(xl-PROJECTION,z0),(xl-PROJECTION,z1),(xl,z2),(xl+P.EPS,z2)],yc-S.SNAP_W/2,yc+S.SNAP_W/2)
        new+=M.wedge_x([(xr-P.EPS,z0),(xr+PROJECTION,z0),(xr+PROJECTION,z1),(xr,z2),(xr-P.EPS,z2)],yc-S.SNAP_W/2,yc+S.SNAP_W/2)
    return new,old,Compound(children=zones)

def buttons():
    parts=[]
    for x,y in M.BUTTONS:
        flange=M.rbox(x-P.CAP_FLANGE_W/2,x+P.CAP_FLANGE_W/2,y-P.CAP_FLANGE_D/2,y+P.CAP_FLANGE_D/2,P.B5,P.B5+V.BUTTON_FLANGE_T,P.CAP_R)
        post=M.rbox(x-P.CAP_W/2,x+P.CAP_W/2,y-P.CAP_D/2,y+P.CAP_D/2,P.B5+V.BUTTON_FLANGE_T-P.EPS,BUTTON_TOP,P.CAP_R)
        edges=[e for e in post.edges() if abs(e.bounding_box().min.Z-BUTTON_TOP)<1e-6 and abs(e.bounding_box().max.Z-BUTTON_TOP)<1e-6]
        parts.append(flange+fillet(edges,TOP_R))
    return Compound(children=parts)

def volume(shape):return 0 if shape is None else sum(s.volume for s in shape.solids())
def overlap(a,b):return volume(a & b)
def origin(shape):
    bb=shape.bounding_box();return Pos(-bb.min.X,-bb.min.Y,-bb.min.Z)*shape

def main():
    OUT.mkdir(parents=True,exist_ok=True);STL.mkdir(parents=True,exist_ok=True)
    b,old,zones=base();l=S.lid();caps=buttons();oldcaps=V.buttons()
    checks={}
    def check(name,ok):checks[name]=bool(ok)
    check('base_valid_single_solid',b.is_valid and len(b.solids())==1)
    check('buttons_four_valid_solids',caps.is_valid and len(caps.solids())==4)
    check('base_changes_only_at_catches',volume((b-old)-zones)<1e-5 and volume((old-b)-zones)<1e-5)
    check('fully_closed_no_shell_overlap',overlap(b,l)<1e-5)
    check('no_collision_before_nominal_free_play',overlap(b,Pos(0,0,FREE_PLAY/2)*l)<1e-5)
    check('catches_hold_after_0_06mm_lift',overlap(b,Pos(0,0,FREE_PLAY+.02)*l)>1e-5)
    check('old_base_has_more_axial_play',overlap(old,Pos(0,0,FREE_PLAY+.02)*l)<1e-5)
    check('hardware_clear',overlap(b,M.hat()+M.pico())<1e-5)
    lower=M.box(S.X0,S.X1,S.Y0,S.Y1,0,BUTTON_TOP-TOP_R-P.EPS)
    check('button_lower_interfaces_unchanged',volume((caps & lower)-(oldcaps & lower))<1e-5 and volume((oldcaps & lower)-(caps & lower))<1e-5)
    fixed=M.hat()
    for x,y in M.BUTTONS:
        fixed-=M.box(x-P.B4X/2,x+P.B4X/2,y-P.B4Y/2,y+P.B4Y/2,P.B3,P.B5+P.EPS)
    for i in range(9):
        pressed=Pos(0,0,-P.B6*i/8)*caps
        check('button_travel_lid_'+str(i),overlap(pressed,l)<1e-5)
        check('button_travel_fixed_hardware_'+str(i),overlap(pressed,fixed)<1e-5)
    for i,c in enumerate(caps.solids()):check('button_retained_'+str(i),overlap(Pos(0,0,.25)*c,l)>1e-5)
    # Verify retained lid is byte-identical, not emitted as a print request.
    from build123d import Rot
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp)/'lid.stl';J.export(origin(Rot(180,0,0)*l),path)
        check('existing_S1_lid_byte_identical',path.read_bytes()==(ROOT/'stl/s1-strong-shell/lid-face-down.stl').read_bytes())
    print_parts={'base-floor-down':origin(b)}
    for i,c in enumerate(caps.solids(),1):print_parts['button-'+str(i)]=origin(c)
    placed=[print_parts['base-floor-down']];x=0;y=S.Y1-S.Y0+GAP
    for i in range(1,5):
        c=print_parts['button-'+str(i)];placed.append(Pos(x,y,0)*c);x+=c.bounding_box().size.X+GAP
    plate=Compound(children=placed)
    check('five_print_parts',len(plate.solids())==5)
    check('parts_separate',all(overlap(a,b)<1e-5 for a,b in itertools.combinations(placed,2)))
    check('all_parts_on_bed',all(abs(p.bounding_box().min.Z)<1e-5 for p in placed))
    check('fits_bed',all(v<256 for v in tuple(plate.bounding_box().size)))
    report=dict(checks=checks,passed=all(checks.values()),nominal_axial_play=FREE_PLAY,nominal_radial_flex=PROJECTION-S.GAP,nominal_recess_spare=S.GAP+S.RECESS-PROJECTION,button_top=BUTTON_TOP,button_top_round_radius=TOP_R,size_mm=list(plate.bounding_box().size),physical_fit_confirmed=False,
        limitations=['0.04mm is CAD target, not achievable printer precision guarantee.','Stronger catches need force/release/fatigue test; use existing pry notch gently.','Short 0.5mm catch underside overhang needs support-free slice inspection.','Rounded top feel and actual full button travel need bench test.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
    if not report['passed']:raise SystemExit('Validation failed')
    for name,s in print_parts.items():J.export(s,STL/(name+'.stl'))
    J.export(plate,STL/'s2-base-and-four-buttons.stl')
    parts={n:fn() for n,(fn,color) in V.PARTS.items()};parts['base']=b;parts['lid']=l;parts['button_caps']=caps
    cap,_=S.L4.L3.J2.cap();parts['joystick_cap']=Pos(*M.JOY_C,S.L1.LIP_TOP-J.BOTTOM-J.FLANGE_T)*cap
    export_step(Compound(children=list(parts.values())),str(OUT/'assembly.step'))
    packed=[]
    with tempfile.TemporaryDirectory() as tmp:
        for name,s in parts.items():
            path=Path(tmp)/(name+'.stl');J.export(s,path);bb=s.bounding_box()
            packed.append(dict(name=name,color=V.PARTS[name][1],stl=base64.b64encode(path.read_bytes()).decode(),bbox=[*tuple(bb.min),*tuple(bb.max)]))
    info=dict(commit='S2 tighter base + rounded buttons',case_mm=[round(S.X1-S.X0,2),round(S.Y1-S.Y0,2),round(S.TOP-M.Z_BOTTOM,2)],split_z=S.SEAM,assumptions=['Print ONLY new base and four buttons. Reuse S1 lid and J2.','Flatter stronger catches: target 0.04mm axial play, not print precision guarantee.','Buttons 0.5mm taller with 1.2mm rounded top edges; same lower fit.','PLA, 0.16mm, 4 walls, no supports/raft.','Physical snap force and tactile feel require testing.'])
    html=(ROOT/'cad/viewer_template.html').read_text().replace('/*__PARTS__*/','const PARTS = '+json.dumps(packed)+';').replace('/*__INFO__*/','const INFO = '+json.dumps(info)+';').replace('V3 review · NOT APPROVED FOR PRINT','S2 · TIGHTER BASE / ROUNDED BUTTONS').replace('V3 Case Review — Not Approved for Print','S2 base and buttons')
    (OUT/'viewer.html').write_text(html);(ROOT/'renders/viewer.html').write_text(html)
    sources=[Path(__file__),*[ROOT/'cad'/n for n in ('s1_strong_shell.py','l4_alignment.py','l3_shifted_hole.py','j3_low_lid.py','joystick_j2.py','v3_flat.py','v3_fit.py','joystick_test.py','model.py','params.py')]]
    outputs=[*STL.glob('*.stl'),OUT/'assembly.step',OUT/'validation.json',OUT/'viewer.html']
    (OUT/'manifest.json').write_text(json.dumps(dict(revision='S2',supports=False,raft=False,slice_verified=False,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}),indent=2)+'\n')

if __name__=='__main__':main()
