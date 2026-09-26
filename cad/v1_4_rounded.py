"""V1.4 look trial: v1.3 with the lid's top outer edge and LCD window edge
rounded. Base, caps and every fit surface unchanged. Rows V1.4-* in MEASUREMENTS.
"""
import base64
import hashlib
import json
import tempfile
from pathlib import Path
from build123d import Pos, Rot, Compound, fillet, export_step
import v1_3_short_end as W
V,T,S=W.V,W.T,W.S
M,P,J,L1=W.M,W.P,W.J,W.L1
ROOT=W.ROOT
REV='v1.4'
OUT=ROOT/'renders'/REV
STL=ROOT/'stl'/REV
TOP_R=3.0  # V1.4-TOP-R: outer top perimeter = wall thickness (review 3; was 1.5, 2.5)
WINDOW_IN=1.0  # V1.4-WINDOW-IN: each side; opening 0.4 over glass -> 0.6 onto its black border
GLASS_GAP=.3  # V1.4-GLASS-GAP: bezel underside above the glass top (S3)
WINDOW_EDGE_R=1.2  # V1.4-WINDOW-R (review 2 on; review 1 was 0.7; larger fails with TOP_R 3)

def top_face(l):
    return max((f for f in l.faces() if abs(f.center().Z-S.TOP)<1e-6 and f.normal_at().Z>.9),key=lambda f:f.area)

def window_wire(face):
    # The LCD window is the largest opening in the top face.
    return max(face.inner_wires(),key=lambda w:w.bounding_box().size.X*w.bounding_box().size.Y)

def narrow_window(old):
    # Bezel ring over the glass edge, down to GLASS_GAP above the glass so the
    # 1.2 mm window rounding has depth; the recess outside the ring stays.
    bb=window_wire(top_face(old)).bounding_box()
    ring=M.rbox(bb.min.X,bb.max.X,bb.min.Y,bb.max.Y,P.S3+GLASS_GAP,S.TOP,P.WINDOW_R)-M.rbox(
        bb.min.X+WINDOW_IN,bb.max.X-WINDOW_IN,bb.min.Y+WINDOW_IN,bb.max.Y-WINDOW_IN,P.S3+GLASS_GAP-P.TOOL_EXT,S.TOP+P.TOOL_EXT,P.WINDOW_R)
    return old+ring,ring

def lid():
    old,_=V.lid()
    old,_=narrow_window(old)
    f=top_face(old)
    l=fillet(f.outer_wire().edges(),TOP_R)
    f=top_face(l)
    return fillet(window_wire(f).edges(),WINDOW_EDGE_R),old

def main():
    OUT.mkdir(parents=True,exist_ok=True);STL.mkdir(parents=True,exist_ok=True)
    W.shorten()
    l,narrowed=lid();b,*_=V.base();caps=T.buttons()
    old,_=V.lid();_,ring=narrow_window(old)
    gx,gy=M.GLASS_C;bb=window_wire(top_face(narrowed)).bounding_box()
    cap,_=V.L3.J2.cap();placed_cap=Pos(*M.JOY_C,L1.LIP_TOP-J.BOTTOM-J.FLANGE_T)*cap
    checks={}
    def check(name,ok):checks[name]=bool(ok)
    check('lid_valid_single_solid',l.is_valid and len(l.solids())==1)
    check('only_adds_window_ring',V.volume(l-old-ring)<1e-5 and V.volume(ring)>1)
    check('rounding_only_removes_material',V.volume(l-narrowed)<1e-5 and V.volume(narrowed-l)>1)
    over=[gx-P.S2/2-bb.min.X,bb.max.X-(gx+P.S2/2),gy-P.S1/2-bb.min.Y,bb.max.Y-(gy+P.S1/2)]
    check('window_covers_glass_edge_0_6_each_side',all(abs(v+(WINDOW_IN-P.WINDOW_CLEAR))<1e-3 for v in over))
    # v1.3's short USB end already disagrees with the model board datum, so
    # check only the new ring, at the model and at the held (pushed) position.
    sight=M.rbox(bb.min.X+P.EPS,bb.max.X-P.EPS,bb.min.Y+P.EPS,bb.max.Y-P.EPS,P.S3,S.TOP+P.TOOL_EXT,P.WINDOW_R)
    check('window_open_down_to_glass',J.overlap(l,sight)<1e-5 and bb.size.X>20 and bb.size.Y>20)
    check('ring_clears_glass_and_hat',J.overlap(ring,M.hat())<1e-5 and J.overlap(ring,Pos(0,M.IY1-P.L1-.02,0)*M.hat())<1e-5)
    below=M.box(S.X0-1,S.X1+1,S.Y0-1,S.Y1+1,M.Z_BOTTOM-1,S.TOP-max(TOP_R,WINDOW_EDGE_R)-P.EPS)
    check('lid_unchanged_below_rounding',V.same(l & below,old & below))
    check('lid_height_unchanged',abs(l.bounding_box().max.Z-S.TOP)<1e-6)
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp)/'base.stl';J.export(V.origin(b),path)
        check('base_byte_identical_to_v1_3',path.read_bytes()==(ROOT/'stl/current/base.stl').read_bytes())
    check('fully_closed_no_shell_overlap',J.overlap(b,l)<1e-5)
    check('buttons_clear_lid',J.overlap(caps,l)<1e-5)
    check('joystick_cap_clear_at_rest',J.overlap(l,placed_cap)<1e-5)
    check('joystick_cap_retained_on_pull',J.overlap(Pos(0,0,L1.UNDER-L1.LIP_TOP+.1)*placed_cap,l)>1e-5)
    printed=V.origin(Rot(180,0,0)*l)
    J.export(printed,STL/'lid-face-down.stl')
    report=dict(revision=REV,checks=checks,passed=all(checks.values()),top_edge_radius=TOP_R,window_in_each_side=WINDOW_IN,window_over_glass_each_side=WINDOW_IN-P.WINDOW_CLEAR,window_edge_radius=WINDOW_EDGE_R,
        base='unchanged v1.3 (stl/current/base.stl)',caps='unchanged',physical_fit_confirmed=False,print_sent=False,
        notes=['Look trial for review; not printed.','Lid prints face down, so both roundings start at the bed: the first layers overhang. Needs a slice check; a 45 degree chamfer is the fallback.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
    if not report['passed']:raise SystemExit('Validation failed')
    view={n:fn() for n,(fn,color) in V.V.PARTS.items()};view['base']=b;view['lid']=l;view['button_caps']=caps;view['joystick_cap']=placed_cap
    export_step(Compound(children=list(view.values())),str(OUT/'assembly.step'))
    packed=[]
    with tempfile.TemporaryDirectory() as tmp:
        for name,s in view.items():
            path=Path(tmp)/(name+'.stl');J.export(s,path);bb=s.bounding_box()
            packed.append(dict(name=name,color=V.V.PARTS[name][1],stl=base64.b64encode(path.read_bytes()).decode(),bbox=[*tuple(bb.min),*tuple(bb.max)]))
    info=dict(commit=REV+' rounded edges',case_mm=[round(S.X1-S.X0,2),round(S.Y1-S.Y0,2),round(S.TOP-M.Z_BOTTOM,2)],split_z=S.SEAM,assumptions=['v1.3 fit, unchanged.','Top outer edge rounded '+str(TOP_R)+'mm.','LCD window edge rounded '+str(WINDOW_EDGE_R)+'mm.','Window 1mm smaller each side, covers glass border.','Look trial, not printed.'])
    html=(ROOT/'cad/viewer_template.html').read_text().replace('/*__PARTS__*/','const PARTS = '+json.dumps(packed)+';').replace('/*__INFO__*/','const INFO = '+json.dumps(info)+';').replace('V3 review · NOT APPROVED FOR PRINT','V1.4 · ROUNDED EDGES · REVIEW').replace('V3 Case Review — Not Approved for Print','V1.4 rounded edges')
    (OUT/'viewer.html').write_text(html);(ROOT/'renders/viewer.html').write_text(html)
    sources=[Path(__file__),*[ROOT/'cad'/n for n in ('v1_3_short_end.py','v1_production.py','s2_tight_base.py','s1_strong_shell.py','l4_alignment.py','l3_shifted_hole.py','j3_low_lid.py','joystick_j2.py','v3_flat.py','v3_fit.py','joystick_test.py','model.py','params.py')]]
    outputs=[*sorted(STL.glob('*.stl')),OUT/'assembly.step',OUT/'validation.json',OUT/'viewer.html']
    (OUT/'manifest.json').write_text(json.dumps(dict(revision=REV,print_sent=False,slice_verified=False,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}),indent=2)+'\n')

if __name__=='__main__':main()
