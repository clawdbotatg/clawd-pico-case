"""V1.7: a case that will not pop open by accident. From v1.6 (lid) and v1.3
(base): (1) the lid's half of the pry notch is filled, leaving only the
base's 0.8 mm slot for a thumbnail or small tool; (2) the catches hook 0.5 mm
instead of 0.3, with a longer, gentler closing ramp and the same flat holding
face; (3) two more catches on the short ends (6 total). New base and lid.
Joystick J9 and buttons unchanged. Rows V1.7-* in MEASUREMENTS.
Run: .venv/bin/python cad/v1_7_lock.py
"""
import base64
import hashlib
import json
import tempfile
from pathlib import Path
from build123d import Pos, Rot, Compound, export_step
import v1_5_tall as T5
import v1_1_spacer as SP
R,W,V,T,S,M,P,J,L1=T5.R,T5.W,T5.V,T5.T,T5.S,T5.M,T5.P,T5.J,T5.L1
ROOT=T5.ROOT
REV='v1.7'
OUT=ROOT/'renders'/REV
STL=ROOT/'stl'/REV
HOOK=.5  # V1.7-HOOK: catch tip past the lid skirt face (was 0.30)
PROJ=S.GAP+HOOK  # from the tongue face
RECESS=HOOK+.05  # lid pocket depth: 0.05 spare past the tip; skin left 0.85
Z_HOLD=T.CATCH_BOTTOM  # flat holding face, unchanged height (0.04 play)
NOSE=T.NOSE
Z_RAMP_TOP=S.SEAM+2.4  # V1.7-RAMP: longer ramp, ~28 deg from vertical
POCKET=(T.POCKET_BOTTOM,Z_RAMP_TOP+S.Z_CLEAR)
LONG_Y=(M.CY-P.L1/4,M.CY+P.L1/4)  # existing catch centres
END_X=(M.CX,)  # V1.7-ENDS: one catch centred on each short end
W2=S.SNAP_W/2

def hook_profile(face,sgn):
    """(inward-coordinate, z) profile of one catch; sgn=+1 when outward is -coord."""
    o=-sgn
    return [(face-o*P.EPS,Z_HOLD),(face+o*PROJ,Z_HOLD),(face+o*PROJ,Z_HOLD+NOSE),(face,Z_RAMP_TOP),(face-o*P.EPS,Z_RAMP_TOP)]

def catches():
    xl,xr=S.X0+S.SKIN+S.GAP,S.X1-S.SKIN-S.GAP
    yl,yr=S.Y0+S.SKIN+S.GAP,S.Y1-S.SKIN-S.GAP
    out=[]
    for yc in LONG_Y:
        out.append(M.wedge_x(hook_profile(xl,1),yc-W2,yc+W2))
        out.append(M.wedge_x(hook_profile(xr,-1),yc-W2,yc+W2))
    for xc in END_X:
        for w in (SP.wedge_y(hook_profile(yl,1),xc-W2,xc+W2),SP.wedge_y(hook_profile(yr,-1),xc-W2,xc+W2)):
            # wedge_y extrudes along the face normal, which flips with the
            # profile's winding: pin each end catch to its x span.
            out.append(Pos(xc-W2-w.bounding_box().min.X,0,0)*w)
    return Compound(children=out)

def pockets():
    f0,f1=S.X0+S.SKIN,S.X1-S.SKIN
    g0,g1=S.Y0+S.SKIN,S.Y1-S.SKIN
    e=W2+S.END_CLEAR;z0,z1=POCKET
    out=[]
    for yc in LONG_Y:
        out+= [M.box(f0-RECESS,f0+P.EPS,yc-e,yc+e,z0,z1),M.box(f1-P.EPS,f1+RECESS,yc-e,yc+e,z0,z1)]
    for xc in END_X:
        out+= [M.box(xc-e,xc+e,g0-RECESS,g0+P.EPS,z0,z1),M.box(xc-e,xc+e,g1-P.EPS,g1+RECESS,z0,z1)]
    return Compound(children=out)

def old_pockets():
    f0,f1=S.X0+S.SKIN,S.X1-S.SKIN;e=W2+S.END_CLEAR
    z0,z1=S.SNAP_Z-S.SNAP_T/2-S.Z_CLEAR,S.SNAP_Z+S.SNAP_T/2+S.Z_CLEAR
    return Compound(children=[b for yc in LONG_Y for b in (M.box(f0-S.RECESS,f0,yc-e,yc+e,z0,z1),M.box(f1,f1+S.RECESS,yc-e,yc+e,z0,z1))])

def lid():
    R.TOP_BEVEL=True;R.HOLE_BEVEL=True;T5.JOY_BEVEL=True  # smooth window and joystick edges too
    l,_=T5.lid()  # v1.6 lid
    old=l
    l=l+old_pockets()
    l=l+(S.pry() & S.outer(S.SEAM,S.SEAM+P.PRY_H) & M.box(S.X0-1,S.X0+S.SKIN,S.Y0,S.Y1,S.SEAM,S.SEAM+P.PRY_H))
    for p in pockets().solids():l-=p
    return l,old

def base():
    b,*_=V.base()  # v1.3 base
    old=b
    xl,xr=S.X0+S.SKIN+S.GAP,S.X1-S.SKIN-S.GAP
    for yc in LONG_Y:  # strip the S2 catches (outside the tongue face only)
        for xa,xb in ((S.X0-P.TOOL_EXT,xl),(xr,S.X1+P.TOOL_EXT)):
            b-=M.box(xa,xb,yc-W2,yc+W2,S.SEAM+P.EPS,S.SEAM+S.LAP)
    for c in catches().solids():b+=c
    return b,old

def main():
    OUT.mkdir(parents=True,exist_ok=True);STL.mkdir(parents=True,exist_ok=True)
    W.shorten()
    l,l16=lid();b,b13=base();caps=T.buttons()
    placed=Pos(*M.JOY_C,L1.LIP_TOP+T5.J9_LIFT-J.BOTTOM-J.FLANGE_T)*T5.J9.cap()
    def vol(s):return sum(x.volume for x in s.solids())
    def diff(a,c):  # a-c that tolerates an empty a
        return a-c if a.solids() else a
    checks={}
    def check(n,ok):checks[n]=bool(ok)
    ribs=R.ribs();cat=catches();poc=pockets()
    check('lid_valid_single_solid',l.is_valid and len(l.solids())==1)
    check('base_valid_single_solid',b.is_valid and len(b.solids())==1)
    check('six_catches',len(cat.solids())==6)
    check('catches_where_intended',all(abs(c.bounding_box().size.X-S.SNAP_W)<1e-6 or abs(c.bounding_box().size.Y-S.SNAP_W)<1e-6 for c in cat.solids()) and sorted(round(c.bounding_box().center().X,2) for c in cat.solids() if abs(c.bounding_box().size.X-S.SNAP_W)<1e-6)==[round(M.CX,2)]*2)
    check('closed_contact_only_at_ribs',J.overlap(b,l-ribs)<1e-5)
    check('ribs_clear_new_pockets',J.overlap(ribs,poc)<1e-6)
    check('catch_tip_hooks_0_5_into_skirt',all(J.overlap(Pos(0,0,T.FREE_PLAY+.02)*l,c)>1e-4 for c in cat.solids()))
    check('catches_seated_clear',J.overlap(cat,l)<1e-5)
    check('pocket_spare_0_05',abs(RECESS-HOOK-.05)<1e-9 and S.SKIN-RECESS>=.8)
    lower=S.pry() & M.box(S.X0-2,S.X1,S.Y0,S.Y1,S.SEAM,S.SEAM+2)
    check('lid_pry_half_filled',vol(l & lower)>.5*vol(lower & S.outer(S.SEAM,S.SEAM+2)))
    check('base_pry_slot_kept',J.overlap(b,S.pry())<1e-5)
    zone=S.outer(S.SEAM,S.SEAM+S.LAP)-S.outer(S.SEAM-1,S.SEAM+S.LAP+1,S.SKIN+S.GAP)
    check('base_changes_only_at_catches',vol(diff(b-b13,zone))<1e-4 and vol(diff(b13-b,zone))<1e-4)
    below=M.box(S.X0-2,S.X1+2,S.Y0-2,S.Y1+2,S.SEAM+S.LAP+S.AXIAL+.01,100)
    check('lid_unchanged_above_joint',vol(diff(l & below,l16 & below))<1e-4 and vol(diff(l16 & below,l & below))<1e-4)
    check('lid_outer_skin_intact',vol(S.outer(S.SEAM+P.PRY_H,S.SEAM+S.LAP)-S.outer(S.SEAM-1,S.SEAM+S.LAP+1,S.SKIN-RECESS)-l)<1e-4)
    check('hardware_clear',J.overlap(b,M.hat()+M.pico())<1e-5)
    import math
    top=S.TOP+T5.RAISE;steep=[]
    near=M.box(S.X0+R.TOP_R+.2,S.X1-R.TOP_R-.2,S.Y0+R.TOP_R+.2,S.Y1-R.TOP_R-.2,top-1.3,top+1)
    for f in (l & near).faces():  # window + joystick + buttons edges, sampled
        for u in (.02,.25,.5,.75,.98):
            for w in (.02,.25,.5,.75,.98):
                try:pt=f.position_at(u,w);n=f.normal_at(pt)
                except Exception:continue
                if abs(pt.Z-top)>1e-3 and n.Z>math.cos(math.radians(45))+1e-2:steep.append((round(pt.X,1),round(pt.Y,1),round(pt.Z,2)))
    check('window_and_joystick_edges_max_45deg_overhang',not steep)
    nar,_=R.narrow_window(V.lid()[0]);wb=R.window_wire(R.top_face(nar)).bounding_box()
    sight=M.rbox(wb.min.X+.01,wb.max.X-.01,wb.min.Y+.01,wb.max.Y-.01,P.S3,top+1,P.WINDOW_R)
    check('window_open_down_to_glass',J.overlap(l,sight)<1e-5)
    hx,hy=M.JOY_C[0]+V.L4.DX,M.JOY_C[1]+V.L4.DY+V.JOY_DY
    check('joystick_hole_open',J.overlap(l,Pos(hx,hy,top-.5)*__import__('build123d').Cylinder(J.HOLE/2-.01,1.2))<1e-5)
    check('usb_open',J.overlap(b+l,M.box(M.PICO_CX-M.USB_HALF_W,M.PICO_CX+M.USB_HALF_W,M.IY1,S.Y1,M.USB_Z0+V.USB_DZ,M.USB_Z1+V.USB_DZ))<1e-5)
    check('joystick_clear',J.overlap(placed,l)<1e-5)
    check('buttons_clear',J.overlap(caps,l)<1e-5)
    report=dict(revision=REV,checks=checks,steep_top_edges=steep,passed=all(checks.values()),hook_mm=HOOK,catches=6,skin_at_pocket=round(S.SKIN-RECESS,2),
        ramp_deg_from_vertical=round(__import__('math').degrees(__import__('math').atan(PROJ/(Z_RAMP_TOP-Z_HOLD-NOSE))),1),
        closing_flex_mm=HOOK,physical_fit_confirmed=False,
        notes=['New base AND lid: v1.7 lid does not fit v1.3 bases (deeper catches).','Open with a thumbnail or small tool at the base slot.','Catch underside overhang 0.7 on the base: check slice.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
    if not report['passed']:raise SystemExit('Validation failed')
    J.export(V.origin(Rot(180,0,0)*l),STL/'lid-face-down.stl');J.export(V.origin(b),STL/'base-floor-down.stl')
    view={n:fn() for n,(fn,color) in V.V.PARTS.items()};view['base']=b;view['lid']=l;view['button_caps']=caps;view['joystick_cap']=placed
    export_step(Compound(children=list(view.values())),str(OUT/'assembly.step'))
    packed=[]
    with tempfile.TemporaryDirectory() as tmp:
        for name,s in view.items():
            path=Path(tmp)/(name+'.stl');J.export(s,path);bb=s.bounding_box()
            packed.append(dict(name=name,color=V.V.PARTS[name][1],stl=base64.b64encode(path.read_bytes()).decode(),bbox=[*tuple(bb.min),*tuple(bb.max)]))
    info=dict(commit=REV+' locking case',case_mm=[round(S.X1-S.X0,2),round(S.Y1-S.Y0,2),round(S.TOP+T5.RAISE-M.Z_BOTTOM,2)],split_z=S.SEAM,assumptions=['6 catches, 0.5mm hook, gentle ramp.','Lid pry notch filled; base slot only.','New base and lid together.','J9 and buttons unchanged.'])
    html=(ROOT/'cad/viewer_template.html').read_text().replace('/*__PARTS__*/','const PARTS = '+json.dumps(packed)+';').replace('/*__INFO__*/','const INFO = '+json.dumps(info)+';').replace('V3 review · NOT APPROVED FOR PRINT','V1.7 · LOCKING CASE').replace('V3 Case Review — Not Approved for Print','V1.7 locking case')
    (OUT/'viewer.html').write_text(html);(ROOT/'renders/viewer.html').write_text(html)
    sources=[Path(__file__),*[ROOT/'cad'/n for n in ('v1_5_tall.py','v1_4_rounded.py','v1_1_spacer.py','v1_3_short_end.py','v1_production.py','s2_tight_base.py','s1_strong_shell.py','model.py','params.py')]]
    outputs=[*sorted(STL.glob('*.stl')),OUT/'assembly.step',OUT/'validation.json',OUT/'viewer.html']
    (OUT/'manifest.json').write_text(json.dumps(dict(revision=REV,supports=False,raft=False,slice_verified=False,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}),indent=2)+'\n')

if __name__=='__main__':main()
